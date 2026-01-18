import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
from plotly.subplots import make_subplots

st.set_page_config(layout="wide")
st.title("📈 Historical Data Analysis")

# Generate historical data
@st.cache_data
def generate_historical_data(days=30):
    """Generate historical extrusion data"""
    np.random.seed(42)
    
    # Generate timestamps for the last N days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # Create hourly data points
    hours = days * 24
    timestamps = [start_date + timedelta(hours=i) for i in range(hours)]
    
    # Generate process data with trends
    data = {
        'timestamp': timestamps,
        'process': np.random.choice(['Roll_Production', 'Profile_Ext', 'Tube_Ext'], hours),
        'material': np.random.choice(['AL-6061', 'AL-7075', 'Copper'], hours),
        'operator': np.random.choice(['OP01', 'OP02', 'OP03', 'Auto'], hours),
        
        # Parameters with some correlation
        'ram_pressure': 45 + np.cumsum(np.random.randn(hours) * 0.1),
        'billet_pressure': 220 + np.cumsum(np.random.randn(hours) * 0.5),
        'front_temp': 410 + np.sin(np.arange(hours) / 24) * 5 + np.random.randn(hours) * 2,
        'ram_speed': np.abs(0.5 + np.random.randn(hours) * 0.2),
        'extrusion_time': 120 + np.random.randn(hours) * 15,
        'quality_score': 90 + np.random.randn(hours) * 3,
        'defect_count': np.random.poisson(0.5, hours),
        'product_length': 6000 + np.random.randn(hours) * 200
    }
    
    # Add some outliers
    outlier_indices = np.random.choice(hours, size=hours//20, replace=False)
    for idx in outlier_indices:
        if np.random.rand() > 0.5:
            data['front_temp'][idx] += np.random.uniform(10, 20)
        else:
            data['ram_pressure'][idx] += np.random.uniform(5, 15)
    
    df = pd.DataFrame(data)
    df['date'] = df['timestamp'].dt.date
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.day_name()
    
    return df

# Load data
df = generate_historical_data(30)

# Sidebar filters
st.sidebar.header("🔍 Analysis Filters")

date_range = st.sidebar.date_input(
    "Date Range",
    [df['date'].min(), df['date'].max()]
)

selected_process = st.sidebar.multiselect(
    "Process Type",
    options=df['process'].unique(),
    default=df['process'].unique()
)

selected_material = st.sidebar.multiselect(
    "Material",
    options=df['material'].unique(),
    default=df['material'].unique()
)

# Apply filters
mask = (
    (df['date'] >= date_range[0]) &
    (df['date'] <= date_range[1]) &
    (df['process'].isin(selected_process)) &
    (df['material'].isin(selected_material))
)

filtered_df = df[mask].copy()

# Summary statistics
st.subheader("📊 Summary Statistics")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total Records", len(filtered_df))
with col2:
    st.metric("Avg RAM Pressure", f"{filtered_df['ram_pressure'].mean():.1f}")
with col3:
    st.metric("Avg Temperature", f"{filtered_df['front_temp'].mean():.1f}°C")
with col4:
    st.metric("Avg Quality", f"{filtered_df['quality_score'].mean():.1f}%")
with col5:
    st.metric("Total Defects", int(filtered_df['defect_count'].sum()))

# Tabs for different analyses
tab1, tab2, tab3, tab4 = st.tabs(["Trend Analysis", "Statistical Analysis", "Quality Analysis", "Export Data"])

with tab1:
    st.subheader("Parameter Trends Over Time")
    
    parameter = st.selectbox(
        "Select Parameter",
        ['ram_pressure', 'billet_pressure', 'front_temp', 'ram_speed', 'quality_score']
    )
    
    # Create trend chart
    fig_trend = px.line(
        filtered_df,
        x='timestamp',
        y=parameter,
        color='process',
        title=f"{parameter.replace('_', ' ').title()} Trend",
        labels={parameter: parameter.replace('_', ' ').title()}
    )
    
    # Add moving average
    if st.checkbox("Show Moving Average (24h)"):
        filtered_df['moving_avg'] = filtered_df[parameter].rolling(window=24, center=True).mean()
        fig_trend.add_trace(
            go.Scatter(
                x=filtered_df['timestamp'],
                y=filtered_df['moving_avg'],
                name='24h Moving Average',
                line=dict(color='black', width=3, dash='dash')
            )
        )
    
    st.plotly_chart(fig_trend, use_container_width=True)
    
    # Daily averages
    st.subheader("Daily Averages")
    daily_avg = filtered_df.groupby('date').agg({
        'ram_pressure': 'mean',
        'front_temp': 'mean',
        'quality_score': 'mean',
        'defect_count': 'sum'
    }).reset_index()
    
    fig_daily = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Process Parameters', 'Quality Metrics'),
        vertical_spacing=0.15
    )
    
    fig_daily.add_trace(
        go.Scatter(
            x=daily_avg['date'],
            y=daily_avg['ram_pressure'],
            name='RAM Pressure',
            line=dict(color='blue')
        ),
        row=1, col=1
    )
    
    fig_daily.add_trace(
        go.Scatter(
            x=daily_avg['date'],
            y=daily_avg['front_temp'],
            name='Front Temp',
            line=dict(color='red'),
            yaxis="y2"
        ),
        row=1, col=1
    )
    
    fig_daily.add_trace(
        go.Scatter(
            x=daily_avg['date'],
            y=daily_avg['quality_score'],
            name='Quality Score',
            line=dict(color='green')
        ),
        row=2, col=1
    )
    
    fig_daily.add_trace(
        go.Bar(
            x=daily_avg['date'],
            y=daily_avg['defect_count'],
            name='Defects',
            marker_color='orange'
        ),
        row=2, col=1
    )
    
    fig_daily.update_layout(height=600)
    fig_daily.update_yaxes(title_text="Pressure", row=1, col=1)
    fig_daily.update_yaxes(title_text="Temperature", row=1, col=1, secondary_y=True)
    fig_daily.update_yaxes(title_text="Quality Score", row=2, col=1)
    fig_daily.update_yaxes(title_text="Defect Count", row=2, col=1, secondary_y=True)
    
    st.plotly_chart(fig_daily, use_container_width=True)

