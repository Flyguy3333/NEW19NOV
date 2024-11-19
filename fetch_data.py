
import ccxt
import pandas as pd
import ta  # Technical analysis library for indicators

# Initialize Binance API
exchange = ccxt.binance({
    'rateLimit': 1200,
    'enableRateLimit': True,
})

# Fetch Historical Data
def fetch_historical_data(symbol, timeframe, since):
    """
    Fetch historical OHLCV data from Binance.
    :param symbol: Trading pair symbol, e.g., 'BTC/USDT'
    :param timeframe: Candle timeframe, e.g., '1h', '4h', '1d'
    :param since: Timestamp in milliseconds to fetch data since
    :return: DataFrame with OHLCV data
    """
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since=since)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

# Generate Features
def generate_features(df):
    """
    Add technical indicators and additional features to the data.
    :param df: DataFrame with OHLCV data
    :return: DataFrame with new features
    """
    # Add RSI
    df['rsi'] = ta.momentum.rsi(df['close'], window=14)
    # Add EMA
    df['ema'] = ta.trend.ema_indicator(df['close'], window=20)
    # Add Bollinger Bands
    bb = ta.volatility.BollingerBands(df['close'], window=20)
    df['bb_high'] = bb.bollinger_hband()
    df['bb_low'] = bb.bollinger_lband()
    # Add returns
    df['returns'] = df['close'].pct_change()
    # Add rolling volatility
    df['volatility'] = df['returns'].rolling(window=20).std()
    return df.dropna()

# Main
if __name__ == "__main__":
    symbol = 'BTC/USDT'
    timeframe = '1h'  # 1-hour candles
    since = exchange.parse8601('2023-01-01T00:00:00Z')  # Fetch data from Jan 1, 2023

    print("Fetching historical data...")
    df = fetch_historical_data(symbol, timeframe, since)
    
    print("Generating features...")
    df = generate_features(df)

    print("Saving to CSV...")
    output_file = f"{symbol.replace('/', '_')}_historical_data.csv"
    df.to_csv(output_file, index=False)
    print(f"Data saved to {output_file}")
