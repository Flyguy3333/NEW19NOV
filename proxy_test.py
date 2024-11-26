import ccxt
import requests
import urllib3
import uuid
import time
urllib3.disable_warnings()

# Using residential proxy configuration
PROXY_HOST = "brd.superproxy.io"
PROXY_PORT = "33335"  # Residential port
SESSION_ID = str(uuid.uuid4())[:8]
PROXY_USER = f"brd-customer-hl_980943f6-zone-residential_proxy1-country-ch-session-{SESSION_ID}"
PROXY_PASS = "iddt873sbq85"

# Construct proxy URL
PROXY_URL = f"http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}"

def test_direct_request():
    print("\nTesting direct request with full browser headers...")
    
    # Full browser-like headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    try:
        # First verify location
        print("Checking location...")
        response = requests.get(
            'https://lumtest.com/myip.json',
            proxies={'http': PROXY_URL, 'https': PROXY_URL},
            headers=headers,
            timeout=30,
            verify=False
        )
        print(f"Location Response: {response.text}")
        
        print("\nTesting Binance spot API...")
        binance_response = requests.get(
            'https://api.binance.com/api/v3/ping',  # Simple ping endpoint
            proxies={'http': PROXY_URL, 'https': PROXY_URL},
            headers=headers,
            timeout=30,
            verify=False
        )
        print(f"Binance Status Code: {binance_response.status_code}")
        print(f"Binance Response: {binance_response.text}")
        
        if binance_response.status_code == 200:
            print("\nTesting time endpoint...")
            time_response = requests.get(
                'https://api.binance.com/api/v3/time',
                proxies={'http': PROXY_URL, 'https': PROXY_URL},
                headers=headers,
                timeout=30,
                verify=False
            )
            print(f"Time Status Code: {time_response.status_code}")
            print(f"Time Response: {time_response.text}")
            
        return binance_response.status_code == 200
        
    except Exception as e:
        print(f"Request error: {str(e)}")
        return False

def test_ccxt_connection():
    if not test_direct_request():
        print("Skipping CCXT test due to direct request failure")
        return
        
    print("\nTesting CCXT connection...")
    try:
        binance = ccxt.binance({
            'options': {
                'defaultType': 'spot',
                'verify': False,
                'timeout': 30000,
                'adjustForTimeDifference': True
            },
            'proxies': {
                'http': PROXY_URL,
                'https': PROXY_URL,
            },
            'enableRateLimit': True,
            'headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5'
            }
        })
        
        time_response = binance.fetch_time()
        print(f"CCXT time response: {time_response}")
        return True
        
    except Exception as e:
        print(f"CCXT error: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing Switzerland proxy with enhanced browser simulation...")
    print(f"Using proxy URL: {PROXY_URL}")
    
    test_ccxt_connection()
