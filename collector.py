import sqlite3
import pandas as pd
import talib
from binance.client import Client

# Binance API keys
API_KEY = "x84SxoHndyDIqRcegdwTd2jjvyQHvwwmixaJgfrqcYRVf6Cj0RSdEAQ0qx74hhn7"
API_SECRET = "GMmYuLioe8365CjOQ9c94iaMvzpnlPuVWqQTMO92k2GcWkhJajX2gt7VEmeTeVJi"

# Initialize Binance Client
client = Client(API_KEY, API_SECRET)

# SQLite database file
DB_FILE = "crypto_data.db"

def fetch_binance_data(symbol="BTCUSDT", interval="1m", limit=100):
    """Fetches historical data from Binance."""
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

def calculate_indicators(df):
    """Calculates indicators using TA-Lib."""
    df["SMA_20"] = talib.SMA(df["close"], timeperiod=20)
    df["EMA_20"] = talib.EMA(df["close"], timeperiod=20)
    df["RSI"] = talib.RSI(df["close"], timeperiod=14)
    df["MACD"], df["MACD_Signal"], df["MACD_Hist"] = talib.MACD(df["close"])
    df["ATR"] = talib.ATR(df["high"], df["low"], df["close"], timeperiod=14)
    return df

def save_to_sqlite(df, table_name="market_data"):
    """Saves the DataFrame to an SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()

def main():
    print("Fetching data from Binance...")
    data = fetch_binance_data()
    
    print("Calculating indicators...")
    data_with_indicators = calculate_indicators(data)
    
    print("Saving data to SQLite...")
    save_to_sqlite(data_with_indicators)
    
    print("Data saved successfully!")
    print(data_with_indicators.tail())

if __name__ == "__main__":
    main()

