import ccxt
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import time
import logging

class BinanceDataFetcher:
    def __init__(self, use_proxy=True):
        self.proxies = {
            "http": "http://brd-customer-hl_980943f6-zone-us:glwlc3ws9off@brd.superproxy.io:33335",
            "https": "http://brd-customer-hl_980943f6-zone-us:glwlc3ws9off@brd.superproxy.io:33335"
        } if use_proxy else None
        
        self.exchange = ccxt.binance({
            'proxies': self.proxies,
            'enableRateLimit': True
        })
        
        self.db_path = 'crypto_data.db'
        self.retention_days = 120
        self.setup_database()
    
    def setup_database(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS market_data (
                    symbol TEXT,
                    timestamp INTEGER,
                    open REAL,
                    high REAL,
                    low REAL,
                    close REAL,
                    volume REAL,
                    quote_volume REAL,
                    trades INTEGER,
                    taker_buy_volume REAL,
                    taker_sell_volume REAL,
                    funding_rate REAL,
                    mark_price REAL,
                    index_price REAL,
                    PRIMARY KEY (symbol, timestamp)
                )
            """)
    
    def cleanup_old_data(self):
        cutoff = int((datetime.now() - timedelta(days=self.retention_days)).timestamp() * 1000)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM market_data WHERE timestamp < ?", (cutoff,))
            logging.info(f"Cleaned up data older than {self.retention_days} days")
    
    def fetch_all_usdt_pairs(self):
        try:
            markets = self.exchange.load_markets()
            return [symbol for symbol in markets.keys() if symbol.endswith('/USDT')]
        except Exception as e:
            logging.error(f"Error fetching markets: {e}")
            return []
    
    def fetch_extended_data(self, symbol):
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, '1m', limit=1)[0]
            ticker = self.exchange.fetch_ticker(symbol)
            
            data = {
                'symbol': symbol,
                'timestamp': ohlcv[0],
                'open': ohlcv[1],
                'high': ohlcv[2],
                'low': ohlcv[3],
                'close': ohlcv[4],
                'volume': ohlcv[5],
                'quote_volume': ticker.get('quoteVolume', 0),
                'trades': ticker.get('trades', 0),
                'taker_buy_volume': ticker.get('takerBuyBaseVolume', 0),
                'taker_sell_volume': ticker.get('takerSellBaseVolume', 0),
                'funding_rate': None,
                'mark_price': None,
                'index_price': None
            }
            
            if '/USDT' in symbol:
                try:
                    futures = self.exchange.fapiPublicGetPremiumIndex({'symbol': symbol.replace('/USDT', 'USDT')})
                    data.update({
                        'funding_rate': float(futures.get('lastFundingRate', 0)),
                        'mark_price': float(futures.get('markPrice', 0)),
                        'index_price': float(futures.get('indexPrice', 0))
                    })
                except:
                    pass
            
            return data
            
        except Exception as e:
            logging.error(f"Error fetching data for {symbol}: {e}")
            return None
    
    def store_data(self, data):
        if not data:
            return
            
        with sqlite3.connect(self.db_path) as conn:
            placeholders = ','.join(['?' for _ in data])
            columns = ','.join(data.keys())
            values = tuple(data.values())
            query = f"INSERT OR REPLACE INTO market_data ({columns}) VALUES ({placeholders})"
            conn.execute(query, values)
    
    def run(self):
        while True:
            try:
                usdt_pairs = self.fetch_all_usdt_pairs()
                for symbol in usdt_pairs:
                    data = self.fetch_extended_data(symbol)
                    self.store_data(data)
                    time.sleep(0.1)
                
                if datetime.now().hour == 0:
                    self.cleanup_old_data()
                    
                time.sleep(60)
                
            except Exception as e:
                logging.error(f"Error in main loop: {e}")
                time.sleep(5)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s]: %(message)s')
    fetcher = BinanceDataFetcher(use_proxy=True)
    fetcher.run()
