import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_extrusion_data(num_records=1000):
    """Generate sample extrusion data"""
    np.random.seed(42)
    
    dates = pd.date_range('2024-01-01', periods=num_records, freq='H')
    
    data = {
        'timestamp': dates,
        'ram_pressure': 45 + np.random.randn(num_records) * 5,
        'billet_pressure': 220 + np.random.randn(num_records) * 20,
        'front_temp': 410 + np.random.randn(num_records) * 8,
        'back_temp': 405 + np.random.randn(num_records) * 7,
        'ram_speed': np.abs(np.random.randn(num_records) * 1.5),
        'extrusion_time': 120 + np.random.randn(num_records) * 15,
        'quality_score': 90 + np.random.randn(num_records) * 5
    }
    
    return pd.DataFrame(data)