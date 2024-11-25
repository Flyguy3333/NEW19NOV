import sqlite3
import pandas as pd
import pickle

def load_model(symbol):
    with open(f"models/{symbol}_model.pkl", "rb") as f:
        return pickle.load(f)

def load_data(symbol):
    conn = sqlite3.connect("crypto_data.db")
    query = f"SELECT * FROM {symbol}_indicators"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def backtest(symbol):
    model = load_model(symbol)
    df = load_data(symbol)

    # Predict buy signals
    X = df[['SMA_20', 'EMA_50', 'RSI', 'MACD', 'MACD_signal']]
    df['buy_predicted'] = model.predict(X)

    # Simulate trades
    initial_balance = 1000
    balance = initial_balance
    position = 0
    for i, row in df.iterrows():
        if row['buy_predicted'] == 1 and position == 0:
            position = balance / row['close']
            balance = 0
        elif row['buy_predicted'] == 0 and position > 0:
            balance = position * row['close']
            position = 0

    # Final balance and return
    if position > 0:
        balance = position * df.iloc[-1]['close']
    profit = balance - initial_balance
    print(f"{symbol} Backtest Result: Initial Balance = ${initial_balance}, Final Balance = ${balance:.2f}, Profit = ${profit:.2f}")

def main():
    symbols = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT']
    for symbol in symbols:
        backtest(symbol)

if __name__ == "__main__":
    main()
