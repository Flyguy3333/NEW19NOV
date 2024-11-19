import ccxt
import pandas as pd
import time
import logging
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Binance API keys from .env file
API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")

# Initialize Binance API
exchange = ccxt.binance({
    'apiKey': API_KEY,
    'secret': SECRET_KEY,
    'enableRateLimit': True
})

# Logger setup
logging.basicConfig(
    filename='bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Trading parameters
symbol = 'BTC/USDT'       # Trading pair
timeframe = '1m'          # Candlestick timeframe
order_size = 0.001        # Order size in BTC (adjust based on account size)
rsi_threshold = 30        # RSI level for buy signals

def fetch_data(symbol, timeframe, limit=50):
    """
    Fetch OHLCV (Open-High-Low-Close-Volume) data from Binance.
    """
    try:
        data = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')  # Convert timestamp to datetime
        return df
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        return None

def calculate_rsi(data, period=14):
    """
    Calculate the Relative Strength Index (RSI).
    """
    delta = data['close'].diff()  # Difference between consecutive close prices
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def place_order(symbol, order_type, side, amount):
    """
    Place a market order on Binance.
    """
    try:
        if order_type == 'market':
            order = exchange.create_market_order(symbol, side, amount)
            logging.info(f"Order placed: {order}")
        else:
            logging.error("Unsupported order type")
    except Exception as e:
        logging.error(f"Error placing order: {e}")

def trading_logic():
    """
    Main trading logic for the bot.
    """
    data = fetch_data(symbol, timeframe)
    if data is None or len(data) < 15:
        return  # Exit if data is unavailable or insufficient

    data['rsi'] = calculate_rsi(data)  # Calculate RSI
    latest_rsi = data['rsi'].iloc[-1]  # Get the most recent RSI value

    # Buy signal: RSI below threshold
    if latest_rsi < rsi_threshold:
        logging.info(f"RSI below {rsi_threshold}. Placing buy order.")
        place_order(symbol, 'market', 'buy', order_size)

    # Sell signal: RSI above threshold
    elif latest_rsi > 100 - rsi_threshold:
        logging.info(f"RSI above {100 - rsi_threshold}. Placing sell order.")
        place_order(symbol, 'market', 'sell', order_size)

if __name__ == "__main__":
    logging.info("Bot started")
    while True:
        try:
            trading_logic()
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
        time.sleep(60)  # Wait 1 minute before the next iteration

