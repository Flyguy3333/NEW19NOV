import requests

# Proxy to route Binance traffic through DigitalOcean
proxies = {
    "http": "http://127.0.0.1:9999",
    "https": "http://127.0.0.1:9999"
}

# Binance API URL
url = "https://api.binance.com/api/v3/ticker/price"

try:
    # Make request using the proxy
    response = requests.get(url, proxies=proxies)
    data = response.json()
    print("Binance API Response:", data)
except Exception as e:
    print("Error fetching data:", e)
