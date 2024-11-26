import requests
from requests.exceptions import ProxyError, HTTPError

# Proxy Configuration
proxies = {
    "http": "http://brd-customer-hl_980943f6-zone-residential_proxy2:glwlc3ws9off@brd.superproxy.io:33335",
    "https": "http://brd-customer-hl_980943f6-zone-residential_proxy2:glwlc3ws9off@brd.superproxy.io:33335",
}

# Binance API URL
url = "https://api.binance.com/api/v3/time"

try:
    # Send GET request to Binance API through the proxy
    response = requests.get(url, proxies=proxies, timeout=10, verify=False)  # Bypass SSL verification
    response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
    print("Response:", response.json())
except ProxyError as e:
    print("Proxy Error:", e)
except HTTPError as e:
    print("HTTP Error:", e.response.status_code, e.response.text)
except Exception as e:
    print("An unexpected error occurred:", e)
