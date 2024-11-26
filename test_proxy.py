import os
import ccxt

os.environ['HTTP_PROXY'] = 'http://brd-customer-hl_980943f6-zone-us:glwlc3ws9off@brd.superproxy.io:33335'
os.environ['HTTPS_PROXY'] = 'http://brd-customer-hl_980943f6-zone-us:glwlc3ws9off@brd.superproxy.io:33335'

exchange = ccxt.binance({
    'enableRateLimit': True,
    'options': {
        'verify': False
    }
})

try:
    ticker = exchange.fetch_ticker('BTC/USDT')
    print("Success:", ticker['last'])
except Exception as e:
    print(f"Error: {e}")
