

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LinearRegression
import plotly.express as px

st.title("🏢 AI Energy Intelligence Dashboard")

# Load data
data = pd.read_csv("data.csv")

st.subheader("📊 Raw Data")
st.write(data)

# -----------------------------
# Waste Detection
# -----------------------------
st.subheader("🚨 Energy Waste Detection")

data['waste'] = (data['occupancy'] == 0) & ((data['light'] == 1) | (data['ac'] == 1))

waste_rooms = data[data['waste'] == True]

st.write("Rooms wasting energy:")
st.write(waste_rooms)

# -----------------------------
# Anomaly Detection (AI)
# -----------------------------
st.subheader("🤖 AI Anomaly Detection")

model = IsolationForest()
data['anomaly'] = model.fit_predict(data[['energy_usage']])

st.write(data[['room', 'energy_usage', 'anomaly']])

# -----------------------------
# Prediction Model
# -----------------------------
st.subheader("📈 Energy Prediction")

X = data[['time']]
y = data['energy_usage']

reg = LinearRegression()
reg.fit(X, y)

future_time = np.array([[11], [12], [13]])
predictions = reg.predict(future_time)

pred_df = pd.DataFrame({
    "time": [11,12,13],
    "predicted_energy": predictions
})

st.write(pred_df)

# -----------------------------
# Visualization
# -----------------------------
st.subheader("📉 Energy Usage Graph")

fig = px.line(data, x='time', y='energy_usage', title="Energy Usage Over Time")
st.plotly_chart(fig)

# -----------------------------
# Efficiency Score
# -----------------------------
st.subheader("🌱 Efficiency Score")

total = len(data)
waste_count = len(waste_rooms)

score = 100 - (waste_count / total * 100)

