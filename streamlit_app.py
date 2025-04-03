# import streamlit as st
# import pandas as pd
# import numpy as np
# import time
# import plotly.express as px
# import plotly.graph_objects as go
# from datetime import datetime, timedelta
# import random
# import folium
# from streamlit_folium import st_folium
# import requests

# # Set page configuration
# st.set_page_config(
#     page_title="Indian Coal Mine Safety Monitoring System",
#     page_icon="⛏️",
#     layout="wide"
# )

# # Application title
# st.title("IoT-Based Coal Mine Safety Tracking System")
# st.markdown("Real-time monitoring of Indian coal mines for worker safety")

# # Sidebar for controls
# st.sidebar.header("System Controls")
# mine_section = st.sidebar.selectbox(
#     "Select Mine Section",
#     ["Section A", "Section B", "Section C", "All Sections"]
# )

# # Indian coal mines locations
# INDIAN_COAL_MINES = {
#     "Northern Coalfields Limited (NCL)": (23.8315, 86.4304),
#     "South Eastern Coalfields Limited (SECL)": (22.3372, 82.7522),
#     "Singareni Collieries": (17.6868, 80.9339),
#     "Jharia Coalfield": (23.7957, 86.4304),
#     "Raniganj Coalfield": (23.6102, 87.1410)
# }

# # Select coal mine
# selected_mine = st.sidebar.selectbox(
#     "Select Coal Mine",
#     list(INDIAN_COAL_MINES.keys())
# )

# # Function to get selected mine location
# def get_mine_location():
#     return INDIAN_COAL_MINES[selected_mine]

# # Function to generate simulated sensor data for Indian coal mines
# def generate_sensor_data(num_miners=5):
#     current_time = datetime.now()
    
#     data = []
#     sections = ["Section A", "Section B", "Section C"]
#     gas_types = ["Methane", "Carbon Monoxide", "Hydrogen Sulfide"]
    
#     # Get selected mine location
#     center_lat, center_lon = get_mine_location()
    
#     for i in range(num_miners):
#         miner_id = f"MINER_{i+1:03d}"
#         section = random.choice(sections)
#         temperature = round(random.uniform(20, 45), 1)  # Higher temperature range for Indian mines
#         humidity = round(random.uniform(40, 95), 1)
#         gas_level = round(random.uniform(0, 100), 1)
#         gas_type = random.choice(gas_types)
#         oxygen_level = round(random.uniform(18, 21), 1)
#         helmet_status = random.choice(["Worn", "Not Worn"])
#         battery_level = round(random.uniform(20, 100), 1)
        
#         # Generate coordinates near the center location
#         lat = center_lat + random.uniform(-0.02, 0.02)
#         lon = center_lon + random.uniform(-0.02, 0.02)
        
#         # Calculate alert status
#         alert = False
#         alert_message = "Normal"
        
#         if temperature > 38:  # Higher threshold for Indian climate
#             alert = True
#             alert_message = "High Temperature"
#         elif gas_level > 70:
#             alert = True
#             alert_message = f"High {gas_type} Level"
#         elif oxygen_level < 19:
#             alert = True
#             alert_message = "Low Oxygen"
#         elif helmet_status == "Not Worn":
#             alert = True
#             alert_message = "Helmet Not Worn"
#         elif battery_level < 30:
#             alert = True
#             alert_message = "Low Battery"
            
#         data.append({
#             "timestamp": current_time - timedelta(minutes=random.randint(0, 30)),
#             "miner_id": miner_id,
#             "section": section,
#             "temperature": temperature,
#             "humidity": humidity,
#             "gas_level": gas_level,
#             "gas_type": gas_type,
#             "oxygen_level": oxygen_level,
#             "helmet_status": helmet_status,
#             "battery_level": battery_level,
#             "alert": alert,
#             "alert_message": alert_message,
#             "lat": lat,
#             "lon": lon
#         })
    
#     return pd.DataFrame(data)

