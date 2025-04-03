import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import os

# Set page configuration
st.set_page_config(
    page_title="Mining Safety Monitoring System",
    page_icon="⛏️",
    layout="wide"
)

# Application title
st.title("IoT-Based Mining Safety Tracking System")
st.markdown("Real-time monitoring of mining conditions and worker safety")

# Sidebar for controls
st.sidebar.header("System Controls")
mine_section = st.sidebar.selectbox(
    "Select Mine Section",
    ["Section A", "Section B", "Section C", "All Sections"]
)

# Function to generate simulated sensor data
def generate_sensor_data(num_miners=5):
    current_time = datetime.now()
    
    data = []
    sections = ["Section A", "Section B", "Section C"]
    gas_types = ["Methane", "Carbon Monoxide", "Hydrogen Sulfide"]
    
    for i in range(num_miners):
        miner_id = f"MINER_{i+1:03d}"
        section = random.choice(sections)
        temperature = round(random.uniform(20, 40), 1)  # Temperature in Celsius
        humidity = round(random.uniform(40, 95), 1)  # Humidity percentage
        gas_level = round(random.uniform(0, 100), 1)  # Gas level in ppm
        gas_type = random.choice(gas_types)
        oxygen_level = round(random.uniform(18, 21), 1)  # Oxygen level percentage
        helmet_status = random.choice(["Worn", "Not Worn"])
        battery_level = round(random.uniform(20, 100), 1)  # Battery percentage
        
        # Calculate alert status
        alert = False
        alert_message = "Normal"
        
        if temperature > 35:
            alert = True
            alert_message = "High Temperature"
        elif gas_level > 70:
            alert = True
            alert_message = f"High {gas_type} Level"
        elif oxygen_level < 19:
            alert = True
            alert_message = "Low Oxygen"
        elif helmet_status == "Not Worn":
            alert = True
            alert_message = "Helmet Not Worn"
        elif battery_level < 30:
            alert = True
            alert_message = "Low Battery"
            
        data.append({
            "timestamp": current_time - timedelta(minutes=random.randint(0, 30)),
            "miner_id": miner_id,
            "section": section,
            "temperature": temperature,
            "humidity": humidity,
            "gas_level": gas_level,
            "gas_type": gas_type,
            "oxygen_level": oxygen_level,
            "helmet_status": helmet_status,
            "battery_level": battery_level,
            "alert": alert,
            "alert_message": alert_message
        })
    
    return pd.DataFrame(data)

# Function to load sample data or generate new data
def load_or_generate_data():
    try:
        # Try to load sample data if it exists
        if os.path.exists("data/sample_data.csv"):
            df = pd.read_csv("data/sample_data.csv")
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            return df
        else:
            return generate_sensor_data(10)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return generate_sensor_data(10)

# Generate initial data
if 'sensor_data' not in st.session_state:
    st.session_state.sensor_data = load_or_generate_data()
    st.session_state.historical_data = st.session_state.sensor_data.copy()
    st.session_state.last_update = datetime.now()

# Update data button
if st.sidebar.button("Update Sensor Data"):
    new_data = generate_sensor_data(10)
    st.session_state.sensor_data = new_data
    st.session_state.historical_data = pd.concat([st.session_state.historical_data, new_data])
    st.session_state.last_update = datetime.now()

# Auto-refresh option
auto_refresh = st.sidebar.checkbox("Enable Auto-refresh (30s)")
if auto_refresh:
    time_diff = (datetime.now() - st.session_state.last_update).total_seconds()
    if time_diff > 30:
        new_data = generate_sensor_data(10)
        st.session_state.sensor_data = new_data
        st.session_state.historical_data = pd.concat([st.session_state.historical_data, new_data])
        st.session_state.last_update = datetime.now()
        st.experimental_rerun()

# Display last update time
st.sidebar.write(f"Last updated: {st.session_state.last_update.strftime('%Y-%m-%d %H:%M:%S')}")

# Filter data based on selected section
if mine_section != "All Sections":
    filtered_data = st.session_state.sensor_data[st.session_state.sensor_data["section"] == mine_section]
else:
    filtered_data = st.session_state.sensor_data

# Dashboard layout
col1, col2 = st.columns(2)

# Alert summary
with col1:
    st.subheader("Safety Alerts")
    alert_data = filtered_data[filtered_data["alert"] == True]
    
    if not alert_data.empty:
        st.error(f"{len(alert_data)} alerts detected!")
        for _, alert in alert_data.iterrows():
            st.warning(f"⚠️ {alert['miner_id']} in {alert['section']}: {alert['alert_message']}")
    else:
        st.success("No alerts detected. All systems normal.")

