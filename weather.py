from typing import Any, List, Dict, Optional
import httpx
from mcp.server.fastmcp import FastMCP
from datetime import datetime
import json

mcp = FastMCP("weather")

class WeatherContext:
    def __init__(self):
        self.location_history = []
        self.last_queries = []
        self.user_preferences = {}
        self.alert_history = []
        self.monitoring_settings = {}
        self.weather_trends = []
        self.user_interactions = []
        self.alert_thresholds = {
            "temperature": {"min": 32, "max": 90},
            "wind_speed": {"min": 0, "max": 30},
            "precipitation": {"min": 0, "max": 0.5}
        }

    def add_interaction(self, action: str, details: dict):
        """Record user interaction with timestamp."""
        self.user_interactions.append({
            "action": action,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })
        # Keep only last 100 interactions
        self.user_interactions = self.user_interactions[-100:]

    def update_weather_trends(self, conditions: dict):
        """Update weather trends with new conditions."""
        self.weather_trends.append({
            "conditions": conditions,
            "timestamp": datetime.now().isoformat()
        })
        # Keep only last 24 hours of trends
        self.weather_trends = self.weather_trends[-24:]

    def check_alert_conditions(self, conditions: dict) -> list:
        """Check if current conditions exceed alert thresholds."""
        alerts = []
        if conditions.get("temperature"):
            temp = conditions["temperature"]
            if temp < self.alert_thresholds["temperature"]["min"]:
                alerts.append(f"Temperature Alert: {temp}°F is below minimum threshold")
            elif temp > self.alert_thresholds["temperature"]["max"]:
                alerts.append(f"Temperature Alert: {temp}°F is above maximum threshold")
        
        if conditions.get("wind_speed"):
            wind = conditions["wind_speed"]
            if wind > self.alert_thresholds["wind_speed"]["max"]:
                alerts.append(f"Wind Alert: {wind} mph exceeds maximum threshold")
        
        return alerts

    def update_context(self, lat: float, lon: float, state: str = None):
        """Update the context with new location information."""
        self.location_history.append({
            "lat": lat,
            "lon": lon,
            "state": state,
            "timestamp": datetime.now().isoformat()
        })
        # Keep only last 10 locations
        self.location_history = self.location_history[-10:]

