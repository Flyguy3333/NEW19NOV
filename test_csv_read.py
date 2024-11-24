import pandas as pd

# Test reading the historical data CSV
try:
    df = pd.read_csv("data/historical_data.csv")
    print("CSV file read successfully!")
    print(df.head())  # Print the first 5 rows to confirm content
except FileNotFoundError:
    print("Error: CSV file not found. Check the file path.")
except Exception as e:
    print(f"An error occurred: {e}")
