import streamlit as st
import json

st.set_page_config(layout="wide")
st.title("⚙️ System Configuration")

# Initialize session state for settings
if 'system_settings' not in st.session_state:
    st.session_state.system_settings = {
        'pressure_limits': {
            'ram_min': 40, 'ram_max': 100, 'ram_warning': 80,
            'billet_min': 150, 'billet_max': 300, 'billet_warning': 250,
            'sys_min': 2, 'sys_max': 5, 'sys_warning': 4
        },
        'temperature_limits': {
            'front_min': 350, 'front_max': 450, 'front_warning': 420,
            'back_min': 340, 'back_max': 440, 'back_warning': 410,
            'oil_min': 20, 'oil_max': 40, 'oil_warning': 35
        },
        'alerts': {
            'email': True, 'sms': False, 'sound': True,
            'popup': True, 'log': True
        },
        'data_logging': {
            'interval': 5, 'retention_days': 90,
            'backup_enabled': True, 'backup_interval': 'daily'
        },
        'maintenance': {
            'ram_hours': 5000, 'container_hours': 4000,
            'heater_hours': 3000, 'pump_hours': 2000
        }
    }

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["Process Limits", "Alert Settings", "Data Management", "Maintenance"])

with tab1:
    st.header("Process Control Limits")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Pressure Limits (bar)")
        
        st.write("**RAM Pressure**")
        ram_min = st.number_input("Min RAM Pressure", 0, 200, 
                                 st.session_state.system_settings['pressure_limits']['ram_min'])
        ram_max = st.number_input("Max RAM Pressure", 0, 200, 
                                 st.session_state.system_settings['pressure_limits']['ram_max'])
        ram_warn = st.number_input("RAM Warning", 0, 200, 
                                  st.session_state.system_settings['pressure_limits']['ram_warning'])
        
        st.write("**Billet Pressure**")
        billet_min = st.number_input("Min Billet Pressure", 0, 500, 
                                    st.session_state.system_settings['pressure_limits']['billet_min'])
        billet_max = st.number_input("Max Billet Pressure", 0, 500, 
                                    st.session_state.system_settings['pressure_limits']['billet_max'])
        billet_warn = st.number_input("Billet Warning", 0, 500, 
                                     st.session_state.system_settings['pressure_limits']['billet_warning'])
    
    with col2:
        st.subheader("Temperature Limits (°C)")
        
        st.write("**Front Temperature**")
        front_min = st.number_input("Min Front Temp", 200, 500, 
                                   st.session_state.system_settings['temperature_limits']['front_min'])
        front_max = st.number_input("Max Front Temp", 200, 500, 
                                   st.session_state.system_settings['temperature_limits']['front_max'])
        front_warn = st.number_input("Front Warning", 200, 500, 
                                    st.session_state.system_settings['temperature_limits']['front_warning'])
        
        st.write("**Oil Temperature**")
        oil_min = st.number_input("Min Oil Temp", 0, 100, 
                                 st.session_state.system_settings['temperature_limits']['oil_min'])
        oil_max = st.number_input("Max Oil Temp", 0, 100, 
                                 st.session_state.system_settings['temperature_limits']['oil_max'])
        oil_warn = st.number_input("Oil Warning", 0, 100, 
                                  st.session_state.system_settings['temperature_limits']['oil_warning'])
    
    if st.button("💾 Save Process Limits", type="primary"):
        st.session_state.system_settings['pressure_limits'] = {
            'ram_min': ram_min, 'ram_max': ram_max, 'ram_warning': ram_warn,
            'billet_min': billet_min, 'billet_max': billet_max, 'billet_warning': billet_warn,
            'sys_min': 2, 'sys_max': 5, 'sys_warning': 4
        }
        
        st.session_state.system_settings['temperature_limits'] = {
            'front_min': front_min, 'front_max': front_max, 'front_warning': front_warn,
            'back_min': 340, 'back_max': 440, 'back_warning': 410,
            'oil_min': oil_min, 'oil_max': oil_max, 'oil_warning': oil_warn
        }
        
        st.success("Process limits saved successfully!")