class WeatherModel:
    def __init__(self):
        self.NWS_API_BASE = "https://api.weather.gov"
        self.USER_AGENT = "weather-app/1.0"
        self.context = WeatherContext()

    async def make_nws_request(self, url: str) -> dict[str, Any] | None:
        """Make a request to the NWS API and return the response as a dictionary."""
        headers = {
            "User-Agent": self.USER_AGENT,
            "Accept": "application/geo+json"
        }
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=headers, timeout=30.0)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                self.context.last_queries.append({
                    "url": url,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                })
                return None

    def update_context(self, lat: float, lon: float, state: str = None):
        """Update the context with new location information."""
        self.context.location_history.append({
            "lat": lat,
            "lon": lon,
            "state": state,
            "timestamp": datetime.now().isoformat()
        })
        # Keep only last 10 locations
        self.context.location_history = self.context.location_history[-10:]

    async def get_current_conditions(self, lat: float, lon: float) -> str:
        """Get current weather conditions for a specific location."""
        self.update_context(lat, lon)
        
        points_url = f"{self.NWS_API_BASE}/points/{lat},{lon}"
        points_data = await self.make_nws_request(points_url)
        
        if not points_data:
            return "Unable to fetch location data."
        
        forecast_url = points_data["properties"]["forecast"]
        forecast_data = await self.make_nws_request(forecast_url)
        
        if not forecast_data or "properties" not in forecast_data:
            return "Unable to fetch forecast data."
        
        current = forecast_data["properties"]["periods"][0]
        
        # Create conditions dictionary for context with proper type conversion
        conditions = {
            "temperature": float(current.get("temperature", 0)),
            "wind_speed": float(current.get("windSpeed", "0").split()[0]),  # Extract numeric part from "X mph"
            "conditions": current.get("shortForecast"),
            "humidity": float(current.get("relativeHumidity", {}).get("value", 0))
        }
        
        # Update weather trends
        self.context.update_weather_trends(conditions)
        
        # Check for alert conditions
        alerts = self.context.check_alert_conditions(conditions)
        
        # Record interaction
        self.context.add_interaction("get_current_conditions", {
            "lat": lat,
            "lon": lon,
            "conditions": conditions,
            "alerts": alerts
        })
        
        # Build response with alerts if any
        response = f"""\
Current Conditions:
Temperature: {current.get('temperature', 'N/A')}°F
Wind: {current.get('windSpeed', 'N/A')} {current.get('windDirection', '')}
Conditions: {current.get('shortForecast', 'N/A')}
Humidity: {current.get('relativeHumidity', {}).get('value', 'N/A')}%
"""
        
        if alerts:
            response += "\nAlerts:\n" + "\n".join(alerts)
        
        return response

    async def get_hourly_forecast(self, lat: float, lon: float) -> str:
        """Get hourly weather forecast for a specific location."""
        self.update_context(lat, lon)
        
        points_url = f"{self.NWS_API_BASE}/points/{lat},{lon}"
        points_data = await self.make_nws_request(points_url)
        
        if not points_data:
            return "Unable to fetch location data."
        
        hourly_url = points_data["properties"]["forecastHourly"]
        hourly_data = await self.make_nws_request(hourly_url)
        
        if not hourly_data or "properties" not in hourly_data:
            return "Unable to fetch hourly forecast data."
        
        periods = hourly_data["properties"]["periods"][:24]
        forecast = []
        
        for period in periods:
            forecast.append(f"""\
Time: {period.get('startTime', 'N/A')}
Temperature: {period.get('temperature', 'N/A')}°F
Conditions: {period.get('shortForecast', 'N/A')}
Wind: {period.get('windSpeed', 'N/A')} {period.get('windDirection', '')}
""")
        
        return "\n---\n".join(forecast)

    async def get_daily_forecast(self, lat: float, lon: float) -> str:
        """Get daily weather forecast for a specific location."""
        self.update_context(lat, lon)
        
        points_url = f"{self.NWS_API_BASE}/points/{lat},{lon}"
        points_data = await self.make_nws_request(points_url)
        
        if not points_data:
            return "Unable to fetch location data."
        
        forecast_url = points_data["properties"]["forecast"]
        forecast_data = await self.make_nws_request(forecast_url)
        
        if not forecast_data or "properties" not in forecast_data:
            return "Unable to fetch forecast data."
        
        periods = forecast_data["properties"]["periods"]
        forecast = []
        
        for period in periods:
            forecast.append(f"""\
Day: {period.get('name', 'N/A')}
Temperature: {period.get('temperature', 'N/A')}°F
Conditions: {period.get('shortForecast', 'N/A')}
Wind: {period.get('windSpeed', 'N/A')} {period.get('windDirection', '')}
Details: {period.get('detailedForecast', 'N/A')}
""")
        
        return "\n---\n".join(forecast)

    async def get_radar_data(self, lat: float, lon: float) -> str:
        """Get weather radar data for a specific location."""
        self.update_context(lat, lon)
        
        points_url = f"{self.NWS_API_BASE}/points/{lat},{lon}"
        points_data = await self.make_nws_request(points_url)
        
        if not points_data:
            return "Unable to fetch location data."
        
        radar_url = f"{self.NWS_API_BASE}/radar/stations"
        radar_data = await self.make_nws_request(radar_url)
        
        if not radar_data or "features" not in radar_data:
            return "Unable to fetch radar data."
        
        nearest_station = None
        min_distance = float('inf')
        
        for station in radar_data["features"]:
            station_lat = station["geometry"]["coordinates"][1]
            station_lon = station["geometry"]["coordinates"][0]
            distance = ((station_lat - lat) ** 2 + (station_lon - lon) ** 2) ** 0.5
            
            if distance < min_distance:
                min_distance = distance
                nearest_station = station
        
        if not nearest_station:
            return "No radar stations found nearby."
        
        return f"""\
Nearest Radar Station: {nearest_station['properties'].get('name', 'Unknown')}
Location: {nearest_station['properties'].get('location', 'Unknown')}
Status: {nearest_station['properties'].get('status', 'Unknown')}
Distance: {min_distance:.2f} degrees
"""

    async def get_alerts(self, state: str) -> str:
        """Get weather alerts for a US state."""
        url = f"{self.NWS_API_BASE}/alerts/active/area/{state}"
        data = await self.make_nws_request(url)
        
        if not data or "features" not in data:
            return "Unable to fetch alerts or no alerts found."
        
        if not data["features"]:
            return "No active alerts for this state."
        
        alerts = []
        for feature in data["features"]:
            props = feature["properties"]
            alert = {
                "event": props.get('event', 'Unknown'),
                "area": props.get('areaDesc', 'Unknown'),
                "severity": props.get('severity', 'Unknown'),
                "description": props.get('description', 'No description available'),
                "instructions": props.get('instruction', 'No specific instructions provided')
            }
            alerts.append(alert)
            self.context.alert_history.append(alert)
        
        # Keep only last 50 alerts
        self.context.alert_history = self.context.alert_history[-50:]
        
        return "\n---\n".join([
            f"""\
Event: {alert['event']}
Area: {alert['area']}
Severity: {alert['severity']}
Description: {alert['description']}
Instructions: {alert['instructions']}"""
            for alert in alerts
        ])

    async def monitor_conditions(self, lat: float, lon: float, interval_minutes: int = 15) -> str:
        """Monitor weather conditions at regular intervals."""
        self.update_context(lat, lon)
        self.context.monitoring_settings = {
            "lat": lat,
            "lon": lon,
            "interval": interval_minutes,
            "last_update": datetime.now().isoformat()
        }
        
        points_url = f"{self.NWS_API_BASE}/points/{lat},{lon}"
        points_data = await self.make_nws_request(points_url)
        
        if not points_data:
            return "Unable to fetch location data."
        
        forecast_url = points_data["properties"]["forecast"]
        forecast_data = await self.make_nws_request(forecast_url)
        
        if not forecast_data or "properties" not in forecast_data:
            return "Unable to fetch forecast data."
        
        current = forecast_data["properties"]["periods"][0]
        last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return f"""\
Weather Monitoring (Last Updated: {last_updated})
Temperature: {current.get('temperature', 'N/A')}°F
Conditions: {current.get('shortForecast', 'N/A')}
Wind: {current.get('windSpeed', 'N/A')} {current.get('windDirection', '')}
Humidity: {current.get('relativeHumidity', {}).get('value', 'N/A')}%
Update Interval: {interval_minutes} minutes
"""

    def get_context_summary(self) -> str:
        """Get a detailed summary of the current context."""
        last_location = self.context.location_history[-1] if self.context.location_history else None
        last_interaction = self.context.user_interactions[-1] if self.context.user_interactions else None
        recent_trends = self.context.weather_trends[-3:] if self.context.weather_trends else []
        
        location_str = f"{last_location['lat']:.4f}, {last_location['lon']:.4f} ({last_location['state']})" if last_location else 'None'
        
        summary = f"""\
Context Summary:
Last Location: {location_str}
Recent Queries: {len(self.context.last_queries)}
Active Alerts: {len(self.context.alert_history)}
Monitoring Active: {'Yes' if self.context.monitoring_settings else 'No'}
Last Interaction: {last_interaction['action'] if last_interaction else 'None'}
Weather Trends: {len(recent_trends)} recent updates
Alert Thresholds:
  Temperature: {self.context.alert_thresholds['temperature']['min']}°F - {self.context.alert_thresholds['temperature']['max']}°F
  Wind Speed: {self.context.alert_thresholds['wind_speed']['max']} mph max
"""
        return summary

