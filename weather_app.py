import streamlit as st
from weather import (
    get_current_conditions,
    get_hourly_forecast,
    get_daily_forecast,
    get_radar_data,
    monitor_conditions,
    get_alerts,
    weather_model
)
import asyncio
import time
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Real-Time Weather Dashboard",
    page_icon="🌤️",
    layout="wide"
)

# Custom CSS for better visibility
st.markdown("""
    <style>
    .main {
        padding: 2rem;
        background-color: #ffffff;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        padding: 10px;
        border-radius: 5px;
        border: none;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .weather-card {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .context-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
        border: 1px solid #dee2e6;
    }
    h1, h2, h3 {
        color: #1f1f1f;
    }
    .stMarkdown {
        color: #1f1f1f;
    }
    </style>
    """, unsafe_allow_html=True)

# Title
st.title("🌤️ Real-Time Weather Dashboard")

# Sidebar for location input
with st.sidebar:
    st.header("Location Settings")
    lat = st.number_input("Latitude", value=40.7128, format="%.4f")
    lon = st.number_input("Longitude", value=-74.006, format="%.4f")
    state = st.text_input("State (2-letter code)", value="NY").upper()
    
    # Display context information
    st.markdown("---")
    st.subheader("Context Information")
    context_summary = weather_model.get_context_summary()
    st.markdown(f'<div class="context-card">{context_summary}</div>', unsafe_allow_html=True)

# Create tabs for different features
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Current Conditions", 
    "Forecasts", 
    "Radar", 
    "Alerts", 
    "Monitoring"
])

# Helper function to run async functions
def run_async(func, *args):
    return asyncio.run(func(*args))

# Current Conditions Tab
with tab1:
    st.header("Current Weather Conditions")
    if st.button("Refresh Current Conditions"):
        with st.spinner("Fetching current conditions..."):
            conditions = run_async(get_current_conditions, lat, lon)
            st.markdown(f'<div class="weather-card">{conditions}</div>', unsafe_allow_html=True)

# Forecasts Tab
with tab2:
    st.header("Weather Forecasts")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Hourly Forecast")
        if st.button("Get Hourly Forecast"):
            with st.spinner("Fetching hourly forecast..."):
                hourly = run_async(get_hourly_forecast, lat, lon)
                st.markdown(f'<div class="weather-card">{hourly}</div>', unsafe_allow_html=True)
    
    with col2:
        st.subheader("Daily Forecast")
        if st.button("Get Daily Forecast"):
            with st.spinner("Fetching daily forecast..."):
                daily = run_async(get_daily_forecast, lat, lon)
                st.markdown(f'<div class="weather-card">{daily}</div>', unsafe_allow_html=True)

# Radar Tab
with tab3:
    st.header("Weather Radar")
    if st.button("Get Radar Data"):
        with st.spinner("Fetching radar data..."):
            radar = run_async(get_radar_data, lat, lon)
            st.markdown(f'<div class="weather-card">{radar}</div>', unsafe_allow_html=True)

# Alerts Tab
with tab4:
    st.header("Weather Alerts")
    if st.button("Check Alerts"):
        with st.spinner("Checking weather alerts..."):
            alerts = run_async(get_alerts, state)
            st.markdown(f'<div class="weather-card">{alerts}</div>', unsafe_allow_html=True)

# Monitoring Tab
with tab5:
    st.header("Real-Time Weather Monitoring")
    interval = st.slider("Update Interval (minutes)", 1, 60, 15)
    
    if st.button("Start Monitoring"):
        st.info(f"Monitoring weather conditions every {interval} minutes...")
        monitoring_placeholder = st.empty()
        
        while True:
            with monitoring_placeholder.container():
                monitoring = run_async(monitor_conditions, lat, lon, interval)
                st.markdown(f'<div class="weather-card">{monitoring}</div>', unsafe_allow_html=True)
                st.write(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            time.sleep(interval * 60)  # Convert minutes to seconds

# Footer
st.markdown("---")
st.markdown("Data provided by National Weather Service API") 