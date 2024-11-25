import ccxt
import pandas as pd
import sqlite3
import time

# Initialize Binance API
binance = ccxt.binance({
    'rateLimit': 1200,
    'enableRateLimit': True
})