# Environmental conditions summary
with col2:
    st.subheader("Environmental Conditions")
    avg_temp = filtered_data["temperature"].mean()
    avg_humidity = filtered_data["humidity"].mean()
    avg_oxygen = filtered_data["oxygen_level"].mean()
    
    col2a, col2b, col2c = st.columns(3)
    col2a.metric("Avg. Temperature", f"{avg_temp:.1f}°C")
    col2b.metric("Avg. Humidity", f"{avg_humidity:.1f}%")
    col2c.metric("Avg. Oxygen Level", f"{avg_oxygen:.1f}%")
    
    # Gas levels chart
    gas_data = filtered_data.groupby("gas_type")["gas_level"].mean().reset_index()
    fig = px.bar(gas_data, x="gas_type", y="gas_level", 
                 title="Average Gas Levels by Type",
                 labels={"gas_type": "Gas Type", "gas_level": "Level (ppm)"},
                 color="gas_level", color_continuous_scale="Viridis")
    st.plotly_chart(fig, use_container_width=True)

# Miner status table
st.subheader("Miner Status")
st.dataframe(filtered_data[["miner_id", "section", "temperature", "humidity", 
                           "gas_level", "gas_type", "oxygen_level", 
                           "helmet_status", "battery_level", "alert_message"]], 
            use_container_width=True)

# Visualizations
st.subheader("Data Visualization")

tab1, tab2, tab3 = st.tabs(["Temperature & Humidity", "Gas Levels", "Battery Status"])

with tab1:
    # Temperature and humidity scatter plot
    fig = px.scatter(filtered_data, x="temperature", y="humidity", 
                     color="section", size="oxygen_level",
                     hover_data=["miner_id", "alert_message"],
                     title="Temperature vs. Humidity by Mine Section")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    # Gas levels by miner
    fig = px.bar(filtered_data, x="miner_id", y="gas_level", 
                 color="gas_type", barmode="group",
                 title="Gas Levels by Miner")
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    # Battery status
    fig = px.bar(filtered_data, x="miner_id", y="battery_level",
                 color="battery_level", color_continuous_scale="RdYlGn",
                 title="Battery Levels by Miner")
    fig.add_hline(y=30, line_dash="dash", line_color="red", annotation_text="Low Battery Threshold")
    st.plotly_chart(fig, use_container_width=True)

# Map visualization (simulated)
st.subheader("Miner Location Map")
st.info("This is a simulated map. In a real implementation, this would show actual GPS coordinates.")

# Generate random coordinates for miners
map_data = filtered_data.copy()
# Center coordinates (can be adjusted to any mine location)
center_lat, center_lon = 37.7749, -122.4194
map_data["lat"] = [center_lat + random.uniform(-0.01, 0.01) for _ in range(len(map_data))]
map_data["lon"] = [center_lon + random.uniform(-0.01, 0.01) for _ in range(len(map_data))]

# Create the map
fig = px.scatter_mapbox(map_data, lat="lat", lon="lon", 
                        hover_name="miner_id", 
                        hover_data=["section", "alert_message"],
                        color="alert", color_discrete_map={True: "red", False: "green"},
                        zoom=14, height=500)
fig.update_layout(mapbox_style="open-street-map")
st.plotly_chart(fig, use_container_width=True)

# Historical data analysis
st.subheader("Historical Data Analysis")
if st.checkbox("Show Historical Data Analysis"):
    # Create time-based analysis if we have enough historical data
    if len(st.session_state.historical_data) > 10:
        # Group by timestamp (hourly)
        st.session_state.historical_data['hour'] = st.session_state.historical_data['timestamp'].dt.floor('H')
        hourly_data = st.session_state.historical_data.groupby('hour').agg({
            'temperature': 'mean',
            'humidity': 'mean',
            'gas_level': 'mean',
            'oxygen_level': 'mean',
            'alert': 'sum'
        }).reset_index()
        
        # Plot time series
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hourly_data['hour'], y=hourly_data['temperature'], 
                                mode='lines+markers', name='Temperature'))
        fig.add_trace(go.Scatter(x=hourly_data['hour'], y=hourly_data['humidity'], 
                                mode='lines+markers', name='Humidity'))
        fig.add_trace(go.Scatter(x=hourly_data['hour'], y=hourly_data['gas_level'], 
                                mode='lines+markers', name='Gas Level'))
        fig.update_layout(title='Environmental Conditions Over Time',
                        xaxis_title='Time',
                        yaxis_title='Value')
        st.plotly_chart(fig, use_container_width=True)
        
        # Alert frequency
        fig = px.bar(hourly_data, x='hour', y='alert', 
                    title='Number of Alerts Over Time')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Not enough historical data available yet. Please update sensor data a few more times.")

# Footer
st.markdown("---")
st.markdown("IoT-Based Mining Safety Tracking System - Developed for mine worker safety")
st.markdown("GitHub: [Mining Safety Tracker Repository](https://github.com/yourusername/mining-safety-tracker)")