# Create a singleton instance
weather_model = WeatherModel()

@mcp.resource("config://app")
def get_config() -> str:
    """Static configuration data"""
    return "App configuration here"

@mcp.tool()
async def get_current_conditions(lat: float, lon: float) -> str:
    """Get current weather conditions for a specific location.
    
    Args:
        lat: Latitude of the location
        lon: Longitude of the location
    """
    return await weather_model.get_current_conditions(lat, lon)

@mcp.tool()
async def get_hourly_forecast(lat: float, lon: float) -> str:
    """Get hourly weather forecast for a specific location.
    
    Args:
        lat: Latitude of the location
        lon: Longitude of the location
    """
    return await weather_model.get_hourly_forecast(lat, lon)

@mcp.tool()
async def get_daily_forecast(lat: float, lon: float) -> str:
    """Get daily weather forecast for a specific location.
    
    Args:
        lat: Latitude of the location
        lon: Longitude of the location
    """
    return await weather_model.get_daily_forecast(lat, lon)

@mcp.tool()
async def get_radar_data(lat: float, lon: float) -> str:
    """Get weather radar data for a specific location.
    
    Args:
        lat: Latitude of the location
        lon: Longitude of the location
    """
    return await weather_model.get_radar_data(lat, lon)

@mcp.tool()
async def monitor_conditions(lat: float, lon: float, interval_minutes: int = 15) -> str:
    """Monitor weather conditions at regular intervals.
    
    Args:
        lat: Latitude of the location
        lon: Longitude of the location
        interval_minutes: Update interval in minutes (default: 15)
    """
    return await weather_model.monitor_conditions(lat, lon, interval_minutes)

@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state.

    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    return await weather_model.get_alerts(state)


