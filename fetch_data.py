from binance.client import Client
import pandas as pd
import time

# Binance API keys
api_key = "your_api_key"
api_secret = "your_api_secret"

client = Client(api_key, api_secret)

def fetch_data(symbol="BTCUSDT", interval=Client.KLINE_INTERVAL_1MINUTE, limit=100):
    """
    Fetch historical klines from Binance.
    :param symbol: Trading pair (e.g., "BTCUSDT")
    :param interval: Kline interval (e.g., "1m", "5m")
    :param limit: Number of klines to fetch
    :return: pandas DataFrame with columns ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    """
    print(f"Fetching data for {symbol}...")
    klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    data = {
        "timestamp": [int(k[0]) for k in klines],
        "open": [float(k[1]) for k in klines],
        "high": [float(k[2]) for k in klines],
        "low": [float(k[3]) for k in klines],
        "close": [float(k[4]) for k in klines],
        "volume": [float(k[5]) for k in klines],
    }
    return pd.DataFrame(data)

if __name__ == "__main__":
    while True:
        df = fetch_data()
        print(df.tail())  # Display the last 5 rows
        time.sleep(60)  # Fetch every minute

