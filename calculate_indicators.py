import sqlite3
import pandas as pd
import pandas_ta as ta

DB_FILE = "crypto_data.db"

def fetch_data(symbol):
    conn = sqlite3.connect(DB_FILE)
    query = f"SELECT timestamp, open, high, low, close, volume FROM crypto_data WHERE symbol = '{symbol}' ORDER BY timestamp"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def calculate_indicators(df):
    df['SMA_20'] = ta.sma(df['close'], length=20)
    df['EMA_50'] = ta.ema(df['close'], length=50)
    df['RSI'] = ta.rsi(df['close'])
    df['MACD'], df['MACD_signal'] = ta.macd(df['close'], fast=12, slow=26, signal=9)[['MACD_12_26_9', 'MACDs_12_26_9']]
    return df

def save_indicators(symbol, df):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {symbol}_indicators (
            timestamp INTEGER PRIMARY KEY,
            SMA_20 REAL,
            EMA_50 REAL,
            RSI REAL,
            MACD REAL,
            MACD_signal REAL
        )
    """)
    for _, row in df.iterrows():
        cursor.execute(f"""
            INSERT OR REPLACE INTO {symbol}_indicators (timestamp, SMA_20, EMA_50, RSI, MACD, MACD_signal)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (row['timestamp'], row['SMA_20'], row['EMA_50'], row['RSI'], row['MACD'], row['MACD_signal']))
    conn.commit()
    conn.close()

def main():
    symbols = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT']
    for symbol in symbols:
        df = fetch_data(symbol)
        df = calculate_indicators(df)
        save_indicators(symbol, df)

if __name__ == "__main__":
    main()

