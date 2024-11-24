import sqlite3
import pandas as pd

# Database path
db_path = 'crypto_data.db'

def verify_data():
    """Fetch and display data from the database."""
    try:
        conn = sqlite3.connect(db_path)
        query = "SELECT * FROM market_data ORDER BY timestamp DESC LIMIT 10"
        data = pd.read_sql_query(query, conn)
        conn.close()

        print("Latest Data from Database:")
        print(data)

    except Exception as e:
        print(f"Error fetching data: {e}")

if __name__ == "__main__":
    verify_data()
