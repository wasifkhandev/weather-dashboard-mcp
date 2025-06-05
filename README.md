# Real-Time Weather Dashboard with MCP Integration

A sophisticated weather application that provides real-time weather data, forecasts, and monitoring capabilities, enhanced with Model Context Protocol (MCP) for intelligent context management.

## 🌟 Latest Updates

### MCP Integration Enhancements
- **Context-Aware Weather System**
  - Real-time context tracking
  - User interaction history
  - Weather trend analysis
  - Smart alert system

### Recent Improvements
- Fixed type conversion for weather data
- Enhanced error handling
- Improved real-time monitoring
- Better context management
- Line ending standardization

## Features

### Core Weather Features
- Real-time current conditions
- Hourly and daily forecasts
- Weather radar data
- Active weather alerts
- Continuous weather monitoring

### MCP Integration Features
- **Context Management**
  - Location history tracking (last 10 locations)
  - User interaction logging (last 100 actions)
  - Weather trend analysis (24-hour history)
  - Alert history maintenance

- **Smart Alert System**
  - Customizable thresholds for:
    - Temperature (min/max)
    - Wind speed
    - Precipitation
  - Real-time alert generation
  - Historical alert tracking

- **Weather Trend Analysis**
  - 24-hour weather condition history
  - Pattern recognition
  - Historical comparisons
  - Trend visualization

- **User Interaction Tracking**
  - Action history with timestamps
  - User preference management
  - Personalized weather updates

## Technical Stack

- Python 3.13+
- Streamlit for UI
- FastMCP for context management
- httpx for async HTTP requests
- National Weather Service API

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd MCPServer
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On Unix/MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install "mcp[cli]>=1.9.2" streamlit httpx
```

## Usage

1. Start the application:
```bash
cd server
python -m streamlit run weather_app.py
```

2. Access the dashboard at `http://localhost:8501`

3. Use the sidebar to:
   - Set location coordinates
   - View context information
   - Monitor weather trends

4. Main features available in tabs:
   - Current Conditions
   - Forecasts (Hourly/Daily)
   - Radar
   - Alerts
   - Monitoring

## MCP Context Features

### Location Context
- Tracks last 10 locations
- Maintains location history with timestamps
- Enables location-based trend analysis

### User Interaction Context
- Records last 100 user actions
- Tracks interaction timestamps
- Maintains user preferences

### Weather Trend Context
- Stores 24 hours of weather data
- Enables pattern recognition
- Supports historical analysis

### Alert Context
- Customizable thresholds
- Real-time alert generation
- Historical alert tracking

## Recent Changes

### Version 1.1.0
- Added MCP context management
- Implemented smart alert system
- Enhanced weather trend analysis
- Fixed type conversion issues
- Standardized line endings
- Improved error handling

### Version 1.0.0
- Initial release with basic weather features
- Streamlit UI implementation
- NWS API integration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- National Weather Service API for weather data
- Streamlit for the web interface
- FastMCP for context management
