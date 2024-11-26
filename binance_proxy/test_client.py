from binance_proxy.client import BinanceClient
import pexpect
import time
import subprocess
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_tunnel():
    try:
        logger.info("Starting SSH tunnel...")
        cmd = 'ssh -D 8080 -C -N -v root@138.197.180.191'
        child = pexpect.spawn(cmd, encoding='utf-8')
        
        i = child.expect(['password:', pexpect.EOF], timeout=30)
        if i == 0:
            child.sendline('jEtsrus33J')
            logger.info("Password sent, waiting for tunnel...")
            time.sleep(5)
            return child
    except Exception as e:
        logger.error(f"Tunnel error: {e}")
        return None

def format_price(price_data):
    if isinstance(price_data, dict):
        return f"{float(price_data['price']):,.2f}"
    return price_data

def main():
    # Kill any existing tunnels
    subprocess.run(['pkill', '-f', 'ssh -D 8080'])
    time.sleep(2)
    
    # Setup tunnel
    tunnel = setup_tunnel()
    if not tunnel:
        logger.error("Failed to create tunnel")
        return
        
    try:
        # Create client
        client = BinanceClient()
        
        while True:
            # Get and format current time
            server_time = client.get_server_time()
            if server_time:
                current_time = datetime.fromtimestamp(server_time['serverTime']/1000)
                print(f"\n=== Binance Data at {current_time} ===")
            
            # Get BTC price
            btc_price = client.get_ticker_price('BTCUSDT')
            if btc_price:
                print(f"BTC/USDT: ${format_price(btc_price)}")
            
            # Get ETH price
            eth_price = client.get_ticker_price('ETHUSDT')
            if eth_price:
                print(f"ETH/USDT: ${format_price(eth_price)}")
            
            # Get 24h BTC stats
            btc_24h = client.get_24h_ticker('BTCUSDT')
            if btc_24h:
                print(f"\nBTC 24h Change: {btc_24h['priceChangePercent']}%")
                print(f"BTC 24h High: ${float(btc_24h['highPrice']):,.2f}")
                print(f"BTC 24h Low: ${float(btc_24h['lowPrice']):,.2f}")
                print(f"BTC 24h Volume: {float(btc_24h['volume']):,.2f} BTC")
            
            print("\nPress CTRL+C to stop (refreshing in 5 seconds)")
            time.sleep(5)
            
    except KeyboardInterrupt:
        logger.info("\nClosing tunnel...")
        tunnel.close()
        subprocess.run(['pkill', '-f', 'ssh -D 8080'])
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        tunnel.close()
        subprocess.run(['pkill', '-f', 'ssh -D 8080'])

if __name__ == "__main__":
    main()
