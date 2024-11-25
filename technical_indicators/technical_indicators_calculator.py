import pandas as pd
import numpy as np
import ta
from typing import Dict, List
import requests
from datetime import datetime, timedelta

class TechnicalIndicatorsCalculator:
    def __init__(self):
        self.base_url = "https://testnet.binancefuture.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0',
            'Accept': 'application/json'
        }

    def fetch_historical_data(self, symbol: str, interval: str = '1h', limit: int = 500) -> pd.DataFrame:
        """Fetch historical OHLCV data from Binance Futures."""
        try:
            endpoint = "/fapi/v1/klines"
            params = {
                'symbol': symbol,
                'interval': interval,
                'limit': limit
            }
            
            response = requests.get(
                f"{self.base_url}{endpoint}",
                params=params,
                headers=self.headers
            )
            
            if response.status_code == 200:
                data = response.json()
                df = pd.DataFrame(data, columns=[
                    'timestamp', 'open', 'high', 'low', 'close', 'volume',
                    'close_time', 'quote_volume', 'trades', 'taker_buy_base',
                    'taker_buy_quote', 'ignore'
                ])
                
                # Convert types
                df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
                for col in ['open', 'high', 'low', 'close', 'volume']:
                    df[col] = df[col].astype(float)
                
                return df
            else:
                print(f"Error fetching data for {symbol}: {response.text}")
                return None
                
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            return None

    def calculate_indicators(self, df: pd.DataFrame) -> Dict:
        """Calculate all technical indicators."""
        try:
            indicators = {}
            
            # Trend Indicators
            indicators['sma_20'] = ta.trend.sma_indicator(df['close'], window=20)
            indicators['ema_50'] = ta.trend.ema_indicator(df['close'], window=50)
            
            # MACD
            macd = ta.trend.MACD(df['close'])
            indicators['macd'] = macd.macd()
            indicators['macd_signal'] = macd.macd_signal()
            indicators['macd_diff'] = macd.macd_diff()
            
            # Bollinger Bands
            bb = ta.volatility.BollingerBands(df['close'])
            indicators['bb_high'] = bb.bollinger_hband()
            indicators['bb_mid'] = bb.bollinger_mavg()
            indicators['bb_low'] = bb.bollinger_lband()
            
            # RSI
            indicators['rsi'] = ta.momentum.RSIIndicator(df['close']).rsi()
            
            # Stochastic
            stoch = ta.momentum.StochasticOscillator(df['high'], df['low'], df['close'])
            indicators['stoch_k'] = stoch.stoch()
            indicators['stoch_d'] = stoch.stoch_signal()
            
            # Volume Indicators
            indicators['obv'] = ta.volume.OnBalanceVolumeIndicator(df['close'], df['volume']).on_balance_volume()
            indicators['mfi'] = ta.volume.MoneyFlowIndicator(df['high'], df['low'], df['close'], df['volume']).money_flow_index()
            
            # Volatility Indicators
            indicators['atr'] = ta.volatility.AverageTrueRange(df['high'], df['low'], df['close']).average_true_range()
            
            # Custom Calculations for remaining indicators
            # Hull Moving Average
            def hull_moving_average(price, window=20):
                half_window = window // 2
                sqrt_window = int(np.sqrt(window))
                weighted_ma = ta.trend.wma_indicator(price, window)
                half_weighted_ma = ta.trend.wma_indicator(price, half_window)
                raw_hma = 2 * half_weighted_ma - weighted_ma
                return ta.trend.wma_indicator(raw_hma, sqrt_window)
            
            indicators['hma'] = hull_moving_average(df['close'])
            
            # Add more custom indicators here...
            
            return indicators
            
        except Exception as e:
            print(f"Error calculating indicators: {e}")
            return {}

    def process_all_pairs(self, pairs_df: pd.DataFrame) -> pd.DataFrame:
        """Process all trading pairs and calculate their indicators."""
        results = []
        
        for idx, row in pairs_df.iterrows():
            symbol = row['symbol']
            print(f"Processing {symbol}... ({idx + 1}/{len(pairs_df)})")
            
            # Fetch historical data
            df = self.fetch_historical_data(symbol)
            if df is not None and not df.empty:
                # Calculate indicators
                indicators = self.calculate_indicators(df)
                if indicators:
                    # Get the latest values
                    latest = {k: v.iloc[-1] if not v.empty else None for k, v in indicators.items()}
                    latest['symbol'] = symbol
                    latest['timestamp'] = df['timestamp'].iloc[-1]
                    results.append(latest)
            
            # Add delay to avoid API rate limits
            time.sleep(0.5)
        
        return pd.DataFrame(results)

def main():
    # Load the pairs from CSV
    pairs_df = pd.read_csv('binance_futures_usdt_pairs.csv')
    
    # Initialize calculator
    calculator = TechnicalIndicatorsCalculator()
    
    # Process all pairs
    results_df = calculator.process_all_pairs(pairs_df)
    
    # Save results
    results_df.to_csv('technical_indicators_results.csv', index=False)
    print("\nResults saved to technical_indicators_results.csv")
    
    # Display summary
    print("\nSummary of calculated indicators:")
    print(results_df.describe())

if __name__ == "__main__":
    main()
