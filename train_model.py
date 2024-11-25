import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Function to load data from the database
def load_data(symbol):
    # Connect to the database
    conn = sqlite3.connect('crypto_data.db')
    
    # Read the data from the relevant table
    query = f"SELECT * FROM {symbol}_USDT_indicators"
    df = pd.read_sql(query, conn)
    conn.close()
    
    print(df.head())  # This line will print the DataFrame to see the data
    return df

# Function to train the model
def train_model(df, symbol):
    # Preprocessing the data
    df = df.dropna()  # Remove rows with missing values
    
    # Define features and target
    X = df[['SMA_20', 'EMA_50', 'RSI', 'MACD', 'MACD_signal']]
    y = df['buy_signal']  # Assuming buy_signal is the target

    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize the model
    model = RandomForestClassifier(n_estimators=100, random_state=42)

    # Train the model
    model.fit(X_train, y_train)

    # Make predictions and evaluate the model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model accuracy: {accuracy * 100:.2f}%")

    # Save the model to a file
    model_filename = f"models/{symbol}_model.pkl"
    joblib.dump(model, model_filename)
    print(f"Model saved to {model_filename}")

# Main function to run the training
def main():
    # Example: Train the model for XRP_USDT
    symbol = 'XRP'
    df = load_data(symbol)  # Load data from the database
    train_model(df, symbol)  # Train the model and save

if __name__ == "__main__":
    main()