with tab2:
    st.header("Alert & Notification Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Alert Channels")
        
        email_alerts = st.checkbox("Email Alerts",
                                  value=st.session_state.system_settings['alerts']['email'])
        sms_alerts = st.checkbox("SMS Alerts",
                                value=st.session_state.system_settings['alerts']['sms'])
        sound_alerts = st.checkbox("Sound Alerts",
                                  value=st.session_state.system_settings['alerts']['sound'])
        popup_alerts = st.checkbox("Popup Alerts",
                                  value=st.session_state.system_settings['alerts']['popup'])
        
        st.subheader("Alert Thresholds")
        
        high_temp_alert = st.number_input("High Temp Alert (°C)", 0, 500, 425)
        high_pressure_alert = st.number_input("High Pressure Alert (bar)", 0, 200, 90)
        low_pressure_alert = st.number_input("Low Pressure Alert (bar)", 0, 200, 30)
    
    with col2:
        st.subheader("Auto Actions")
        
        auto_shutdown = st.checkbox("Enable Auto Shutdown", value=True)
        if auto_shutdown:
            shutdown_temp = st.number_input("Shutdown Temp (°C)", 0, 500, 450)
            shutdown_pressure = st.number_input("Shutdown Pressure (bar)", 0, 300, 100)
        
        auto_pause = st.checkbox("Enable Auto Pause", value=True)
        if auto_pause:
            pause_temp = st.number_input("Pause Temp (°C)", 0, 500, 430)
            pause_pressure = st.number_input("Pause Pressure (bar)", 0, 300, 95)
        
        st.subheader("Alert Recipients")
        recipients = st.text_area("Email Recipients (comma-separated)",
                                 value="operator@factory.com,manager@factory.com")
    
    if st.button("💾 Save Alert Settings", type="primary"):
        st.session_state.system_settings['alerts'] = {
            'email': email_alerts,
            'sms': sms_alerts,
            'sound': sound_alerts,
            'popup': popup_alerts,
            'log': True
        }
        
        st.session_state.system_settings['alert_thresholds'] = {
            'high_temp': high_temp_alert,
            'high_pressure': high_pressure_alert,
            'low_pressure': low_pressure_alert,
            'auto_shutdown': auto_shutdown,
            'shutdown_temp': shutdown_temp if auto_shutdown else None,
            'shutdown_pressure': shutdown_pressure if auto_shutdown else None
        }
        
        st.success("Alert settings saved!")

with tab3:
    st.header("Data Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Data Logging")
        
        log_interval = st.selectbox(
            "Logging Interval (seconds)",
            [1, 5, 10, 30, 60],
            index=[1, 5, 10, 30, 60].index(st.session_state.system_settings['data_logging']['interval'])
        )
        
        retention_days = st.slider(
            "Data Retention (days)",
            1, 365,
            st.session_state.system_settings['data_logging']['retention_days']
        )
        
        backup_enabled = st.checkbox(
            "Enable Auto Backup",
            value=st.session_state.system_settings['data_logging']['backup_enabled']
        )
        
        if backup_enabled:
            backup_interval = st.selectbox(
                "Backup Interval",
                ["hourly", "daily", "weekly", "monthly"],
                index=["hourly", "daily", "weekly", "monthly"].index(
                    st.session_state.system_settings['data_logging']['backup_interval']
                )
            )
    
    with col2:
        st.subheader("Database Status")
        
        st.info("""
        **Current Status:**
        - Database Size: 245 MB
        - Total Records: 15,432
        - Last Backup: 2024-01-15 03:00
        - Next Backup: 2024-01-16 03:00
        - Free Space: 1.2 GB
        """)
        
        st.subheader("Data Actions")
        
        if st.button("🔄 Clear Cache", use_container_width=True):
            st.cache_data.clear()
            st.success("Cache cleared!")
        
        if st.button("🧹 Purge Old Data", use_container_width=True):
            st.warning("This will delete data older than retention period!")
            confirm = st.checkbox("I confirm this action")
            if confirm and st.button("Confirm Purge", type="primary"):
                st.success("Old data purged successfully!")
        
        if st.button("💾 Manual Backup", use_container_width=True, type="primary"):
            st.success("Backup initiated. Check backup folder.")
    
    if st.button("💾 Save Data Settings", type="primary"):
        st.session_state.system_settings['data_logging'] = {
            'interval': log_interval,
            'retention_days': retention_days,
            'backup_enabled': backup_enabled,
            'backup_interval': backup_interval if backup_enabled else 'daily'
        }
        st.success("Data settings saved!")

