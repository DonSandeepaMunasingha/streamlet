import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import time

st.set_page_config(layout="wide")
st.title("📊 Live Process Monitoring")

# Initialize session state for data
if 'live_data' not in st.session_state:
    st.session_state.live_data = pd.DataFrame()

# Generate live data function
def generate_live_data_points(num_points=60):
    """Generate live data for visualization"""
    np.random.seed(int(time.time()))
    
    timestamps = [datetime.now() - timedelta(seconds=i) for i in range(num_points, -1, -1)]
    
    # Generate realistic extrusion data
    base_pressure = 48.7
    base_temp = 410
    base_speed = 0.5
    
    data = []
    for i, ts in enumerate(timestamps):
        # Add some trends and cycles
        trend = np.sin(i / 10) * 2
        cycle = np.sin(i / 5) * 1.5
        
        point = {
            'timestamp': ts,
            'ram_pressure': base_pressure + trend + np.random.randn() * 0.5,
            'billet_pressure': 224.5 + trend * 10 + np.random.randn() * 3,
            'front_temp': base_temp + cycle + np.random.randn() * 2,
            'back_temp': base_temp - 5 + cycle + np.random.randn() * 2,
            'oil_temp': 29.1 + np.random.randn() * 0.5,
            'ram_speed': max(0, base_speed + np.random.randn() * 0.3),
            'container_position': 450 + np.random.randn() * 1,
            'sys_pressure': 3.0 + np.random.randn() * 0.1,
            'pilot_pressure': 48.7 + np.random.randn() * 0.3
        }
        data.append(point)
    
    return pd.DataFrame(data)

# Update live data
st.session_state.live_data = generate_live_data_points()

# Control panel
st.sidebar.header("Monitoring Controls")
sample_rate = st.sidebar.selectbox("Sample Rate", ["1 sec", "5 sec", "10 sec", "30 sec"], index=1)
history_points = st.sidebar.slider("History Points", 30, 300, 120)
auto_update = st.sidebar.checkbox("Auto Update", value=True)

if st.sidebar.button("Refresh Data"):
    st.rerun()

# Display current values
st.subheader("Current Values")
col1, col2, col3, col4 = st.columns(4)
current = st.session_state.live_data.iloc[-1]

with col1:
    st.metric("RAM Pressure", f"{current['ram_pressure']:.1f}")
with col2:
    st.metric("Front Temp", f"{current['front_temp']:.1f}°C")
with col3:
    st.metric("RAM Speed", f"{current['ram_speed']:.1f} mm/s")
with col4:
    st.metric("Billet Pressure", f"{current['billet_pressure']:.1f}")

# Create tabs for different visualizations
tab1, tab2, tab3 = st.tabs(["Pressure Monitoring", "Temperature Monitoring", "Combined View"])

with tab1:
    st.subheader("Pressure Trends")
    
    fig_pressure = make_subplots(
        rows=2, cols=1,
        subplot_titles=('RAM & Billet Pressure', 'System Pressures'),
        vertical_spacing=0.15
    )
    
    # RAM and Billet Pressure
    fig_pressure.add_trace(
        go.Scatter(
            x=st.session_state.live_data['timestamp'],
            y=st.session_state.live_data['ram_pressure'],
            name='RAM Pressure',
            line=dict(color='blue', width=2),
            mode='lines'
        ),
        row=1, col=1
    )
    
    fig_pressure.add_trace(
        go.Scatter(
            x=st.session_state.live_data['timestamp'],
            y=st.session_state.live_data['billet_pressure'],
            name='Billet Pressure',
            line=dict(color='red', width=2),
            mode='lines',
            yaxis="y2"
        ),
        row=1, col=1
    )
    
    # System Pressures
    fig_pressure.add_trace(
        go.Scatter(
            x=st.session_state.live_data['timestamp'],
            y=st.session_state.live_data['sys_pressure'],
            name='System Pressure',
            line=dict(color='green', width=2),
            mode='lines'
        ),
        row=2, col=1
    )
    
    fig_pressure.add_trace(
        go.Scatter(
            x=st.session_state.live_data['timestamp'],
            y=st.session_state.live_data['pilot_pressure'],
            name='Pilot Pressure',
            line=dict(color='orange', width=2),
            mode='lines'
        ),
        row=2, col=1
    )
    
    fig_pressure.update_layout(
        height=600,
        showlegend=True,
        hovermode='x unified'
    )
    
    # Add range sliders
    fig_pressure.update_xaxes(rangeslider_visible=True, row=1, col=1)
    fig_pressure.update_xaxes(rangeslider_visible=True, row=2, col=1)
    
    st.plotly_chart(fig_pressure, use_container_width=True)

