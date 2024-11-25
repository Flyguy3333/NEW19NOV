import pandas as pd
import joblib

# Function to load the trained model
def load_trained_model(symbol):
    model_filename = f"models/{symbol}_model.pkl"
    model = joblib.load(model_filename)
    return model

# Function to make predictions
def make_predictions(symbol, data):
    model = load_trained_model(symbol)
    
    # Prepare features for prediction
    X = data[['SMA_20', 'EMA_50', 'RSI', 'MACD', 'MACD_signal']]  # Include all 40 features in the actual data
    predictions = model.predict(X)
    
    return predictions

# Example usage with new data
new_data = pd.DataFrame({
    'SMA_20': [150.5], 'EMA_50': [155.0], 'RSI': [45.5], 'MACD': [0.20], 'MACD_signal': [0.18]
})

# Make prediction for LTC
predictions = make_predictions('LTC', new_data)
print(f"Predictions: {predictions}")