with tab4:
    st.header("Maintenance Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Component Life Hours")
        
        ram_hours = st.number_input(
            "RAM System Hours",
            0, 10000,
            st.session_state.system_settings['maintenance']['ram_hours']
        )
        
        container_hours = st.number_input(
            "Container Hours",
            0, 10000,
            st.session_state.system_settings['maintenance']['container_hours']
        )
        
        heater_hours = st.number_input(
            "Heater Hours",
            0, 10000,
            st.session_state.system_settings['maintenance']['heater_hours']
        )
        
        pump_hours = st.number_input(
            "Pump Hours",
            0, 10000,
            st.session_state.system_settings['maintenance']['pump_hours']
        )
        
        st.subheader("Calibration Schedule")
        
        cal_interval = st.selectbox(
            "Calibration Interval",
            ["weekly", "monthly", "quarterly", "yearly"],
            index=1
        )
        
        last_calibration = st.date_input("Last Calibration")
    
    with col2:
        st.subheader("Component Status")
        
        components = [
            ("RAM System", ram_hours, 5000),
            ("Container", container_hours, 4000),
            ("Heating System", heater_hours, 3000),
            ("Hydraulic Pump", pump_hours, 2000),
            ("Control System", 4320, 8000)
        ]
        
        for name, current, limit in components:
            usage = (current / limit) * 100
            
            st.write(f"**{name}**")
            progress = st.progress(min(usage / 100, 1.0))
            
            if usage > 90:
                st.error(f"{current}h / {limit}h ({usage:.0f}%) - Maintenance Required!")
            elif usage > 75:
                st.warning(f"{current}h / {limit}h ({usage:.0f}%) - Schedule Maintenance")
            else:
                st.success(f"{current}h / {limit}h ({usage:.0f}%) - Good")
        
        st.subheader("Maintenance Actions")
        
        if st.button("📅 Schedule Maintenance", use_container_width=True):
            st.success("Maintenance scheduled for next available slot")
        
        if st.button("📝 Log Maintenance", use_container_width=True):
            st.success("Maintenance logged successfully")
    
    if st.button("💾 Save Maintenance Settings", type="primary"):
        st.session_state.system_settings['maintenance'] = {
            'ram_hours': ram_hours,
            'container_hours': container_hours,
            'heater_hours': heater_hours,
            'pump_hours': pump_hours
        }
        st.success("Maintenance settings saved!")

# Export/Import Settings
st.divider()
st.subheader("Configuration Management")

col1, col2 = st.columns(2)

with col1:
    if st.button("📤 Export Configuration", use_container_width=True):
        settings_json = json.dumps(st.session_state.system_settings, indent=2)
        st.download_button(
            label="Download Settings JSON",
            data=settings_json,
            file_name="extrusion_settings.json",
            mime="application/json"
        )

with col2:
    uploaded_file = st.file_uploader("Import Configuration", type=['json'])
    if uploaded_file is not None:
        try:
            imported_settings = json.load(uploaded_file)
            if st.button("Apply Imported Settings", type="primary"):
                st.session_state.system_settings = imported_settings
                st.success("Settings imported successfully!")
        except:
            st.error("Invalid configuration file")

# Current settings display
with st.expander("📋 Current Configuration"):
    st.json(st.session_state.system_settings)