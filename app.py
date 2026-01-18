import streamlit as st
from datetime import datetime
import pandas as pd
import numpy as np
import time

# Page configuration
st.set_page_config(
    page_title="Swisstek Aluminium Extrusion Press",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark/Industrial Theme CSS
st.markdown("""
<style>
    /* Main Container */
    .main {
        background-color: #0f172a;
        color: #f1f5f9;
    }
    
    /* Logo Container - CENTERED */
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #1e293b 0%, #334155 50%, #1e293b 100%);
        border-bottom: 3px solid #3b82f6;
        margin-bottom: 2rem;
    }
    
    /* Company Title */
    .company-title {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #60a5fa 0%, #3b82f6 50%, #60a5fa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        padding: 1rem 0;
    }
    
    /* Dashboard Title */
    .dashboard-title {
        font-size: 1.5rem;
        text-align: center;
        color: #cbd5e1;
        margin-bottom: 2rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid #475569;
    }
    
    /* White Metric Containers */
    .metric-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);
        border-left: 5px solid #3b82f6;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    .metric-card.pressure {
        border-left-color: #3b82f6;
        background: linear-gradient(145deg, #eff6ff 0%, #dbeafe 100%);
    }
    
    .metric-card.temperature {
        border-left-color: #ef4444;
        background: linear-gradient(145deg, #fef2f2 0%, #fee2e2 100%);
    }
    
    .metric-card.position {
        border-left-color: #10b981;
        background: linear-gradient(145deg, #f0fdf4 0%, #dcfce7 100%);
    }
    
    .metric-card.status {
        border-left-color: #8b5cf6;
        background: linear-gradient(145deg, #f5f3ff 0%, #ede9fe 100%);
    }
    
    /* Metric Text Styling */
    .metric-label {
        font-size: 0.85rem;
        font-weight: 600;
        color: #475569;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1e293b;
        margin-bottom: 0.25rem;
    }
    
    .metric-unit {
        font-size: 1rem;
        color: #64748b;
        margin-left: 0.25rem;
    }
    
    .metric-change {
        font-size: 0.85rem;
        font-weight: 500;
    }
    
    .change-positive {
        color: #10b981;
    }
    
    .change-negative {
        color: #ef4444;
    }
    
    .change-neutral {
        color: #64748b;
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #e2e8f0;
        margin-top: 2rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #475569;
    }
    
    .section-subheader {
        font-size: 1.2rem;
        font-weight: 600;
        color: #cbd5e1;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    /* Status Indicators */
    .status-dot {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
        vertical-align: middle;
    }
    
    .status-good {
        background-color: #10b981;
        box-shadow: 0 0 8px #10b981;
    }
    
    .status-warning {
        background-color: #f59e0b;
        box-shadow: 0 0 8px #f59e0b;
    }
    
    .status-alert {
        background-color: #ef4444;
        box-shadow: 0 0 8px #ef4444;
    }
    
    /* Sidebar Styling */
    .sidebar .sidebar-content {
        background-color: #1e293b;
        color: #f1f5f9;
    }
    
    /* Alert Boxes */
    .alert-box {
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 5px solid;
    }
    
    .alert-success {
        background-color: #d1fae5;
        border-left-color: #10b981;
        color: #065f46;
    }
    
    .alert-warning {
        background-color: #fef3c7;
        border-left-color: #f59e0b;
        color: #92400e;
    }
    
    .alert-danger {
        background-color: #fee2e2;
        border-left-color: #ef4444;
        color: #991b1b;
    }
    
    /* Data Table */
    .data-table {
        background-color: white;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Footer */
    .footer {
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid #475569;
        color: #94a3b8;
        font-size: 0.9rem;
        text-align: center;
    }
    
    /* Button Styling */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #1e293b;
        border-radius: 8px 8px 0px 0px;
        gap: 1rem;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #3b82f6 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_data' not in st.session_state:
    st.session_state.current_data = {}
if 'auto_refresh' not in st.session_state:
    st.session_state.auto_refresh = False
if 'emergency_stop' not in st.session_state:
    st.session_state.emergency_stop = False

# Function to generate current extrusion data
def generate_current_data():
    """Generate current extrusion data matching your control panel"""
    np.random.seed(int(time.time()) % 1000)
    
    data = {
        'timestamp': datetime.now(),
        
        # Core positions
        'main_ram_position': 298.8 + np.random.randn() * 0.5,
        'container_position': 450.0 + np.random.randn() * 0.5,
        
        # Pressure system
        'sys_pressure': 3.0 + np.random.randn() * 0.1,
        'aux_pressure': 2.4 + np.random.randn() * 0.1,
        'pilot_pressure': 48.7 + np.random.randn() * 0.5,
        'ram_pressure': 48.7 + np.random.randn() * 0.5,
        'ram_press': 0.0 + np.random.randn() * 0.1,
        'lock_pressure': 2.3 + np.random.randn() * 0.1,
        'low_pressure': 2.7 + np.random.randn() * 0.1,
        'billet_pressure': 224.5 + np.random.randn() * 2,
        
        # Temperature system
        'oil_temp': 29.1 + np.random.randn() * 0.3,
        'front_temp': 412.8 + np.random.randn() * 2,
        'back_temp': 405.5 + np.random.randn() * 2,
        'profile_temp': 0.0,
        
        # Speed system
        'ram_speed': 0.0 + np.random.randn() * 0.1,
        'container_speed': 0.0 + np.random.randn() * 0.1,
        'extrusion_time': 0.0,
        
        # Residue & counters
        'container_residue': max(1100, 1149.2 - np.random.rand() * 0.5),
        'billet_residue': 0.0,
        'die_counter': 0,
        'total_count': 45,
        
        # Status flags
        'ram_status': 'STOP',
        'mode': 'MANUAL',
        'puller_status': 'ON',
        'phase': 'PLUX',
        'data_status': 'ACTIVE',
        'ram_stop': 30,
        'manual_mode': 30
    }
    return data

# Update current data
st.session_state.current_data = generate_current_data()

# ==================== SIDEBAR ====================
with st.sidebar:
    # Sidebar Header
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    try:
        # Try to load logo - CENTERED
        st.image("logo.png", width=120)
    except:
        # Fallback if logo not found
        st.markdown("<h2 style='color: #60a5fa;'>🏭 SWISSTEK</h2>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # System Status
    st.markdown("### 📊 System Status")
    
    col1, col2 = st.columns(2)
    with col1:
        ram_status = st.session_state.current_data['ram_status']
        dot_color = "status-good" if ram_status == 'STOP' else "status-alert"
        st.markdown(f"""
        <div class='metric-card status'>
            <div class='metric-label'>RAM Status</div>
            <div class='metric-value'>
                <span class='status-dot {dot_color}'></span>
                {ram_status}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        mode = st.session_state.current_data['mode']
        st.markdown(f"""
        <div class='metric-card status'>
            <div class='metric-label'>Operation Mode</div>
            <div class='metric-value'>{mode}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick Stats
    st.markdown("---")
    st.markdown("### 📈 Quick Stats")
    
    stats = [
        ("Total Production", f"{st.session_state.current_data['total_count']} CLEAR"),
        ("Phase", st.session_state.current_data['phase']),
        ("Oil Temp", f"{st.session_state.current_data['oil_temp']:.1f}°C"),
        ("Die Counter", f"{st.session_state.current_data['die_counter']} Pcs"),
        ("RAM Stop", st.session_state.current_data['ram_stop']),
        ("Manual Reset", st.session_state.current_data['manual_mode'])
    ]
    
    for label, value in stats:
        st.markdown(f"""
        <div style='display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid #475569;'>
            <span style='color: #cbd5e1;'>{label}:</span>
            <span style='font-weight: 600; color: #60a5fa;'>{value}</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Controls
    st.markdown("---")
    st.markdown("### ⚙️ Controls")
    
    st.session_state.auto_refresh = st.checkbox("🔄 Auto-refresh (5s)", value=False)
    
    if st.button("📊 Export Data", use_container_width=True):
        st.success("Data export initiated")
    
    # Emergency Stop
    st.markdown("---")
    if st.button("🛑 EMERGENCY STOP", type="primary", use_container_width=True):
        st.session_state.emergency_stop = True
        st.error("EMERGENCY STOP ACTIVATED!")
    
    if st.session_state.emergency_stop:
        if st.button("🟢 RESUME OPERATION", type="secondary", use_container_width=True):
            st.session_state.emergency_stop = False
            st.rerun()
    
    st.markdown("---")
    st.markdown(f"**Last Update:** {datetime.now().strftime('%H:%M:%S')}")

# ==================== MAIN CONTENT ====================
# Logo and Title Section - CENTERED
st.markdown("<div class='logo-container'>", unsafe_allow_html=True)
try:
    # Center the logo
    col_logo1, col_logo2, col_logo3 = st.columns([1, 2, 1])
    with col_logo2:
        st.image("logo.png", width=500)  # Center logo
except:
    # Fallback centered text
    st.markdown("<h1 class='company-title'>🏭 SWISSTEK ALUMINIUM</h1>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<h1 class='dashboard-title'>EXTRUSION PRESS MONITORING DASHBOARD</h1>", unsafe_allow_html=True)

# Emergency stop overlay
if st.session_state.emergency_stop:
    st.error("""
    ⚠️ **EMERGENCY STOP ACTIVATED** ⚠️
    
    All systems are halted. Press RESUME in the sidebar to continue.
    """)
    st.stop()

# Process Information
st.markdown("<div class='section-header'>Process Information</div>", unsafe_allow_html=True)

info_col1, info_col2, info_col3 = st.columns(3)
with info_col1:
    st.markdown("""
    <div class='metric-card status'>
        <div class='metric-label'>Current Process</div>
        <div class='metric-value'>Roll Production #1</div>
    </div>
    """, unsafe_allow_html=True)

with info_col2:
    current_time = datetime.now().strftime('%m/%Y %H:%M:%S')
    st.markdown(f"""
    <div class='metric-card status'>
        <div class='metric-label'>Date/Time</div>
        <div class='metric-value'>{current_time}</div>
    </div>
    """, unsafe_allow_html=True)

with info_col3:
    st.markdown("""
    <div class='metric-card status'>
        <div class='metric-label'>Operator & Shift</div>
        <div class='metric-value'>System Auto | Day</div>
    </div>
    """, unsafe_allow_html=True)

# ==================== PRESSURE SYSTEM ====================
st.markdown("<div class='section-header'>Pressure System</div>", unsafe_allow_html=True)

# Row 1
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
    <div class='metric-card pressure'>
        <div class='metric-label'>RAM Pressure</div>
        <div class='metric-value'>
            {st.session_state.current_data['ram_pressure']:.1f}
            <span class='metric-unit'>bar</span>
        </div>
        <div class='metric-change change-positive'>▲ {np.random.randn()*0.5:.1f}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='metric-card pressure'>
        <div class='metric-label'>Billet Pressure</div>
        <div class='metric-value'>
            {st.session_state.current_data['billet_pressure']:.1f}
            <span class='metric-unit'>bar</span>
        </div>
        <div class='metric-change change-positive'>▲ {np.random.randn()*2:.1f}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class='metric-card pressure'>
        <div class='metric-label'>System Pressure</div>
        <div class='metric-value'>
            {st.session_state.current_data['sys_pressure']:.1f}
            <span class='metric-unit'>bar</span>
        </div>
        <div class='metric-change change-neutral'>→ {np.random.randn()*0.1:.1f}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class='metric-card pressure'>
        <div class='metric-label'>Pilot Pressure</div>
        <div class='metric-value'>
            {st.session_state.current_data['pilot_pressure']:.1f}
            <span class='metric-unit'>bar</span>
        </div>
        <div class='metric-change change-negative'>▼ {np.random.randn()*0.3:.1f}</div>
    </div>
    """, unsafe_allow_html=True)

# Row 2 - Additional Pressures
st.markdown("<div class='section-subheader'>Secondary Pressures</div>", unsafe_allow_html=True)

col5, col6, col7, col8 = st.columns(4)
with col5:
    st.markdown(f"""
    <div class='metric-card pressure'>
        <div class='metric-label'>AUX Pressure</div>
        <div class='metric-value'>
            {st.session_state.current_data['aux_pressure']:.1f}
            <span class='metric-unit'>bar</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown(f"""
    <div class='metric-card pressure'>
        <div class='metric-label'>Lock Pressure</div>
        <div class='metric-value'>
            {st.session_state.current_data['lock_pressure']:.1f}
            <span class='metric-unit'>bar</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col7:
    st.markdown(f"""
    <div class='metric-card pressure'>
        <div class='metric-label'>Low Pressure</div>
        <div class='metric-value'>
            {st.session_state.current_data['low_pressure']:.1f}
            <span class='metric-unit'>bar</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col8:
    st.markdown(f"""
    <div class='metric-card pressure'>
        <div class='metric-label'>RAM Press</div>
        <div class='metric-value'>
            {st.session_state.current_data['ram_press']:.1f}
            <span class='metric-unit'>bar</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==================== TEMPERATURE SYSTEM ====================
st.markdown("<div class='section-header'>Temperature System</div>", unsafe_allow_html=True)

temp_col1, temp_col2, temp_col3, temp_col4 = st.columns(4)

with temp_col1:
    temp = st.session_state.current_data['front_temp']
    status = "status-alert" if temp > 420 else "status-good" if temp < 415 else "status-warning"
    st.markdown(f"""
    <div class='metric-card temperature'>
        <div class='metric-label'>Front Temperature</div>
        <div class='metric-value'>
            <span class='status-dot {status}'></span>
            {temp:.1f}
            <span class='metric-unit'>°C</span>
        </div>
        <div class='metric-change {'change-negative' if temp > 420 else 'change-positive'}'>
            {np.random.randn()*2:.1f}°C
        </div>
    </div>
    """, unsafe_allow_html=True)

with temp_col2:
    temp = st.session_state.current_data['back_temp']
    status = "status-alert" if temp > 415 else "status-good"
    st.markdown(f"""
    <div class='metric-card temperature'>
        <div class='metric-label'>Back Temperature</div>
        <div class='metric-value'>
            <span class='status-dot {status}'></span>
            {temp:.1f}
            <span class='metric-unit'>°C</span>
        </div>
        <div class='metric-change change-positive'>▲ {np.random.randn()*1.5:.1f}°C</div>
    </div>
    """, unsafe_allow_html=True)

with temp_col3:
    temp = st.session_state.current_data['oil_temp']
    status = "status-alert" if temp > 35 else "status-good" if temp > 25 else "status-warning"
    st.markdown(f"""
    <div class='metric-card temperature'>
        <div class='metric-label'>Oil Temperature</div>
        <div class='metric-value'>
            <span class='status-dot {status}'></span>
            {temp:.1f}
            <span class='metric-unit'>°C</span>
        </div>
        <div class='metric-change change-neutral'>→ {np.random.randn()*0.3:.1f}°C</div>
    </div>
    """, unsafe_allow_html=True)

with temp_col4:
    temp = st.session_state.current_data['profile_temp']
    st.markdown(f"""
    <div class='metric-card temperature'>
        <div class='metric-label'>Profile Temperature</div>
        <div class='metric-value'>
            {temp:.1f}
            <span class='metric-unit'>°C</span>
        </div>
        <div class='metric-change change-neutral'>0.0°C</div>
    </div>
    """, unsafe_allow_html=True)

# ==================== POSITION & SPEED ====================
st.markdown("<div class='section-header'>Position & Speed Monitoring</div>", unsafe_allow_html=True)

pos_col1, pos_col2, pos_col3, pos_col4 = st.columns(4)

with pos_col1:
    st.markdown(f"""
    <div class='metric-card position'>
        <div class='metric-label'>RAM Position</div>
        <div class='metric-value'>
            {st.session_state.current_data['main_ram_position']:.1f}
            <span class='metric-unit'>mm</span>
        </div>
        <div class='metric-change change-neutral'>→ {np.random.randn()*0.2:.1f} mm</div>
    </div>
    """, unsafe_allow_html=True)

with pos_col2:
    st.markdown(f"""
    <div class='metric-card position'>
        <div class='metric-label'>Container Position</div>
        <div class='metric-value'>
            {st.session_state.current_data['container_position']:.1f}
            <span class='metric-unit'>mm</span>
        </div>
        <div class='metric-change change-neutral'>→ {np.random.randn()*0.2:.1f} mm</div>
    </div>
    """, unsafe_allow_html=True)

with pos_col3:
    st.markdown(f"""
    <div class='metric-card position'>
        <div class='metric-label'>RAM Speed</div>
        <div class='metric-value'>
            {st.session_state.current_data['ram_speed']:.1f}
            <span class='metric-unit'>mm/s</span>
        </div>
        <div class='metric-change change-neutral'>→ {np.random.randn()*0.1:.1f} mm/s</div>
    </div>
    """, unsafe_allow_html=True)

with pos_col4:
    st.markdown(f"""
    <div class='metric-card position'>
        <div class='metric-label'>Container Residue</div>
        <div class='metric-value'>
            {st.session_state.current_data['container_residue']:.1f}
            <span class='metric-unit'>mm</span>
        </div>
        <div class='metric-change change-negative'>▼ {np.random.rand()*0.5:.1f} mm</div>
    </div>
    """, unsafe_allow_html=True)

# ==================== DETAILED PARAMETERS ====================
st.markdown("<div class='section-header'>Detailed Parameters</div>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📊 Counters & Status", "⚙️ All Parameters", "📈 Quick View"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Counters")
        counters_data = {
            "DIE Counter": f"{st.session_state.current_data['die_counter']} Pcs",
            "Total Count": f"{st.session_state.current_data['total_count']} CLEAR",
            "RAM Stop": st.session_state.current_data['ram_stop'],
            "Manual": st.session_state.current_data['manual_mode'],
            "Extrusion Time": f"{st.session_state.current_data['extrusion_time']:.1f} sec",
            "Billet Residue": f"{st.session_state.current_data['billet_residue']:.1f} mm"
        }
        
        for label, value in counters_data.items():
            st.markdown(f"""
            <div style='background: #1e293b; padding: 0.75rem; margin: 0.5rem 0; border-radius: 8px; border-left: 4px solid #3b82f6;'>
                <div style='color: #cbd5e1; font-size: 0.9rem;'>{label}</div>
                <div style='color: #60a5fa; font-size: 1.2rem; font-weight: bold;'>{value}</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### System Status")
        status_data = {
            "RAM Status": st.session_state.current_data['ram_status'],
            "Operation Mode": st.session_state.current_data['mode'],
            "Puller Status": st.session_state.current_data['puller_status'],
            "Phase": st.session_state.current_data['phase'],
            "Data Status": st.session_state.current_data['data_status'],
            "Container Speed": f"{st.session_state.current_data['container_speed']:.1f} mm/s"
        }
        
        for label, value in status_data.items():
            st.markdown(f"""
            <div style='background: #1e293b; padding: 0.75rem; margin: 0.5rem 0; border-radius: 8px; border-left: 4px solid #10b981;'>
                <div style='color: #cbd5e1; font-size: 0.9rem;'>{label}</div>
                <div style='color: #60a5fa; font-size: 1.2rem; font-weight: bold;'>{value}</div>
            </div>
            """, unsafe_allow_html=True)

with tab2:
    # Create a DataFrame for all parameters
    all_params = {
        "Parameter": [
            "Main RAM Position", "Container Position", 
            "SYS Pressure", "AUX Pressure", "Pilot Pressure", "RAM Pressure",
            "RAM Press", "Lock Pressure", "Low Pressure", "Billet Pressure",
            "Oil Temperature", "Front Temperature", "Back Temperature", "Profile Temperature",
            "RAM Speed", "Container Speed", "Container Residue", "Billet Residue",
            "Extrusion Time", "DIE Counter", "Total Count"
        ],
        "Value": [
            f"{st.session_state.current_data['main_ram_position']:.1f} mm",
            f"{st.session_state.current_data['container_position']:.1f} mm",
            f"{st.session_state.current_data['sys_pressure']:.1f} bar",
            f"{st.session_state.current_data['aux_pressure']:.1f} bar",
            f"{st.session_state.current_data['pilot_pressure']:.1f} bar",
            f"{st.session_state.current_data['ram_pressure']:.1f} bar",
            f"{st.session_state.current_data['ram_press']:.1f} bar",
            f"{st.session_state.current_data['lock_pressure']:.1f} bar",
            f"{st.session_state.current_data['low_pressure']:.1f} bar",
            f"{st.session_state.current_data['billet_pressure']:.1f} bar",
            f"{st.session_state.current_data['oil_temp']:.1f}°C",
            f"{st.session_state.current_data['front_temp']:.1f}°C",
            f"{st.session_state.current_data['back_temp']:.1f}°C",
            f"{st.session_state.current_data['profile_temp']:.1f}°C",
            f"{st.session_state.current_data['ram_speed']:.1f} mm/s",
            f"{st.session_state.current_data['container_speed']:.1f} mm/s",
            f"{st.session_state.current_data['container_residue']:.1f} mm",
            f"{st.session_state.current_data['billet_residue']:.1f} mm",
            f"{st.session_state.current_data['extrusion_time']:.1f} sec",
            f"{st.session_state.current_data['die_counter']} Pcs",
            f"{st.session_state.current_data['total_count']} CLEAR"
        ]
    }
    
    df = pd.DataFrame(all_params)
    st.dataframe(df, use_container_width=True, height=400)

with tab3:
    # Quick view of key parameters
    st.markdown("### 🎯 Key Parameters Summary")
    
    key_params = [
        ("RAM Pressure", f"{st.session_state.current_data['ram_pressure']:.1f} bar", "pressure"),
        ("Front Temp", f"{st.session_state.current_data['front_temp']:.1f}°C", "temperature"),
        ("RAM Position", f"{st.session_state.current_data['main_ram_position']:.1f} mm", "position"),
        ("Billet Pressure", f"{st.session_state.current_data['billet_pressure']:.1f} bar", "pressure"),
        ("Container Residue", f"{st.session_state.current_data['container_residue']:.1f} mm", "position"),
        ("Oil Temp", f"{st.session_state.current_data['oil_temp']:.1f}°C", "temperature")
    ]
    
    cols = st.columns(3)
    for idx, (label, value, card_type) in enumerate(key_params):
        with cols[idx % 3]:
            st.markdown(f"""
            <div class='metric-card {card_type}'>
                <div class='metric-label'>{label}</div>
                <div class='metric-value'>{value.split()[0]}</div>
                <div style='color: #64748b;'>{' '.join(value.split()[1:])}</div>
            </div>
            """, unsafe_allow_html=True)

# ==================== ALERTS & WARNINGS ====================
st.markdown("<div class='section-header'>Alerts & Warnings</div>", unsafe_allow_html=True)

# Check for alerts
alerts = []

if st.session_state.current_data['front_temp'] > 420:
    alerts.append(("High Front Temperature", f"{st.session_state.current_data['front_temp']:.1f}°C exceeds 420°C limit", "danger"))
elif st.session_state.current_data['front_temp'] > 415:
    alerts.append(("Warning: Front Temperature", f"{st.session_state.current_data['front_temp']:.1f}°C approaching limit", "warning"))

if st.session_state.current_data['ram_pressure'] > 50:
    alerts.append(("High RAM Pressure", f"{st.session_state.current_data['ram_pressure']:.1f} bar exceeds 50 bar limit", "danger"))

if st.session_state.current_data['container_residue'] < 1100:
    alerts.append(("Low Container Residue", f"{st.session_state.current_data['container_residue']:.1f} mm is below 1100mm", "warning"))

if st.session_state.current_data['oil_temp'] > 35:
    alerts.append(("High Oil Temperature", f"{st.session_state.current_data['oil_temp']:.1f}°C exceeds 35°C limit", "danger"))

if alerts:
    for title, message, alert_type in alerts:
        if alert_type == "danger":
            st.markdown(f"""
            <div class='alert-box alert-danger'>
                <strong>⚠️ {title}:</strong> {message}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='alert-box alert-warning'>
                <strong>⚠️ {title}:</strong> {message}
            </div>
            """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class='alert-box alert-success'>
        <strong>✅ All systems normal:</strong> No active alerts or warnings
    </div>
    """, unsafe_allow_html=True)

# ==================== FOOTER ====================
st.markdown("<div class='footer'>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center;'>
    <div>🏭 <strong>Swisstek Aluminium</strong> | Extrusion Press Monitoring System v2.5</div>
    <div style='margin-top: 0.5rem;'>
        📅 Session: {date} | 🕐 Last Update: {time}
    </div>
    <div style='margin-top: 0.5rem; color: #60a5fa;'>
        🟢 <strong>Status:</strong> Operational | All Systems Go
    </div>
</div>
""".format(
    date=datetime.now().strftime('%Y-%m-%d'),
    time=datetime.now().strftime('%H:%M:%S')
), unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Auto-refresh logic
if st.session_state.auto_refresh:
    time.sleep(5)
    st.rerun()