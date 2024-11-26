import requests

# Binance API Base URL
BASE_URL = "https://api.binance.com/api/v3"

def test_binance_connection():
    """
    Tests connectivity to Binance API by fetching server time.
    """
    endpoint = f"{BASE_URL}/time"
    try:
        response = requests.get(endpoint)
        response.raise_for_status()  # Raise an exception for HTTP errors
        print("Connection successful!")
        print(f"Server Time: {response.json()['serverTime']}")
    except requests.RequestException as e:
        print(f"Error connecting to Binance API: {e}")

if __name__ == "__main__":
    test_binance_connection()
