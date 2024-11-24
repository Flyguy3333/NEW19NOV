import pandas as pd
import matplotlib.pyplot as plt

# Read CSV file
try:
    df = pd.read_csv("data/historical_data.csv")
    print("CSV file read successfully!")
    print(df.head())  # Print the first 5 rows to confirm content
except FileNotFoundError:
    print("Error: CSV file not found. Check the file path.")
except Exception as e:
    print(f"An error occurred: {e}")

# Define backtest function
def backtest(df):
    # Example strategy: Buy when RSI < 30, Sell when RSI > 70
    df['Signal'] = 0  # Default to no action
    df.loc[df['RSI'] < 30, 'Signal'] = 1  # Buy signal when RSI < 30
    df.loc[df['RSI'] > 70, 'Signal'] = -1  # Sell signal when RSI > 70
    
    # Example of calculating an equity curve (just a simple assumption here for the sake of example)
    df['Daily_Return'] = df['close'].pct_change()
    df['Strategy_Return'] = df['Daily_Return'] * df['Signal'].shift(1)  # Applying strategy
    
    # Compute cumulative returns for strategy
    df['Cumulative_Strategy_Return'] = (1 + df['Strategy_Return']).cumprod()
    df['Cumulative_Market_Return'] = (1 + df['Daily_Return']).cumprod()
    
    return df

# Apply backtest function
df_backtested = backtest(df)

# Display some results
print("\nBacktest Results:")
print(df_backtested[['timestamp', 'Signal', 'Cumulative_Strategy_Return', 'Cumulative_Market_Return']].tail())

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(df_backtested['timestamp'], df_backtested['Cumulative_Strategy_Return'], label='Strategy')
plt.plot(df_backtested['timestamp'], df_backtested['Cumulative_Market_Return'], label='Market')
plt.title('Backtest Strategy vs Market Performance')
plt.xlabel('Timestamp')
plt.ylabel('Cumulative Return')
plt.legend()
plt.show()
