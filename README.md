# Weather Dashboard MCP 🌤️

A powerful real-time weather dashboard built with Streamlit and FastMCP, providing comprehensive weather data from the National Weather Service API. This application offers a user-friendly interface to access detailed weather information for any location in the United States.

![Weather Dashboard](https://img.shields.io/badge/Weather-Dashboard-blue)
![Python](https://img.shields.io/badge/Python-3.13+-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32.0+-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🌟 Features

### Current Weather
- Real-time temperature and conditions
- Wind speed and direction
- Humidity levels
- Detailed weather descriptions

### Forecasts
- **Hourly Forecast**: Next 24 hours of weather predictions
- **Daily Forecast**: Extended weather outlook
- Temperature trends
- Precipitation probability
- Wind conditions

### Weather Radar
- Nearest radar station information
- Station status and location
- Distance calculations
- Coverage area details

### Weather Alerts
- Active weather warnings
- Severe weather notifications
- Area-specific alerts
- Alert severity levels

### Monitoring
- Continuous weather tracking
- Customizable update intervals
- Real-time data refresh
- Historical data comparison

## 🛠️ Technical Stack

- **Frontend**: Streamlit
- **Backend**: FastMCP
- **API**: National Weather Service (NWS)
- **HTTP Client**: httpx
- **Language**: Python 3.13+

## 📋 Prerequisites

- Python 3.13 or higher
- pip (Python package manager)
- Git
- Virtual environment (recommended)
- Internet connection for API access

## 🚀 Installation

1. **Clone the repository**:
```bash
git clone https://github.com/wasifkhandev/weather-dashboard-mcp.git
cd weather-dashboard-mcp
```

2. **Create and activate virtual environment**:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Unix/MacOS
python -m venv venv
source venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

## 💻 Usage

1. **Start the application**:
```bash
cd server
python -m streamlit run weather_app.py
```

2. **Access the dashboard**:
Open your web browser and navigate to:
```
http://localhost:8501
```

3. **Using the dashboard**:
   - Enter location coordinates in the sidebar
   - Select your state code for alerts
   - Use the tabs to access different features
   - Click buttons to fetch real-time data

## 📍 Example Coordinates

| City | Latitude | Longitude |
|------|----------|-----------|
| New York City | 40.7128 | -74.006 |
| Los Angeles | 34.0522 | -118.2437 |
| Chicago | 41.8781 | -87.6298 |
| Miami | 25.7617 | -80.1918 |
| Seattle | 47.6062 | -122.3321 |

## 📁 Project Structure

```
weather-dashboard-mcp/
├── server/
│   ├── weather.py          # Core weather functionality
│   ├── weather_app.py      # Streamlit UI
│   └── venv/               # Virtual environment
├── README.md              # Project documentation
├── requirements.txt       # Project dependencies
└── LICENSE               # MIT License
```

## 🔧 API Reference

The application uses the National Weather Service (NWS) API:
- **Base URL**: https://api.weather.gov
- **Documentation**: https://www.weather.gov/documentation/services-web-api
- **Rate Limits**: 30 requests per minute
- **Data Format**: GeoJSON

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guide
- Add comments for complex functions
- Update documentation for new features
- Write clear commit messages

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- National Weather Service for providing the weather data API
- Streamlit for the web application framework
- FastMCP for the backend functionality
- All contributors and users of the project

## 📞 Support

For support, please:
1. Check the [documentation](https://www.weather.gov/documentation/services-web-api)
2. Open an [issue](https://github.com/wasifkhandev/weather-dashboard-mcp/issues)
3. Contact the maintainers

## 🔄 Updates

Stay updated with the latest changes by:
- Watching the repository
- Following the release notes
- Checking the commit history

---

Made with ❤️ by [Wasif Khan](https://github.com/wasifkhandev)