with tab2:
    st.subheader("Temperature Trends")
    
    fig_temp = go.Figure()
    
    fig_temp.add_trace(go.Scatter(
        x=st.session_state.live_data['timestamp'],
        y=st.session_state.live_data['front_temp'],
        name='Front Temperature',
        line=dict(color='red', width=2)
    ))
    
    fig_temp.add_trace(go.Scatter(
        x=st.session_state.live_data['timestamp'],
        y=st.session_state.live_data['back_temp'],
        name='Back Temperature',
        line=dict(color='orange', width=2)
    ))
    
    fig_temp.add_trace(go.Scatter(
        x=st.session_state.live_data['timestamp'],
        y=st.session_state.live_data['oil_temp'],
        name='Oil Temperature',
        line=dict(color='blue', width=2),
        yaxis="y2"
    ))
    
    fig_temp.update_layout(
        title="Temperature Monitoring",
        yaxis=dict(title="Container Temperature (°C)"),
        yaxis2=dict(
            title="Oil Temperature (°C)",
            overlaying="y",
            side="right"
        ),
        height=500,
        hovermode='x unified'
    )
    
    fig_temp.add_hline(y=420, line_dash="dash", line_color="red", 
                      annotation_text="Max Temp Limit", row=1, col=1)
    
    st.plotly_chart(fig_temp, use_container_width=True)

with tab3:
    st.subheader("Combined Process View")
    
    # Create gauge charts
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        fig_gauge1 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=current['ram_pressure'],
            title={'text': "RAM Pressure"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 40], 'color': "lightgray"},
                    {'range': [40, 80], 'color': "gray"},
                    {'range': [80, 100], 'color': "lightcoral"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        fig_gauge1.update_layout(height=250)
        st.plotly_chart(fig_gauge1, use_container_width=True)
    
    with col2:
        fig_gauge2 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=current['front_temp'],
            title={'text': "Front Temp"},
            gauge={
                'axis': {'range': [350, 450]},
                'bar': {'color': "darkred"},
                'steps': [
                    {'range': [350, 400], 'color': "lightblue"},
                    {'range': [400, 420], 'color': "lightgreen"},
                    {'range': [420, 450], 'color': "lightcoral"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 420
                }
            }
        ))
        fig_gauge2.update_layout(height=250)
        st.plotly_chart(fig_gauge2, use_container_width=True)
    
    with col3:
        fig_gauge3 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=current['billet_pressure'],
            title={'text': "Billet Pressure"},
            gauge={
                'axis': {'range': [0, 300]},
                'bar': {'color': "darkgreen"},
                'steps': [
                    {'range': [0, 150], 'color': "lightgray"},
                    {'range': [150, 250], 'color': "lightyellow"},
                    {'range': [250, 300], 'color': "lightcoral"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 250
                }
            }
        ))
        fig_gauge3.update_layout(height=250)
        st.plotly_chart(fig_gauge3, use_container_width=True)
    
    with col4:
        fig_gauge4 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=current['ram_speed'],
            title={'text': "RAM Speed"},
            gauge={
                'axis': {'range': [0, 10]},
                'bar': {'color': "purple"},
                'steps': [
                    {'range': [0, 5], 'color': "lightgreen"},
                    {'range': [5, 8], 'color': "lightyellow"},
                    {'range': [8, 10], 'color': "lightcoral"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 8
                }
            }
        ))
        fig_gauge4.update_layout(height=250)
        st.plotly_chart(fig_gauge4, use_container_width=True)
    
    # Recent data table
    st.subheader("Recent Data Points")
    display_data = st.session_state.live_data.tail(20).copy()
    display_data['timestamp'] = display_data['timestamp'].dt.strftime('%H:%M:%S')
    st.dataframe(display_data.set_index('timestamp'), use_container_width=True)

# Auto-refresh
if auto_update:
    time.sleep(5)
    st.rerun()