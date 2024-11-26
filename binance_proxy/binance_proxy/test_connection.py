import requests
import logging
import time
import socket
import urllib3
urllib3.disable_warnings()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_port(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    return result == 0

def test_binance_connection():
    proxy_url = f"http://127.0.0.1:8080"
    proxies = {
        "http": proxy_url,
        "https": proxy_url
    }
    
    print(f"\nChecking if port 8080 is listening...")
    if not check_port(8080):
        print("Error: Port 8080 is not listening!")
        return False
    
    try:
        print("Attempting connection through proxy...")
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        session.proxies = proxies
        
        response = session.get(
            "https://api.binance.com/api/v3/time",
            verify=False,
            timeout=10
        )
        print(f"Response received: {response.text}")
        return True
        
    except Exception as e:
        print(f"Connection error: {str(e)}")
        return False
