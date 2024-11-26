import pandas as pd
import pandas_ta as ta

# Example DataFrame with sample closing prices
df = pd.DataFrame({
    "close": [100, 102, 104, 103, 101, 99, 98, 100, 102, 105]
})

# Calculate the RSI (Relative Strength Index) indicator
df["RSI"] = ta.rsi(df["close"], length=14)

# Print the DataFrame to check the results
print(df)
