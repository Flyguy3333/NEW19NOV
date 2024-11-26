import json
import websockets
import asyncio
import logging
from datetime import datetime
import socket
import socks
from typing import Optional, Callable, Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BinanceWebsocketClient:
    def __init__(self, proxy_host='127.0.0.1', proxy_port=8080):
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.ws_url = "wss://stream.binance.com:9443/ws"
        self.subscriptions = {}
        self.running = False
        
        # Configure SOCKS proxy for websockets
        socks.set_default_proxy(socks.SOCKS5, proxy_host, proxy_port)
        socket.socket = socks.socksocket

    async def connect(self) -> None:
        """Establish websocket connection through SOCKS proxy"""
        self.running = True
        while self.running:
            try:
                async with websockets.connect(self.ws_url) as websocket:
                    logger.info("WebSocket connected")
                    
                    # Resubscribe to all active streams
                    if self.subscriptions:
                        await self._subscribe_all(websocket)
                    
                    while self.running:
                        try:
                            message = await websocket.recv()
                            await self._handle_message(json.loads(message))
                        except websockets.ConnectionClosed:
                            logger.warning("WebSocket connection closed")
                            break
                        except Exception as e:
                            logger.error(f"Error handling message: {e}")
                            
            except Exception as e:
                logger.error(f"WebSocket connection error: {e}")
                if self.running:
                    await asyncio.sleep(5)  # Wait before reconnecting
                    
    async def _subscribe_all(self, websocket) -> None:
        """Resubscribe to all active streams after reconnection"""
        for stream, callback in self.subscriptions.items():
            await self._subscribe(websocket, stream)

    async def _subscribe(self, websocket, stream: str) -> None:
        """Subscribe to a specific stream"""
        subscribe_message = {
            "method": "SUBSCRIBE",
            "params": [stream],
            "id": len(self.subscriptions)
        }
        await websocket.send(json.dumps(subscribe_message))

    async def _handle_message(self, message: Dict[str, Any]) -> None:
        """Handle incoming websocket messages"""
        if 'stream' in message and message['stream'] in self.subscriptions:
            await self.subscriptions[message['stream']](message['data'])

    def add_symbol_ticker(self, symbol: str, callback: Callable) -> None:
        """Subscribe to real-time ticker updates for a symbol"""
        stream = f"{symbol.lower()}@ticker"
        self.subscriptions[stream] = callback

    def add_symbol_miniticker(self, symbol: str, callback: Callable) -> None:
        """Subscribe to mini ticker updates for a symbol"""
        stream = f"{symbol.lower()}@miniTicker"
        self.subscriptions[stream] = callback

    def add_symbol_bookticker(self, symbol: str, callback: Callable) -> None:
        """Subscribe to order book ticker updates"""
        stream = f"{symbol.lower()}@bookTicker"
        self.subscriptions[stream] = callback

    def stop(self) -> None:
        """Stop the websocket client"""
        self.running = False
