import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect('crypto_data.db')

# Query to fetch data
query = "SELECT * FROM BTC_USDT_indicators"
df = pd.read_sql(query, conn)

# Close the database connection
conn.close()

# Print out the columns and the number of rows
print(f"Columns: {df.columns}")
print(f"Number of rows: {df.shape[0]}")
