import asyncio
import pexpect
import subprocess
import time
from datetime import datetime
import logging
import websockets
import json
import socks
import socket

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BinanceWebsocketClient:
    def __init__(self, proxy_host='127.0.0.1', proxy_port=8080):
        self.ws_url = "wss://stream.binance.com:9443/ws"
        self.running = False
        self.market_data = {}
        
        # Configure SOCKS proxy
        socks.set_default_proxy(socks.SOCKS5, proxy_host, proxy_port)
        socket.socket = socks.socksocket

    async def connect(self, symbols):
        self.running = True
        subscription_message = {
            "method": "SUBSCRIBE",
            "params": [f"{symbol.lower()}@ticker" for symbol in symbols],
            "id": 1
        }
        
        while self.running:
            try:
                async with websockets.connect(self.ws_url) as ws:
                    logger.info("WebSocket connected")
                    await ws.send(json.dumps(subscription_message))
                    
                    while self.running:
                        try:
                            message = await ws.recv()
                            await self.handle_message(json.loads(message))
                        except websockets.ConnectionClosed:
                            logger.warning("WebSocket connection closed")
                            break
                        
            except Exception as e:
                logger.error(f"WebSocket error: {e}")
                if self.running:
                    await asyncio.sleep(5)

    async def handle_message(self, message):
        if 'e' in message and message['e'] == '24hrTicker':
            symbol = message['s']
            self.market_data[symbol] = {
                'price': float(message['c']),
                'high': float(message['h']),
                'low': float(message['l']),
                'volume': float(message['v']),
                'change': float(message['P']),
                'time': datetime.now().strftime('%H:%M:%S')
            }
            self.display_market_data()

    def display_market_data(self):
        print("\033[2J\033[H")  # Clear screen
        print(f"=== Real-time Binance Market Data (Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ===\n")
        
        for symbol, data in sorted(self.market_data.items()):
            print(f"{symbol}:")
            print(f"  Price: ${data['price']:,.2f}")
            print(f"  24h Change: {data['change']:+.2f}%")
            print(f"  24h High: ${data['high']:,.2f}")
            print(f"  24h Low: ${data['low']:,.2f}")
            print(f"  Volume: {data['volume']:,.2f}")
            print()

    def stop(self):
        self.running = False

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

async def main():
    # Kill any existing tunnels
    subprocess.run(['pkill', '-f', 'ssh -D 8080'])
    time.sleep(2)
    
    # Setup tunnel
    tunnel = setup_tunnel()
    if not tunnel:
        logger.error("Failed to create tunnel")
        return
        
    try:
        client = BinanceWebsocketClient()
        symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'XRPUSDT']
        
        # Start WebSocket connection
        await client.connect(symbols)
        
    except KeyboardInterrupt:
        logger.info("\nClosing connections...")
        client.stop()
        tunnel.close()
        subprocess.run(['pkill', '-f', 'ssh -D 8080'])
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        if tunnel:
            tunnel.close()
        subprocess.run(['pkill', '-f', 'ssh -D 8080'])

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExiting...")