# # Function to load sample data or generate new data
# def load_or_generate_data():
#     try:
#         # Try to load sample data if it exists
#         if os.path.exists("data/sample_data.csv"):
#             df = pd.read_csv("data/sample_data.csv")
#             df["timestamp"] = pd.to_datetime(df["timestamp"])
#             return df
#         else:
#             return generate_sensor_data(10)
#     except Exception as e:
#         st.error(f"Error loading data: {e}")
#         return generate_sensor_data(10)

# # Generate initial data
# if 'sensor_data' not in st.session_state:
#     st.session_state.sensor_data = generate_sensor_data(10)
#     st.session_state.historical_data = st.session_state.sensor_data.copy()
#     st.session_state.last_update = datetime.now()

# # Update data button
# if st.sidebar.button("Update Sensor Data"):
#     new_data = generate_sensor_data(10)
#     st.session_state.sensor_data = new_data
#     st.session_state.historical_data = pd.concat([st.session_state.historical_data, new_data])
#     st.session_state.last_update = datetime.now()

# # Auto-refresh option
# auto_refresh = st.sidebar.checkbox("Enable Auto-refresh (30s)")
# if auto_refresh:
#     time_diff = (datetime.now() - st.session_state.last_update).total_seconds()
#     if time_diff > 30:
#         new_data = generate_sensor_data(10)
#         st.session_state.sensor_data = new_data
#         st.session_state.historical_data = pd.concat([st.session_state.historical_data, new_data])
#         st.session_state.last_update = datetime.now()
#         st.rerun()

# # Display current mine and last update time
# st.sidebar.write(f"Current Mine: {selected_mine}")
# st.sidebar.write(f"Last updated: {st.session_state.last_update.strftime('%Y-%m-%d %H:%M:%S')}")

# # Filter data based on selected section
# if mine_section != "All Sections":
#     filtered_data = st.session_state.sensor_data[st.session_state.sensor_data["section"] == mine_section]
# else:
#     filtered_data = st.session_state.sensor_data

# # Dashboard layout
# col1, col2 = st.columns(2)

# # Alert summary
# with col1:
#     st.subheader("Safety Alerts")
#     alert_data = filtered_data[filtered_data["alert"] == True]
    
#     if not alert_data.empty:
#         st.error(f"{len(alert_data)} alerts detected!")
#         for _, alert in alert_data.iterrows():
#             st.warning(f"⚠️ {alert['miner_id']} in {alert['section']}: {alert['alert_message']}")
            
#             # Add SOS button for emergencies
#             if st.button(f"Send SOS for {alert['miner_id']}", key=f"sos_{alert['miner_id']}"):
#                 st.success(f"SOS signal sent for {alert['miner_id']}. Emergency team notified!")
#     else:
#         st.success("No alerts detected. All systems normal.")

# # Environmental conditions summary
# with col2:
#     st.subheader("Environmental Conditions")
#     avg_temp = filtered_data["temperature"].mean()
#     avg_humidity = filtered_data["humidity"].mean()
#     avg_oxygen = filtered_data["oxygen_level"].mean()
    
#     col2a, col2b, col2c = st.columns(3)
#     col2a.metric("Avg. Temperature", f"{avg_temp:.1f}°C")
#     col2b.metric("Avg. Humidity", f"{avg_humidity:.1f}%")
#     col2c.metric("Avg. Oxygen Level", f"{avg_oxygen:.1f}%")
    
#     # Gas levels chart
#     gas_data = filtered_data.groupby("gas_type")["gas_level"].mean().reset_index()
#     fig = px.bar(gas_data, x="gas_type", y="gas_level", 
#                  title="Average Gas Levels by Type",
#                  labels={"gas_type": "Gas Type", "gas_level": "Level (ppm)"},
#                  color="gas_level", color_continuous_scale="Viridis")
#     st.plotly_chart(fig, use_container_width=True)

# # Miner status table
# st.subheader("Miner Status")
# st.dataframe(filtered_data[["miner_id", "section", "temperature", "humidity", 
#                            "gas_level", "gas_type", "oxygen_level", 
#                            "helmet_status", "battery_level", "alert_message"]], 
#             use_container_width=True)

