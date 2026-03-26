# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(page_title="Energy Efficiency Dashboard", layout="wide")
st.title("🏠 AI Energy Efficiency Dashboard")
st.write("Interactive dashboard to monitor and optimize energy usage in rooms.")

# --- Load CSV ---
data = pd.read_csv("data.csv")
data.columns = data.columns.str.strip()  # remove any spaces in column names

# Rename columns to match dashboard logic
data.rename(columns={'room':'Room', 'energy_usage':'Used_kWh'}, inplace=True)

# Compute Total_kWh as sum of light + AC usage (assuming 1 = ON, 0 = OFF)
data['Total_kWh'] = data['light'] + data['ac']

# --- Sidebar Filters ---
st.sidebar.header("Filters")

# Room selector
room = st.sidebar.selectbox("Choose a room", data['Room'].unique())

# Threshold slider for efficiency
threshold = st.sidebar.slider("Efficiency threshold (%)", 0, 100, 80)

# Filter data for the selected room
room_data = data[data['Room'] == room]

# --- Efficiency Calculation ---
used_energy = room_data['Used_kWh'].sum()
total_energy = room_data['Total_kWh'].sum()

if total_energy > 0:
    efficiency_score = round(100 * (1 - used_energy / total_energy), 2)
else:
    efficiency_score = 100.0

# Display efficiency score
st.metric("⚡ Efficiency Score (%)", efficiency_score)

# Actionable suggestion
if efficiency_score < threshold:
    st.warning(f"Room '{room}' is inefficient! Consider turning off unused lights or AC.")
else:
    st.success(f"Room '{room}' is efficient.")

# --- Show Data Table ---
st.subheader(f"Energy Data for {room}")
st.dataframe(room_data)

# --- Dynamic Chart ---
st.subheader(f"Energy Usage Chart for {room}")
# For the chart, show light, AC, and total energy usage per time step
chart_data = room_data[['time', 'light', 'ac', 'Used_kWh']].melt(id_vars='time', 
                                                                   var_name='Appliance', 
                                                                   value_name='Energy')
fig = px.bar(chart_data, x='time', y='Energy', color='Appliance', barmode='group',
             title=f"Energy Usage in {room} Over Time")
st.plotly_chart(fig, use_container_width=True)