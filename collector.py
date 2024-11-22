import pandas as pd
from sqlalchemy import create_engine
from indicators import calculate_indicators  # Importing the function to calculate indicators

# Create a mock DataFrame to simulate data collection
data = pd.DataFrame({
    "timestamp": pd.date_range(start="2024-11-21 00:00", periods=100, freq="min"),
    "close": range(100, 200),
    "open": range(99, 199),
    "high": [x + 5 for x in range(100, 200)],
    "low": [x - 5 for x in range(100, 200)],
    "volume": [10 for _ in range(100)]
})

# Apply indicators
data = calculate_indicators(data)

# Save to SQLite database
engine = create_engine("sqlite:///crypto_data.db")

try:
    data.to_sql("crypto_data", engine, if_exists="append", index=False)
    print("Data saved successfully!")
except Exception as e:
    print(f"Error saving to database: {e}")