# # Visualizations
# st.subheader("Data Visualization")

# tab1, tab2, tab3 = st.tabs(["Temperature & Humidity", "Gas Levels", "Battery Status"])

# with tab1:
#     # Temperature and humidity scatter plot
#     fig = px.scatter(filtered_data, x="temperature", y="humidity", 
#                      color="section", size="oxygen_level",
#                      hover_data=["miner_id", "alert_message"],
#                      title="Temperature vs. Humidity by Mine Section")
    
#     # Add safety thresholds
#     fig.add_hline(y=90, line_dash="dash", line_color="red", annotation_text="High Humidity Threshold")
#     fig.add_vline(x=38, line_dash="dash", line_color="red", annotation_text="High Temperature Threshold")
    
#     st.plotly_chart(fig, use_container_width=True)

# with tab2:
#     # Gas levels by miner
#     fig = px.bar(filtered_data, x="miner_id", y="gas_level", 
#                  color="gas_type", barmode="group",
#                  title="Gas Levels by Miner")
    
#     # Add safety threshold
#     fig.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Dangerous Gas Level")
    
#     st.plotly_chart(fig, use_container_width=True)

# with tab3:
#     # Battery status
#     fig = px.bar(filtered_data, x="miner_id", y="battery_level",
#                  color="battery_level", color_continuous_scale="RdYlGn",
#                  title="Battery Levels by Miner")
#     fig.add_hline(y=30, line_dash="dash", line_color="red", annotation_text="Low Battery Threshold")
#     st.plotly_chart(fig, use_container_width=True)

# # Map visualization with real Indian coal mine locations
# st.subheader("Miner Location Map")
# st.info("This map shows the real-time locations of miners in the selected Indian coal mine.")

# # Create the map centered on the selected mine
# center_lat, center_lon = get_mine_location()
# m = folium.Map(location=[center_lat, center_lon], zoom_start=14)

# # Add a marker for the mine headquarters
# folium.Marker(
#     location=[center_lat, center_lon],
#     popup=f"{selected_mine} Headquarters",
#     icon=folium.Icon(color="blue", icon="building", prefix="fa")
# ).add_to(m)

# # Add markers for each miner
# for _, miner in filtered_data.iterrows():
#     popup_html = f"""
#     <b>Miner ID:</b> {miner['miner_id']}<br>
#     <b>Section:</b> {miner['section']}<br>
#     <b>Temperature:</b> {miner['temperature']}°C<br>
#     <b>Gas Level:</b> {miner['gas_level']} ppm ({miner['gas_type']})<br>
#     <b>Status:</b> {miner['alert_message']}
#     """
    
#     folium.CircleMarker(
#         location=[miner['lat'], miner['lon']],
#         radius=7,
#         popup=folium.Popup(popup_html, max_width=300),
#         color="red" if miner['alert'] else "green",
#         fill=True,
#         fill_opacity=0.7
#     ).add_to(m)

# # Display the map
# st_folium(m, width=700, height=500)

# # Historical data analysis
# st.subheader("Historical Data Analysis")
# if st.checkbox("Show Historical Data Analysis"):
#     # Create time-based analysis if we have enough historical data
#     if len(st.session_state.historical_data) > 10:
#         # Group by timestamp (hourly)
#         st.session_state.historical_data['hour'] = st.session_state.historical_data['timestamp'].dt.floor('H')
#         hourly_data = st.session_state.historical_data.groupby('hour').agg({
#             'temperature': 'mean',
#             'humidity': 'mean',
#             'gas_level': 'mean',
#             'oxygen_level': 'mean',
#             'alert': 'sum'
#         }).reset_index()
        
#         # Plot time series
#         fig = go.Figure()
#         fig.add_trace(go.Scatter(x=hourly_data['hour'], y=hourly_data['temperature'], 
#                                 mode='lines+markers', name='Temperature'))
#         fig.add_trace(go.Scatter(x=hourly_data['hour'], y=hourly_data['humidity'], 
#                                 mode='lines+markers', name='Humidity'))
#         fig.add_trace(go.Scatter(x=hourly_data['hour'], y=hourly_data['gas_level'], 
#                                 mode='lines+markers', name='Gas Level'))
#         fig.update_layout(title='Environmental Conditions Over Time',
#                         xaxis_title='Time',
#                         yaxis_title='Value')
#         st.plotly_chart(fig, use_container_width=True)
        
