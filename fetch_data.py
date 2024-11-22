import pandas as pd

def fetch_data():
    data = pd.DataFrame({
        "timestamp": pd.date_range(start="2024-11-21 00:00", periods=100, freq="T"),
        "open": [100 + i for i in range(100)],
        "high": [101 + i for i in range(100)],
        "low": [99 + i for i in range(100)],
        "close": [100 + i for i in range(100)],
        "volume": [10 * i for i in range(100)],
    })
    return data