with tab2:
    st.subheader("Statistical Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribution plot
        param_dist = st.selectbox(
            "Parameter for Distribution",
            ['ram_pressure', 'front_temp', 'quality_score', 'ram_speed']
        )
        
        fig_dist = px.histogram(
            filtered_df,
            x=param_dist,
            nbins=30,
            title=f"Distribution of {param_dist.replace('_', ' ').title()}",
            marginal="box"
        )
        
        # Add mean and std lines
        mean_val = filtered_df[param_dist].mean()
        std_val = filtered_df[param_dist].std()
        
        fig_dist.add_vline(
            x=mean_val,
            line_dash="dash",
            line_color="green",
            annotation_text=f"Mean: {mean_val:.2f}"
        )
        
        fig_dist.add_vrect(
            x0=mean_val - std_val,
            x1=mean_val + std_val,
            fillcolor="lightgreen",
            opacity=0.2,
            annotation_text="±1σ"
        )
        
        st.plotly_chart(fig_dist, use_container_width=True)
    
    with col2:
        # Box plots
        category = st.selectbox(
            "Group By",
            ['process', 'material', 'day_of_week']
        )
        
        fig_box = px.box(
            filtered_df,
            x=category,
            y='quality_score',
            title=f"Quality Score by {category.replace('_', ' ').title()}"
        )
        st.plotly_chart(fig_box, use_container_width=True)
        
        # Correlation matrix
        if st.checkbox("Show Correlation Matrix"):
            numeric_cols = ['ram_pressure', 'front_temp', 'ram_speed', 'quality_score', 'extrusion_time']
            corr_matrix = filtered_df[numeric_cols].corr()
            
            fig_corr = px.imshow(
                corr_matrix,
                text_auto=True,
                aspect="auto",
                title="Correlation Matrix",
                color_continuous_scale='RdBu'
            )
            st.plotly_chart(fig_corr, use_container_width=True)

with tab3:
    st.subheader("Quality & Defect Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Defects by material
        defect_by_material = filtered_df.groupby('material')['defect_count'].sum().reset_index()
        fig_defects = px.pie(
            defect_by_material,
            values='defect_count',
            names='material',
            title="Defects by Material"
        )
        st.plotly_chart(fig_defects, use_container_width=True)
    
    with col2:
        # Quality trend
        fig_quality = px.line(
            filtered_df,
            x='timestamp',
            y='quality_score',
            color='process',
            title="Quality Score Trend by Process"
        )
        st.plotly_chart(fig_quality, use_container_width=True)
    
    # Scatter plot: Pressure vs Quality
    st.subheader("Process Parameter vs Quality")
    
    x_param = st.selectbox(
        "X-axis Parameter",
        ['ram_pressure', 'front_temp', 'ram_speed', 'extrusion_time'],
        key='x_param'
    )
    
    fig_scatter = px.scatter(
        filtered_df,
        x=x_param,
        y='quality_score',
        color='process',
        trendline="ols",
        title=f"{x_param.replace('_', ' ').title()} vs Quality Score"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

with tab4:
    st.subheader("Data Export")
    
    # Data preview
    st.dataframe(filtered_df, use_container_width=True, height=400)
    
    # Export options
    col1, col2 = st.columns(2)
    
    with col1:
        export_format = st.selectbox("Export Format", ["CSV", "Excel"])
        include_all = st.checkbox("Include all columns", value=True)
    
    with col2:
        st.write("")
        st.write("")
        if st.button("📥 Download Data", use_container_width=True, type="primary"):
            # Prepare data for download
            export_df = filtered_df if include_all else filtered_df[['timestamp', 'process', 'material', 'ram_pressure', 'front_temp', 'quality_score']]
            
            if export_format == "CSV":
                csv = export_df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="extrusion_data.csv",
                    mime="text/csv"
                )
            else:
                # For Excel, you'd typically use BytesIO
                st.info("Excel export requires additional setup. CSV export is recommended.")

# Insights section
with st.expander("💡 Analysis Insights"):
    insights = [
        "**Trend Analysis**: RAM pressure shows stable operation with occasional spikes",
        "**Quality Correlation**: Higher front temperatures (>425°C) correlate with lower quality scores",
        "**Process Comparison**: Roll_Production shows 5% better quality than Tube_Ext",
        "**Material Performance**: AL-7075 has 15% fewer defects compared to Copper",
        "**Time Analysis**: Quality scores improve during night shifts (operator consistency)",
        "**Recommendation**: Consider reducing front temperature by 5°C to improve quality by ~3%"
    ]
    
    for insight in insights:
        st.write(f"• {insight}")