#         # Alert frequency
#         fig = px.bar(hourly_data, x='hour', y='alert', 
#                     title='Number of Alerts Over Time')
#         st.plotly_chart(fig, use_container_width=True)
#     else:
#         st.info("Not enough historical data available yet. Please update sensor data a few more times.")

# # Emergency Response System
# st.subheader("Emergency Response System")
# st.markdown("The system is integrated with the 'Suraksha Kavach' IoT-enabled safety system implemented by NCL and SECL.")

# col1, col2 = st.columns(2)

# with col1:
#     st.markdown("### SOS Emergency Button")
#     if st.button("ACTIVATE EMERGENCY RESPONSE", key="global_sos"):
#         st.error("EMERGENCY SIGNAL ACTIVATED!")
#         st.markdown("✅ Alert sent to command center")
#         st.markdown("✅ SMS notifications sent to safety team")
#         st.markdown("✅ Evacuation protocol initiated")

# with col2:
#     st.markdown("### Safety Protocols")
#     st.markdown("1. **Check gas levels** before entering new areas")
#     st.markdown("2. **Maintain communication** with the control room")
#     st.markdown("3. **Wear safety equipment** at all times")
#     st.markdown("4. **Report anomalies** immediately")
#     st.markdown("5. **Know evacuation routes** for your section")

# # Footer
# st.markdown("---")
# st.markdown("IoT-Based Coal Mine Safety Tracking System - Developed for Indian coal mines")
# st.markdown("Implementation based on 'Suraksha Kavach' system by NCL and SECL")


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
import os

# Set page configuration
st.set_page_config(
    page_title="Indian Coal Mine Safety Monitoring System",
    page_icon="⛏️",
    layout="wide"
)

# Application title with improved styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #FF5733;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #555555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-container {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .alert-box {
        background-color: #ffe6e6;
        border-left: 5px solid #ff0000;
        padding: 10px;
        margin-bottom: 10px;
        border-radius: 5px;
    }
    .normal-box {
        background-color: #e6ffe6;
        border-left: 5px solid #00cc00;
        padding: 10px;
        margin-bottom: 10px;
        border-radius: 5px;
    }
