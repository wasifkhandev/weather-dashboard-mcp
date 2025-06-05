from typing import Any, List, Dict
import httpx
from mcp.server.fastmcp import FastMCP
from datetime import datetime

mcp = FastMCP("weather")

NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

async def make_nws_request(url:str)-> dict[str,Any] | None:
    """Make a request to the NWS API and return the response as a dictionary."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception: 
            return None

def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    return f"""\
Event: {props.get('event', 'Unknown')}
Area: {props.get('areaDesc', 'Unknown')}
Severity: {props.get('severity', 'Unknown')}
Description: {props.get('description', 'No description available')}
Instructions: {props.get('instruction', 'No specific instructions provided')}
"""

@mcp.tool()
async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state.

    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["features"]:
        return "No active alerts for this state."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n---\n".join(alerts)

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
    # First get the grid endpoint
    points_url = f"{NWS_API_BASE}/points/{lat},{lon}"
    points_data = await make_nws_request(points_url)
    
    if not points_data:
        return "Unable to fetch location data."
    
    # Get the forecast URL from the points data
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)
    
    if not forecast_data or "properties" not in forecast_data:
        return "Unable to fetch forecast data."
    
    # Get current conditions
    current = forecast_data["properties"]["periods"][0]
    return f"""\
Current Conditions:
Temperature: {current.get('temperature', 'N/A')}°F
Wind: {current.get('windSpeed', 'N/A')} {current.get('windDirection', '')}
Conditions: {current.get('shortForecast', 'N/A')}
Humidity: {current.get('relativeHumidity', {}).get('value', 'N/A')}%
"""

@mcp.tool()
async def get_hourly_forecast(lat: float, lon: float) -> str:
    """Get hourly weather forecast for a specific location.
    
    Args:
        lat: Latitude of the location
        lon: Longitude of the location
    """
    points_url = f"{NWS_API_BASE}/points/{lat},{lon}"
    points_data = await make_nws_request(points_url)
    
    if not points_data:
        return "Unable to fetch location data."
    
    hourly_url = points_data["properties"]["forecastHourly"]
    hourly_data = await make_nws_request(hourly_url)
    
    if not hourly_data or "properties" not in hourly_data:
        return "Unable to fetch hourly forecast data."
    
    periods = hourly_data["properties"]["periods"][:24]  # Get next 24 hours
    forecast = []
    
    for period in periods:
        forecast.append(f"""\
Time: {period.get('startTime', 'N/A')}
Temperature: {period.get('temperature', 'N/A')}°F
Conditions: {period.get('shortForecast', 'N/A')}
Wind: {period.get('windSpeed', 'N/A')} {period.get('windDirection', '')}
""")
    
    return "\n---\n".join(forecast)

@mcp.tool()
async def get_daily_forecast(lat: float, lon: float) -> str:
    """Get daily weather forecast for a specific location.
    
    Args:
        lat: Latitude of the location
        lon: Longitude of the location
    """
    points_url = f"{NWS_API_BASE}/points/{lat},{lon}"
    points_data = await make_nws_request(points_url)
    
    if not points_data:
        return "Unable to fetch location data."
    
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)
    
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

@mcp.tool()
async def get_radar_data(lat: float, lon: float) -> str:
    """Get weather radar data for a specific location.
    
    Args:
        lat: Latitude of the location
        lon: Longitude of the location
    """
    points_url = f"{NWS_API_BASE}/points/{lat},{lon}"
    points_data = await make_nws_request(points_url)
    
    if not points_data:
        return "Unable to fetch location data."
    
    radar_url = f"{NWS_API_BASE}/radar/stations"
    radar_data = await make_nws_request(radar_url)
    
    if not radar_data or "features" not in radar_data:
        return "Unable to fetch radar data."
    
    # Find the nearest radar station
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

@mcp.tool()
async def monitor_conditions(lat: float, lon: float, interval_minutes: int = 15) -> str:
    """Monitor weather conditions at regular intervals.
    
    Args:
        lat: Latitude of the location
        lon: Longitude of the location
        interval_minutes: Update interval in minutes (default: 15)
    """
    points_url = f"{NWS_API_BASE}/points/{lat},{lon}"
    points_data = await make_nws_request(points_url)
    
    if not points_data:
        return "Unable to fetch location data."
    
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)
    
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


