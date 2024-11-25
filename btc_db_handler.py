import sqlite3
import pandas as pd
from datetime import datetime

class BTCIndicatorDBHandler:
    def __init__(self, db_path='crypto_indicators.db'):
        """Initialize database handler with specified database path."""
        self.db_path = db_path
        # Create table when initializing
        self.create_table()
        print(f"Database initialized at: {db_path}")

    def create_connection(self):
        """Create and return a database connection."""
        try:
            conn = sqlite3.connect(self.db_path)
            return conn
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            raise

    def create_table(self):
        """Create the BTC_USDT_indicators table if it doesn't exist."""
        try:
            conn = self.create_connection()
            cursor = conn.cursor()

            # Drop table if exists (for clean start)
            cursor.execute("DROP TABLE IF EXISTS BTC_USDT_indicators")
            
            create_table_sql = """
            CREATE TABLE BTC_USDT_indicators (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME NOT NULL,
                SMA_20 REAL NOT NULL,
                EMA_50 REAL NOT NULL,
                RSI REAL NOT NULL,
                MACD REAL NOT NULL,
                MACD_signal REAL NOT NULL,
                Indicator_6 REAL DEFAULT 0.0,
                Indicator_7 REAL DEFAULT 0.0,
                Indicator_8 REAL DEFAULT 0.0,
                Indicator_9 REAL DEFAULT 0.0,
                Indicator_10 REAL DEFAULT 0.0,
                Indicator_11 REAL DEFAULT 0.0,
                Indicator_12 REAL DEFAULT 0.0,
                Indicator_13 REAL DEFAULT 0.0,
                Indicator_14 REAL DEFAULT 0.0,
                Indicator_15 REAL DEFAULT 0.0,
                Indicator_16 REAL DEFAULT 0.0,
                Indicator_17 REAL DEFAULT 0.0,
                Indicator_18 REAL DEFAULT 0.0,
                Indicator_19 REAL DEFAULT 0.0,
                Indicator_20 REAL DEFAULT 0.0,
                Indicator_21 REAL DEFAULT 0.0,
                Indicator_22 REAL DEFAULT 0.0,
                Indicator_23 REAL DEFAULT 0.0,
                Indicator_24 REAL DEFAULT 0.0,
                Indicator_25 REAL DEFAULT 0.0,
                Indicator_26 REAL DEFAULT 0.0,
                Indicator_27 REAL DEFAULT 0.0,
                Indicator_28 REAL DEFAULT 0.0,
                Indicator_29 REAL DEFAULT 0.0,
                Indicator_30 REAL DEFAULT 0.0,
                Indicator_31 REAL DEFAULT 0.0,
                Indicator_32 REAL DEFAULT 0.0,
                Indicator_33 REAL DEFAULT 0.0,
                Indicator_34 REAL DEFAULT 0.0,
                Indicator_35 REAL DEFAULT 0.0,
                Indicator_36 REAL DEFAULT 0.0,
                Indicator_37 REAL DEFAULT 0.0,
                Indicator_38 REAL DEFAULT 0.0,
                Indicator_39 REAL DEFAULT 0.0,
                sell_signal INTEGER NOT NULL DEFAULT 0
            )
            """
            cursor.execute(create_table_sql)
            conn.commit()
            print("Table created successfully")
            
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")
            raise
        finally:
            conn.close()

    def insert_indicators(self, data):
        """Insert indicator data into the database."""
        try:
            conn = self.create_connection()
            cursor = conn.cursor()
            
            # Define columns in the correct order
            columns = (
                ['timestamp', 'SMA_20', 'EMA_50', 'RSI', 'MACD', 'MACD_signal'] +
                [f'Indicator_{i}' for i in range(6, 40)] +
                ['sell_signal']
            )
            
            # Create the SQL insert statement
            placeholders = ','.join(['?' for _ in range(len(columns))])
            insert_sql = f"""
            INSERT INTO BTC_USDT_indicators 
            ({','.join(columns)}) 
            VALUES ({placeholders})
            """
            
            # Prepare values for insertion
            values_to_insert = []
            for row in data:
                # Ensure datetime format is correct
                timestamp = datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S')
                
                row_values = [
                    timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                    float(row['SMA_20']),
                    float(row['EMA_50']),
                    float(row['RSI']),
                    float(row['MACD']),
                    float(row['MACD_signal'])
                ]
                
                # Add indicator values with default 0.0
                for i in range(6, 40):
                    row_values.append(float(row.get(f'Indicator_{i}', 0.0)))
                
                row_values.append(int(row['sell_signal']))
                values_to_insert.append(tuple(row_values))
            
            # Execute the insertion
            cursor.executemany(insert_sql, values_to_insert)
            conn.commit()
            print(f"Successfully inserted {len(values_to_insert)} rows")
            
        except (sqlite3.Error, ValueError) as e:
            print(f"Error inserting data: {e}")
            conn.rollback()
            raise
        finally:
            conn.close()

    def read_data(self):
        """Read all data from the database."""
        try:
            conn = self.create_connection()
            query = "SELECT * FROM BTC_USDT_indicators ORDER BY timestamp"
            df = pd.read_sql_query(query, conn)
            return df
        except sqlite3.Error as e:
            print(f"Error reading data: {e}")
            raise
        finally:
            conn.close()

def main():
    """Main function to demonstrate usage."""
    try:
        # Initialize database handler
        db_handler = BTCIndicatorDBHandler()
        
        # Example data
        sample_data = [
            {
                'timestamp': '2024-11-25 00:00:00',
                'SMA_20': 0.76,
                'EMA_50': 0.81,
                'RSI': 31.0,
                'MACD': 0.11,
                'MACD_signal': 0.09,
                'sell_signal': 1
            },
            {
                'timestamp': '2024-11-26 00:00:00',
                'SMA_20': 0.77,
                'EMA_50': 0.82,
                'RSI': 32.5,
                'MACD': 0.12,
                'MACD_signal': 0.10,
                'sell_signal': 1
            }
        ]
        
        # Insert the data
        db_handler.insert_indicators(sample_data)
        
        # Read and display the data
        df = db_handler.read_data()
        print("\nStored data:")
        print(df)
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
