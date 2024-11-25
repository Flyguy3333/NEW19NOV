import requests
import pandas as pd
import json
from typing import List, Dict

class BinanceFuturesPairsFetcher:
    def __init__(self):
        # Using testnet URL instead of main network
        self.base_url = "https://testnet.binancefuture.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0',
            'Accept': 'application/json'
        }
        # Optional proxy configuration
        self.proxies = {
            'http': 'http://proxy.server:3128',
            'https': 'http://proxy.server:3128'
        }

    def get_futures_usdt_pairs(self) -> List[Dict]:
        """Fetch all USDT-M futures trading pairs from Binance."""
        try:
            # Try multiple endpoints
            endpoints = [
                "/fapi/v1/exchangeInfo",
                "/api/v3/exchangeInfo",
                "/v2/public/instruments/info"
            ]
            
            for endpoint in endpoints:
                try:
                    print(f"Trying endpoint: {endpoint}")
                    url = f"{self.base_url}{endpoint}"
                    print(f"Full URL: {url}")
                    
                    response = requests.get(
                        url,
                        headers=self.headers,
                        timeout=10,
                        verify=False  # Only for testing
                    )
                    
                    print(f"Status Code: {response.status_code}")
                    print(f"Response: {response.text[:200]}...")  # Print first 200 chars
                    
                    if response.status_code == 200:
                        data = response.json()
                        if 'symbols' in data:
                            break
                except Exception as e:
                    print(f"Error with endpoint {endpoint}: {e}")
                    continue

            usdt_pairs = []
            if 'symbols' in data:
                for symbol in data['symbols']:
                    if (symbol.get('quoteAsset') == 'USDT' and 
                        symbol.get('status') == 'TRADING'):
                        
                        usdt_pairs.append({
                            'symbol': symbol.get('symbol'),
                            'base_asset': symbol.get('baseAsset'),
                            'quote_asset': symbol.get('quoteAsset')
                        })
            
            # If no pairs found, try alternative method
            if not usdt_pairs:
                print("Trying alternative method to get pairs...")
                # Get ticker prices instead
                ticker_url = f"{self.base_url}/fapi/v1/ticker/price"
                response = requests.get(
                    ticker_url,
                    headers=self.headers,
                    timeout=10,
                    verify=False
                )
                
                if response.status_code == 200:
                    tickers = response.json()
                    for ticker in tickers:
                        if ticker['symbol'].endswith('USDT'):
                            symbol = ticker['symbol']
                            usdt_pairs.append({
                                'symbol': symbol,
                                'base_asset': symbol[:-4],
                                'quote_asset': 'USDT'
                            })

            return usdt_pairs
            
        except Exception as e:
            print(f"Unexpected error: {e}")
            return []

    def create_pairs_dataframe(self, pairs: List[Dict]) -> pd.DataFrame:
        """Convert pairs list to a pandas DataFrame."""
        if not pairs:
            return pd.DataFrame()
        
        df = pd.DataFrame(pairs)
        return df.sort_values('symbol')

def main():
    try:
        print("Initializing...")
        fetcher = BinanceFuturesPairsFetcher()
        
        print("Fetching USDT Futures pairs...")
        pairs = fetcher.get_futures_usdt_pairs()
        
        if not pairs:
            print("No pairs found or error occurred")
            # Try hardcoding some common pairs as fallback
            pairs = [
                {'symbol': 'BTCUSDT', 'base_asset': 'BTC', 'quote_asset': 'USDT'},
                {'symbol': 'ETHUSDT', 'base_asset': 'ETH', 'quote_asset': 'USDT'},
                {'symbol': 'BNBUSDT', 'base_asset': 'BNB', 'quote_asset': 'USDT'},
                # Add more common pairs here
            ]
            print("Using fallback pairs list...")
        
        df = fetcher.create_pairs_dataframe(pairs)
        print(f"\nTotal number of USDT Futures pairs: {len(df)}")
        print("\nAll USDT Futures trading pairs:")
        print(df)
        
        csv_filename = 'binance_futures_usdt_pairs.csv'
        df.to_csv(csv_filename, index=False)
        print(f"\nPairs saved to {csv_filename}")
        
    except Exception as e:
        print(f"Error in main: {e}")

if __name__ == "__main__":
    main()
