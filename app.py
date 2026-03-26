# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(page_title="Energy Efficiency Dashboard", layout="wide")

st.title("🏠 AI Energy Efficiency Dashboard")
st.write("Interactive dashboard to monitor and optimize energy usage in rooms.")

# Load data
data = pd.read_csv("data.csv")  # Make sure data.csv is in the same folder

# Sidebar interactivity
st.sidebar.header("Filters")

# Select room
room = st.sidebar.selectbox("Choose a room", data['Room'].unique())

# Select appliance (optional)
appliances_in_room = data[data['Room']==room]['Appliance'].unique()
appliance = st.sidebar.selectbox("Choose appliance (optional)", ["All"] + list(appliances_in_room))

# Set efficiency threshold
threshold = st.sidebar.slider("Efficiency threshold (%)", 0, 100, 80)

# Filter data based on selection
if appliance == "All":
    filtered_data = data[data['Room']==room]
else:
    filtered_data = data[(data['Room']==room) & (data['Appliance']==appliance)]

# Compute efficiency score
used_energy = filtered_data['Used_kWh'].sum()
total_energy = filtered_data['Total_kWh'].sum()
if total_energy > 0:
    efficiency_score = round(100 * (1 - used_energy / total_energy), 2)
else:
    efficiency_score = 100.0

# Show efficiency score
st.metric("⚡ Efficiency Score (%)", efficiency_score)

# Actionable suggestions
if efficiency_score < threshold:
    st.warning(f"Room '{room}' is inefficient! Consider turning off unused appliances.")
else:
    st.success(f"Room '{room}' is efficient.")

# Show data table
st.subheader(f"Energy Data for {room}")
st.dataframe(filtered_data)

# Dynamic chart
st.subheader(f"Energy Usage Chart for {room}")
fig = px.bar(filtered_data, x='Appliance', y='Used_kWh', color='Used_kWh',
             title=f'Energy Consumption in {room}', labels={'Used_kWh':'Energy Used (kWh)'})
st.plotly_chart(fig, use_container_width=True)

