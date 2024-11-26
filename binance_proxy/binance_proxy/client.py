import time
from urllib3.contrib.socks import SOCKSProxyManager
import json
import logging
from typing import Optional, Dict, Any, Union

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BinanceClient:
    def __init__(self, proxy_host='127.0.0.1', proxy_port=8080):
        self.proxy_url = f"socks5h://{proxy_host}:{proxy_port}"
        self.proxy = SOCKSProxyManager(self.proxy_url)
        self.base_url = 'https://api.binance.com'
        self.max_retries = 3
        self.retry_delay = 1

    def _request(self, 
                method: str, 
                endpoint: str, 
                params: Optional[Dict] = None,
                retry_count: int = 0) -> Optional[Dict[str, Any]]:
        """
        Make a request to Binance API with retry logic
        """
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.proxy.request(
                method,
                url,
                fields=params,
                timeout=10.0
            )
            return json.loads(response.data.decode())
        except Exception as e:
            if retry_count < self.max_retries:
                logger.warning(f"Request failed, retrying ({retry_count + 1}/{self.max_retries}): {e}")
                time.sleep(self.retry_delay)
                return self._request(method, endpoint, params, retry_count + 1)
            logger.error(f"Request failed after {self.max_retries} retries: {e}")
            return None

    def get_server_time(self) -> Optional[Dict[str, int]]:
        """Get Binance server time"""
        return self._request('GET', '/api/v3/time')

    def get_exchange_info(self) -> Optional[Dict]:
        """Get exchange trading rules and symbol information"""
        return self._request('GET', '/api/v3/exchangeInfo')

    def get_ticker_price(self, symbol: Optional[str] = None) -> Optional[Union[Dict, list]]:
        """
        Get latest price for a symbol or all symbols
        :param symbol: Optional trading pair symbol (e.g., 'BTCUSDT')
        :return: Price data for requested symbol(s)
        """
        params = {'symbol': symbol} if symbol else None
        return self._request('GET', '/api/v3/ticker/price', params)

    def get_24h_ticker(self, symbol: Optional[str] = None) -> Optional[Union[Dict, list]]:
        """
        Get 24 hour price change statistics
        :param symbol: Optional trading pair symbol (e.g., 'BTCUSDT')
        :return: 24h statistics for requested symbol(s)
        """
        params = {'symbol': symbol} if symbol else None
        return self._request('GET', '/api/v3/ticker/24hr', params)

    def get_klines(self, 
                   symbol: str, 
                   interval: str = '1d',
                   limit: int = 100) -> Optional[list]:
        """
        Get kline/candlestick data
        :param symbol: Trading pair symbol (e.g., 'BTCUSDT')
        :param interval: Kline interval (1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M)
        :param limit: Number of klines to return (max 1000)
        """
        params = {
            'symbol': symbol,
            'interval': interval,
            'limit': limit
        }
        return self._request('GET', '/api/v3/klines', params)

    def get_recent_trades(self, 
                         symbol: str, 
                         limit: int = 100) -> Optional[list]:
        """
        Get recent trades for a symbol
        :param symbol: Trading pair symbol (e.g., 'BTCUSDT')
        :param limit: Number of trades to return (max 1000)
        """
        params = {
            'symbol': symbol,
            'limit': limit
        }
        return self._request('GET', '/api/v3/trades', params)
