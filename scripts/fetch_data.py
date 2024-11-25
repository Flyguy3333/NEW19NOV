import os
import pandas as pd
from binance.client import Client
from datetime import datetime, timedelta

# Initialize Binance client (you need to fill in your API keys here)
api_key = 'your_api_key'
api_secret = 'your_api_secret'
client = Client(api_key, api_secret)

# Define your pairs and timeframes
pairs = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]  # You can add all 303 pairs here
timeframes = ['1m', '4h', '1d']  # Fetch data for 1 minute, 4 hours, and 1 day

# Define the path to save data
data_path = '/workspaces/NEW19NOV/data'

# Function to fetch historical data
def fetch_data(pair, timeframe, lookback_days=120):
    """Fetch historical data from Binance for a given pair and timeframe."""
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=lookback_days)

    # Format start_time to Binance API format
    start_str = start_time.strftime('%d %b %Y %H:%M:%S')

    # Fetch historical data from Binance
    klines = client.get_historical_klines(pair, timeframe, start_str)

    # Convert data to a DataFrame
    data = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_vol', 'num_trades', 'taker_buy_base_asset_vol', 'taker_buy_quote_asset_vol', 'ignore'])
    
    # Convert timestamp to datetime
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')

    # Set the timestamp as the index and drop the unnecessary columns
    data.set_index('timestamp', inplace=True)
    data = data[['open', 'high', 'low', 'close', 'volume']]

    # Save data to CSV
    if not os.path.exists(data_path):
        os.makedirs(data_path)

    file_path = f"{data_path}/{pair}_{timeframe}.csv"
    data.to_csv(file_path)
    print(f"Saved {pair} data for {timeframe} timeframe to {file_path}")

# Main function to fetch data for all pairs and timeframes
def main():
    for pair in pairs:
        for timeframe in timeframes:
            fetch_data(pair, timeframe)

if __name__ == "__main__":
    main()
