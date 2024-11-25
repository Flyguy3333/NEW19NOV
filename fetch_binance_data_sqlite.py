import ccxt
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import time
import logging

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s]: %(message)s')

# Initialize Binance API
exchange = ccxt.binance()

# Database connection
db_path = 'crypto_data.db'  # Update with your database path
conn = sqlite3.connect(db_path)

# Parameters
symbols = ["BTC/USDT", "ETH/USDT"]  # Add more trading pairs
timeframes = ["1m", "5m", "15m", "1h", "4h", "1d"]  # Desired timeframes
since_timestamp = int((datetime.now() - timedelta(days=120)).timestamp() * 1000)

# Ensure tables exist for each symbol and timeframe
def create_table(symbol, timeframe):
    table_name = f"{symbol.replace('/', '_')}_{timeframe}"
    query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        timestamp INTEGER PRIMARY KEY,
        open REAL,
        high REAL,
        low REAL,
        close REAL,
        volume REAL
    )
    """
    conn.execute(query)
    conn.commit()
    return table_name

# Insert data into SQLite
def insert_data(table_name, df):
    with conn:
        df.to_sql(table_name, conn, if_exists='append', index=False)

# Fetch and store data
for symbol in symbols:
    for timeframe in timeframes:
        try:
            # Ensure the table exists
            table_name = create_table(symbol, timeframe)
            
            logging.info(f"Fetching {symbol} - {timeframe} since {datetime.fromtimestamp(since_timestamp / 1000)}")
            
            # Fetch data from Binance
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since=since_timestamp)
            
            # Convert to DataFrame
            df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit='ms')
            
            # Check for duplicates and only insert new data
            existing_timestamps = conn.execute(f"SELECT timestamp FROM {table_name}").fetchall()
            existing_timestamps = {row[0] for row in existing_timestamps}
            df = df[~df["timestamp"].astype(int).isin(existing_timestamps)]
            
            if not df.empty:
                insert_data(table_name, df)
                logging.info(f"Inserted {len(df)} rows into {table_name}")
            else:
                logging.info(f"No new data for {symbol} - {timeframe}")
            
            # Rate limit handling
            time.sleep(1)  # Adjust based on API limits
            
        except Exception as e:
            logging.error(f"Error fetching {symbol} - {timeframe}: {e}")