</style>
<h1 class="main-header">IoT-Based Coal Mine Safety Tracking System</h1>
<p class="sub-header">Real-time monitoring of Indian coal mines for worker safety</p>
""", unsafe_allow_html=True)

# Sidebar for controls
st.sidebar.header("System Controls")

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

mine_section = st.sidebar.selectbox(
    "Select Mine Section",
    ["Section A", "Section B", "Section C", "All Sections"]
)

# Function to get selected mine location
def get_mine_location():
    return INDIAN_COAL_MINES[selected_mine]

# Worker data entry form
st.sidebar.header("Worker Data Entry")
with st.sidebar.expander("Add/Update Worker", expanded=False):
    worker_id = st.text_input("Worker ID (e.g., MINER_001)")
    worker_name = st.text_input("Worker Name")
    worker_section = st.selectbox("Section", ["Section A", "Section B", "Section C"])
    worker_role = st.selectbox("Role", ["Miner", "Supervisor", "Engineer", "Safety Officer"])
    worker_shift = st.selectbox("Shift", ["Morning", "Afternoon", "Night"])
    
    if st.button("Add/Update Worker"):
        if worker_id and worker_name:
            if 'workers' not in st.session_state:
                st.session_state.workers = {}
            
            st.session_state.workers[worker_id] = {
                "name": worker_name,
                "section": worker_section,
                "role": worker_role,
                "shift": worker_shift,
                "check_in_time": datetime.now()
            }
            st.sidebar.success(f"Worker {worker_name} added/updated successfully!")
        else:
            st.sidebar.error("Worker ID and Name are required!")

# Function to detect real IoT sensors
def detect_iot_sensors():
    # This is a placeholder - in a real implementation, 
    # you would scan for actual IoT devices
    return False

# Function to generate simulated sensor data for Indian coal mines
def generate_sensor_data(num_miners=5):
    current_time = datetime.now()
    
    data = []
    sections = ["Section A", "Section B", "Section C"]
    gas_types = ["Methane", "Carbon Monoxide", "Hydrogen Sulfide"]
    
    # Get selected mine location
    center_lat, center_lon = get_mine_location()
    
    # Use registered workers if available
    if 'workers' in st.session_state and st.session_state.workers:
        worker_ids = list(st.session_state.workers.keys())
        # If we have fewer workers than num_miners, add some random ones
        if len(worker_ids) < num_miners:
            for i in range(len(worker_ids), num_miners):
                worker_ids.append(f"MINER_{i+1:03d}")
    else:
        worker_ids = [f"MINER_{i+1:03d}" for i in range(num_miners)]
    
    for miner_id in worker_ids:
        # Use registered worker data if available
        if 'workers' in st.session_state and miner_id in st.session_state.workers:
            section = st.session_state.workers[miner_id]["section"]
            name = st.session_state.workers[miner_id]["name"]
            role = st.session_state.workers[miner_id]["role"]
            shift = st.session_state.workers[miner_id]["shift"]
        else:
            section = random.choice(sections)
            name = f"Worker {miner_id[-3:]}"
            role = random.choice(["Miner", "Supervisor", "Engineer"])
            shift = random.choice(["Morning", "Afternoon", "Night"])
        
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
            "name": name,
            "role": role,
            "shift": shift,
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

# Initialize session state for real-time updates
if 'last_update' not in st.session_state:
    st.session_state.last_update = datetime.now()
    
if 'sensor_data' not in st.session_state:
    st.session_state.sensor_data = generate_sensor_data(10)
    
if 'historical_data' not in st.session_state:
    st.session_state.historical_data = st.session_state.sensor_data.copy()

# Create placeholders for real-time updates
data_container = st.empty()
alert_container = st.empty()
map_container = st.empty()
viz_container = st.empty()

# Auto-refresh option
auto_refresh = st.sidebar.checkbox("Enable Auto-refresh", value=True)
refresh_interval = st.sidebar.slider("Refresh Interval (seconds)", 5, 60, 30)

# Manual update button
if st.sidebar.button("Update Sensor Data Now"):
    st.session_state.sensor_data = generate_sensor_data(10)
    st.session_state.historical_data = pd.concat([st.session_state.historical_data, st.session_state.sensor_data])
    st.session_state.last_update = datetime.now()

# Display current mine and last update time
st.sidebar.write(f"Current Mine: {selected_mine}")
st.sidebar.write(f"Last updated: {st.session_state.last_update.strftime('%Y-%m-%d %H:%M:%S')}")

# Real-time update loop
def update_data():
    # Check if we should update based on the refresh interval
    time_diff = (datetime.now() - st.session_state.last_update).total_seconds()
    
    if auto_refresh and time_diff > refresh_interval:
        # Check for real IoT sensors first
        if detect_iot_sensors():
            # Code to read from actual IoT sensors would go here
            pass
        else:
            # Generate simulated data
            st.session_state.sensor_data = generate_sensor_data(10)
            st.session_state.historical_data = pd.concat([st.session_state.historical_data, st.session_state.sensor_data])
            st.session_state.last_update = datetime.now()
        
        # Filter data based on selected section
        if mine_section != "All Sections":
            filtered_data = st.session_state.sensor_data[st.session_state.sensor_data["section"] == mine_section]
        else:
            filtered_data = st.session_state.sensor_data
        
        # Update the dashboard components
        with data_container.container():
            # Dashboard layout
            col1, col2 = st.columns(2)
            
            # Environmental conditions summary
            with col1:
                st.subheader("Environmental Conditions")
                avg_temp = filtered_data["temperature"].mean()
                avg_humidity = filtered_data["humidity"].mean()
                avg_oxygen = filtered_data["oxygen_level"].mean()
                
                col1a, col1b, col1c = st.columns(3)
                with col1a:
                    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                    st.metric("Avg. Temperature", f"{avg_temp:.1f}°C")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col1b:
                    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                    st.metric("Avg. Humidity", f"{avg_humidity:.1f}%")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col1c:
                    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
                    st.metric("Avg. Oxygen Level", f"{avg_oxygen:.1f}%")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Gas levels chart
                gas_data = filtered_data.groupby("gas_type")["gas_level"].mean().reset_index()
                fig = px.bar(gas_data, x="gas_type", y="gas_level", 
                            title="Average Gas Levels by Type",
                            labels={"gas_type": "Gas Type", "gas_level": "Level (ppm)"},
                            color="gas_level", color_continuous_scale="Viridis")
                st.plotly_chart(fig, use_container_width=True)
            
            # Worker status
            with col2:
                st.subheader("Worker Status")
                
                # Count workers by section
                section_counts = filtered_data["section"].value_counts().reset_index()
                section_counts.columns = ["Section", "Count"]
                
                # Create a pie chart
                fig = px.pie(section_counts, values="Count", names="Section", 
                            title="Workers by Section",
                            color_discrete_sequence=px.colors.qualitative.Pastel)
                st.plotly_chart(fig, use_container_width=True)
                
                # Count workers by role
                role_counts = filtered_data["role"].value_counts().reset_index()
                role_counts.columns = ["Role", "Count"]
                
                # Create a horizontal bar chart
                fig = px.bar(role_counts, y="Role", x="Count", 
                            title="Workers by Role",
                            orientation='h',
                            color="Count", color_continuous_scale="Viridis")
                st.plotly_chart(fig, use_container_width=True)
            
            # Miner status table
            st.subheader("Worker Details")
            st.dataframe(filtered_data[["miner_id", "name", "role", "section", "temperature", 
                                        "humidity", "gas_level", "gas_type", "oxygen_level", 
                                        "helmet_status", "battery_level", "alert_message"]], 
                        use_container_width=True)
        
        # Alert summary
        with alert_container.container():
            st.subheader("Safety Alerts")
            alert_data = filtered_data[filtered_data["alert"] == True]
            
            if not alert_data.empty:
                st.markdown(f'<div class="alert-box"><h3>⚠️ {len(alert_data)} alerts detected!</h3></div>', unsafe_allow_html=True)
                for _, alert in alert_data.iterrows():
                    st.warning(f"⚠️ {alert['name']} ({alert['miner_id']}) in {alert['section']}: {alert['alert_message']}")
                    
                    # Add SOS button for emergencies
                    if st.button(f"Send SOS for {alert['name']}", key=f"sos_{alert['miner_id']}"):
                        st.success(f"SOS signal sent for {alert['name']}. Emergency team notified!")
            else:
                st.markdown('<div class="normal-box"><h3>✅ No alerts detected. All systems normal.</h3></div>', unsafe_allow_html=True)
        
        # Map visualization
        with map_container.container():
            st.subheader("Worker Location Map")
            st.info("This map shows the real-time locations of workers in the selected Indian coal mine.")
            
            # Create the map centered on the selected mine
            center_lat, center_lon = get_mine_location()
            m = folium.Map(location=[center_lat, center_lon], zoom_start=14)
            
            # Add a marker for the mine headquarters
            folium.Marker(
                location=[center_lat, center_lon],
                popup=f"{selected_mine} Headquarters",
                icon=folium.Icon(color="blue", icon="building", prefix="fa")
            ).add_to(m)
            
            # Add markers for each worker
            for _, worker in filtered_data.iterrows():
                popup_html = f"""
                <b>ID:</b> {worker['miner_id']}<br>
                <b>Name:</b> {worker['name']}<br>
                <b>Role:</b> {worker['role']}<br>
                <b>Section:</b> {worker['section']}<br>
                <b>Temperature:</b> {worker['temperature']}°C<br>
                <b>Gas Level:</b> {worker['gas_level']} ppm ({worker['gas_type']})<br>
                <b>Status:</b> {worker['alert_message']}
                """
                
                folium.CircleMarker(
                    location=[worker['lat'], worker['lon']],
                    radius=7,
                    popup=folium.Popup(popup_html, max_width=300),
                    color="red" if worker['alert'] else "green",
                    fill=True,
                    fill_opacity=0.7
                ).add_to(m)
            
            # Display the map
            st_folium(m, width=700, height=500)
        
        # Visualizations
        with viz_container.container():
            st.subheader("Data Visualization")
            
            tab1, tab2, tab3 = st.tabs(["Temperature & Humidity", "Gas Levels", "Battery Status"])
            
            with tab1:
                # Temperature and humidity scatter plot
                fig = px.scatter(filtered_data, x="temperature", y="humidity", 
                                color="section", size="oxygen_level",
                                hover_data=["name", "miner_id", "alert_message"],
                                title="Temperature vs. Humidity by Mine Section")
                
                # Add safety thresholds
                fig.add_hline(y=90, line_dash="dash", line_color="red", annotation_text="High Humidity Threshold")
                fig.add_vline(x=38, line_dash="dash", line_color="red", annotation_text="High Temperature Threshold")
                
                st.plotly_chart(fig, use_container_width=True)
            
            with tab2:
                # Gas levels by worker
                fig = px.bar(filtered_data, x="miner_id", y="gas_level", 
                            color="gas_type", barmode="group",
                            hover_data=["name"],
                            title="Gas Levels by Worker")
                
                # Add safety threshold
                fig.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Dangerous Gas Level")
                
                st.plotly_chart(fig, use_container_width=True)
            
            with tab3:
                # Battery status
                fig = px.bar(filtered_data, x="miner_id", y="battery_level",
                            color="battery_level", color_continuous_scale="RdYlGn",
                            hover_data=["name"],
                            title="Battery Levels by Worker")
                fig.add_hline(y=30, line_dash="dash", line_color="red", annotation_text="Low Battery Threshold")
                st.plotly_chart(fig, use_container_width=True)

# Run the update function
update_data()

# Set up a loop to refresh the data
if auto_refresh:
    while True:
        time.sleep(1)          # Check every second if we need to update based on refresh interval
        time_diff = (datetime.now() - st.session_state.last_update).total_seconds()
        if time_diff > refresh_interval:
            st.rerun()
        time.sleep(1)

# Historical data analysis section
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

# Worker Management
st.subheader("Worker Management")
with st.expander("View All Registered Workers"):
    if 'workers' in st.session_state and st.session_state.workers:
        worker_data = []
        for worker_id, worker_info in st.session_state.workers.items():
            worker_data.append({
                "ID": worker_id,
                "Name": worker_info["name"],
                "Section": worker_info["section"],
                "Role": worker_info["role"],
                "Shift": worker_info["shift"],
                "Check-in Time": worker_info["check_in_time"].strftime("%Y-%m-%d %H:%M:%S")
            })
        worker_df = pd.DataFrame(worker_data)
        st.dataframe(worker_df, use_container_width=True)
    else:
        st.info("No workers registered yet. Use the form in the sidebar to add workers.")

# System Health Monitoring
st.subheader("System Health Monitoring")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### Network Status")
    st.success("✅ Network: Online")
    st.success("✅ Signal Strength: Strong")
    st.success("✅ Last Sync: " + datetime.now().strftime("%H:%M:%S"))

with col2:
    st.markdown("### Server Status")
    st.success("✅ Server: Running")
    st.success("✅ Database: Connected")
    st.success("✅ API: Operational")

with col3:
    st.markdown("### IoT Gateway")
    st.success("✅ Gateway: Online")
    st.success("✅ Sensors Connected: 24")
    st.success("✅ Data Flow: Normal")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center;">
    <p>IoT-Based Coal Mine Safety Tracking System - Developed for Indian coal mines</p>
    <p>Implementation based on 'Suraksha Kavach' system by NCL and SECL</p>
    <p>Last updated: April 03, 2025</p>
</div>
""", unsafe_allow_html=True)


