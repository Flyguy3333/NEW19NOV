import logging
import sqlite3
from datetime import datetime
import ccxt

# Configure logging
logging.basicConfig(
    filename='collector.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Initialize exchange
exchange = ccxt.binance({
    'rateLimit': 1200,
    'enableRateLimit': True,
})

# Database setup
db_path = 'crypto_data.db'

def create_table():
    """Create a table for storing crypto data."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS market_data (
            id INTEGER PRIMARY KEY,
            symbol TEXT,
            timestamp DATETIME,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume REAL
        )
    """)
    conn.commit()
    conn.close()

def fetch_and_store_data():
    """Fetch data from Binance and store it in the database."""
    try:
        # Fetch ticker data
        ticker_data = exchange.fetch_tickers()
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        for symbol, data in ticker_data.items():
            if 'close' in data:
                cursor.execute("""
                    INSERT INTO market_data (symbol, timestamp, open, high, low, close, volume)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    symbol,
                    datetime.utcfromtimestamp(data['timestamp'] / 1000),
                    data.get('open', 0),
                    data.get('high', 0),
                    data.get('low', 0),
                    data.get('close', 0),
                    data.get('quoteVolume', 0)
                ))

        conn.commit()
        conn.close()
        logging.info("Data fetched and stored successfully.")

    except Exception as e:
        logging.error(f"Error fetching or storing data: {e}")

if __name__ == "__main__":
    logging.info("Starting collector script...")
    create_table()
    fetch_and_store_data()
    logging.info("Collector script completed.")
