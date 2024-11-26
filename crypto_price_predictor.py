import pandas as pd
import pandas_ta as ta
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import matplotlib.pyplot as plt

# Load data (replace with actual data file)
file_path = "crypto_data.csv"  # Historical data in CSV format
df = pd.read_csv(file_path)

# Prepare data
df["SMA"] = df["Close"].rolling(window=10).mean()  # Simple Moving Average
df["EMA"] = df["Close"].ewm(span=10).mean()       # Exponential Moving Average
df["RSI"] = ta.rsi(df["Close"], length=14)         # Relative Strength Index

# Target variable: 1 if price increased, 0 if decreased
df["Target"] = (df["Close"].shift(-1) > df["Close"]).astype(int)

# Drop NaN values
df = df.dropna()

# Feature selection
features = ["SMA", "EMA", "RSI"]
X = df[features]
y = df["Target"]

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluation
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
print("Classification Report:\n", classification_report(y_test, y_pred))

# Feature importance visualization
plt.bar(features, model.feature_importances_)
plt.title("Feature Importance")
plt.show()
