import pandas as pd
import matplotlib.pyplot as plt

# Test the backtest functionality
def test_backtest():
    # Example test data similar to what you're using in your actual script
    data = {
        'timestamp': [1732168620000, 1732168680000, 1732168740000, 1732168800000, 1732168860000],
        'close': [97000, 97100, 97200, 97300, 97400],
        'RSI': [25, 45, 50, 75, 80],
        'MACD': [-10, -12, -11, -10, -8],
        'MACD_Signal': [-15, -13, -12, -11, -9]
    }
    df = pd.DataFrame(data)

    print("Test Data:")
    print(df)

    # Run the backtest strategy function
    def backtest(df):
        df['Signal'] = 0  # Default to no action
        df.loc[df['RSI'] < 30, 'Signal'] = 1  # Buy signal when RSI < 30
        df.loc[df['RSI'] > 70, 'Signal'] = -1  # Sell signal when RSI > 70
        
        df['Daily_Return'] = df['close'].pct_change()
        df['Strategy_Return'] = df['Daily_Return'] * df['Signal'].shift(1)  # Applying strategy
        
        df['Cumulative_Strategy_Return'] = (1 + df['Strategy_Return']).cumprod()
        df['Cumulative_Market_Return'] = (1 + df['Daily_Return']).cumprod()
        
        return df

    df_backtested = backtest(df)

    # Output results for verification
    print("\nBacktest Results:")
    print(df_backtested[['timestamp', 'Signal', 'Cumulative_Strategy_Return', 'Cumulative_Market_Return']])

    # Plot the results
    plt.figure(figsize=(10, 6))
    plt.plot(df_backtested['timestamp'], df_backtested['Cumulative_Strategy_Return'], label='Strategy')
    plt.plot(df_backtested['timestamp'], df_backtested['Cumulative_Market_Return'], label='Market')
    plt.title('Backtest Strategy vs Market Performance')
    plt.xlabel('Timestamp')
    plt.ylabel('Cumulative Return')
    plt.legend()
    plt.show()

# Run the test
test_backtest()
