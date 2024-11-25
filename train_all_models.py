import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Function to load data
def load_data(symbol):
    conn = sqlite3.connect('crypto_data.db')
    query = f"SELECT * FROM {symbol}_USDT_indicators"  # Adjust for your coin
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Function to train the model
def train_model(coin):
    # Load data
    df = load_data(coin)
    
    # Ensure there is data to train on
    if df.empty:
        print(f"No data available for {coin}. Skipping model training.")
        return

    # Print columns and number of rows to ensure data is loaded properly
    print(f"Columns for {coin}: {df.columns}")
    print(f"Number of rows: {df.shape[0]}")

    # Define the features (input columns) and the label (output column)
    indicator_columns = ['SMA_20', 'EMA_50', 'RSI', 'MACD', 'MACD_signal']  # Replace with your actual columns if needed
    X = df[indicator_columns]  # Features
    y = df['buy_signal']  # Labels (you can change this to 'sell_signal' if needed)

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize and train a RandomForest model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate the model
    accuracy = model.score(X_test, y_test)
    print(f"Model accuracy for {coin}: {accuracy * 100:.2f}%")

    # Save the trained model
    model_filename = f"models/{coin}_model.pkl"
    joblib.dump(model, model_filename)
    print(f"Model for {coin} saved to {model_filename}")

# List of coins to train models for
coins = ['BTC', 'ETH', 'XRP', 'LTC']  # Add all the coins you need

# Train models for each coin
for coin in coins:
    train_model(coin)
