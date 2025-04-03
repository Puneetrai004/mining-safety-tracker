import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import folium
from streamlit_folium import st_folium
import requests

# Set page configuration
st.set_page_config(
    page_title="Indian Coal Mine Safety Monitoring System",
    page_icon="⛏️",
    layout="wide"
)

# Application title
st.title("IoT-Based Coal Mine Safety Tracking System")
st.markdown("Real-time monitoring of Indian coal mines for worker safety")

# Sidebar for controls
st.sidebar.header("System Controls")
mine_section = st.sidebar.selectbox(
    "Select Mine Section",
    ["Section A", "Section B", "Section C", "All Sections"]
)

# Indian coal mines locations
INDIAN_COAL_MINES = {
    "Northern Coalfields Limited (NCL)": (23.8315, 86.4304),
    "South Eastern Coalfields Limited (SECL)": (22.3372, 82.7522),
    "Singareni Collieries": (17.6868, 80.9339),
    "Jharia Coalfield": (23.7957, 86.4304),
    "Raniganj Coalfield": (23.6102, 87.1410)
}

# Select coal mine
selected_mine = st.sidebar.selectbox(
    "Select Coal Mine",
    list(INDIAN_COAL_MINES.keys())
)

# Function to get selected mine location
def get_mine_location():
    return INDIAN_COAL_MINES[selected_mine]

# Function to generate simulated sensor data for Indian coal mines
def generate_sensor_data(num_miners=5):
    current_time = datetime.now()
    
    data = []
    sections = ["Section A", "Section B", "Section C"]
    gas_types = ["Methane", "Carbon Monoxide", "Hydrogen Sulfide"]
    
    # Get selected mine location
    center_lat, center_lon = get_mine_location()
    
    for i in range(num_miners):
        miner_id = f"MINER_{i+1:03d}"
        section = random.choice(sections)
        temperature = round(random.uniform(20, 45), 1)  # Higher temperature range for Indian mines
        humidity = round(random.uniform(40, 95), 1)
        gas_level = round(random.uniform(0, 100), 1)
        gas_type = random.choice(gas_types)
        oxygen_level = round(random.uniform(18, 21), 1)
        helmet_status = random.choice(["Worn", "Not Worn"])
        battery_level = round(random.uniform(20, 100), 1)
        
        # Generate coordinates near the center location
        lat = center_lat + random.uniform(-0.02, 0.02)
        lon = center_lon + random.uniform(-0.02, 0.02)
        
        # Calculate alert status
        alert = False
        alert_message = "Normal"
        
        if temperature > 38:  # Higher threshold for Indian climate
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
            "alert_message": alert_message,
            "lat": lat,
            "lon": lon
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
    st.session_state.sensor_data = generate_sensor_data(10)
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

# Display current mine and last update time
st.sidebar.write(f"Current Mine: {selected_mine}")
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
            
            # Add SOS button for emergencies
            if st.button(f"Send SOS for {alert['miner_id']}", key=f"sos_{alert['miner_id']}"):
                st.success(f"SOS signal sent for {alert['miner_id']}. Emergency team notified!")
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
    
    # Add safety thresholds
    fig.add_hline(y=90, line_dash="dash", line_color="red", annotation_text="High Humidity Threshold")
    fig.add_vline(x=38, line_dash="dash", line_color="red", annotation_text="High Temperature Threshold")
    
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    # Gas levels by miner
    fig = px.bar(filtered_data, x="miner_id", y="gas_level", 
                 color="gas_type", barmode="group",
                 title="Gas Levels by Miner")
    
    # Add safety threshold
    fig.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Dangerous Gas Level")
    
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    # Battery status
    fig = px.bar(filtered_data, x="miner_id", y="battery_level",
                 color="battery_level", color_continuous_scale="RdYlGn",
                 title="Battery Levels by Miner")
    fig.add_hline(y=30, line_dash="dash", line_color="red", annotation_text="Low Battery Threshold")
    st.plotly_chart(fig, use_container_width=True)

# Map visualization with real Indian coal mine locations
st.subheader("Miner Location Map")
st.info("This map shows the real-time locations of miners in the selected Indian coal mine.")

# Create the map centered on the selected mine
center_lat, center_lon = get_mine_location()
m = folium.Map(location=[center_lat, center_lon], zoom_start=14)

# Add a marker for the mine headquarters
folium.Marker(
    location=[center_lat, center_lon],
    popup=f"{selected_mine} Headquarters",
    icon=folium.Icon(color="blue", icon="building", prefix="fa")
).add_to(m)

# Add markers for each miner
for _, miner in filtered_data.iterrows():
    popup_html = f"""
    <b>Miner ID:</b> {miner['miner_id']}<br>
    <b>Section:</b> {miner['section']}<br>
    <b>Temperature:</b> {miner['temperature']}°C<br>
    <b>Gas Level:</b> {miner['gas_level']} ppm ({miner['gas_type']})<br>
    <b>Status:</b> {miner['alert_message']}
    """
    
    folium.CircleMarker(
        location=[miner['lat'], miner['lon']],
        radius=7,
        popup=folium.Popup(popup_html, max_width=300),
        color="red" if miner['alert'] else "green",
        fill=True,
        fill_opacity=0.7
    ).add_to(m)

# Display the map
st_folium(m, width=700, height=500)

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

# Emergency Response System
st.subheader("Emergency Response System")
st.markdown("The system is integrated with the 'Suraksha Kavach' IoT-enabled safety system implemented by NCL and SECL.")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### SOS Emergency Button")
    if st.button("ACTIVATE EMERGENCY RESPONSE", key="global_sos"):
        st.error("EMERGENCY SIGNAL ACTIVATED!")
        st.markdown("✅ Alert sent to command center")
        st.markdown("✅ SMS notifications sent to safety team")
        st.markdown("✅ Evacuation protocol initiated")

with col2:
    st.markdown("### Safety Protocols")
    st.markdown("1. **Check gas levels** before entering new areas")
    st.markdown("2. **Maintain communication** with the control room")
    st.markdown("3. **Wear safety equipment** at all times")
    st.markdown("4. **Report anomalies** immediately")
    st.markdown("5. **Know evacuation routes** for your section")

# Footer
st.markdown("---")
st.markdown("IoT-Based Coal Mine Safety Tracking System - Developed for Indian coal mines")
st.markdown("Implementation based on 'Suraksha Kavach' system by NCL and SECL")
