import pandas as pd
import os
from typing import List, Dict
import glob

class IndicatorVerifier:
    def __init__(self, data_dir: str = 'data'):
        self.data_dir = data_dir

    def check_files(self) -> Dict:
        """Check all saved indicator files."""
        stats = {
            'total_files': 0,
            'processed_pairs': [],
            'missing_indicators': [],
            'empty_files': [],
            'error_files': []
        }

        # Get all CSV files
        csv_files = glob.glob(os.path.join(self.data_dir, '*_indicators.csv'))
        stats['total_files'] = len(csv_files)

        for file in csv_files:
            symbol = file.split('/')[-1].replace('_indicators.csv', '')
            try:
                df = pd.read_csv(file)
                
                if df.empty:
                    stats['empty_files'].append(symbol)
                    continue

                # Check for required columns
                required_indicators = [
                    'SMA_20', 'EMA_50', 'RSI', 'MACD', 'MACD_signal',
                    'BB_upper', 'BB_middle', 'BB_lower', 'STOCH_K', 'STOCH_D',
                    'ATR', 'OBV', 'MFI', 'CCI'
                ]

                missing = [ind for ind in required_indicators if ind not in df.columns]
                if missing:
                    stats['missing_indicators'].append({
                        'symbol': symbol,
                        'missing': missing
                    })

                stats['processed_pairs'].append({
                    'symbol': symbol,
                    'rows': len(df),
                    'indicators': len(df.columns),
                    'date_range': f"{df['timestamp'].iloc[0]} to {df['timestamp'].iloc[-1]}"
                })

            except Exception as e:
                stats['error_files'].append({
                    'symbol': symbol,
                    'error': str(e)
                })

        return stats

    def generate_report(self, stats: Dict) -> None:
        """Generate a detailed verification report."""
        print("\n=== INDICATOR VERIFICATION REPORT ===")
        print(f"\nTotal files processed: {stats['total_files']}")
        
        print("\n=== PROCESSED PAIRS ===")
        df_processed = pd.DataFrame(stats['processed_pairs'])
        if not df_processed.empty:
            print(df_processed.to_string())
        
        if stats['empty_files']:
            print("\n=== EMPTY FILES ===")
            for symbol in stats['empty_files']:
                print(f"- {symbol}")
        
        if stats['missing_indicators']:
            print("\n=== MISSING INDICATORS ===")
            for item in stats['missing_indicators']:
                print(f"\n{item['symbol']}:")
                for ind in item['missing']:
                    print(f"  - {ind}")
        
        if stats['error_files']:
            print("\n=== ERROR FILES ===")
            for item in stats['error_files']:
                print(f"\n{item['symbol']}:")
                print(f"  Error: {item['error']}")

        # Save report to file
        with open('verification_report.txt', 'w') as f:
            f.write("=== INDICATOR VERIFICATION REPORT ===\n")
            f.write(f"\nTotal files processed: {stats['total_files']}\n")
            f.write("\n=== PROCESSED PAIRS ===\n")
            f.write(df_processed.to_string())
            
            if stats['empty_files']:
                f.write("\n\n=== EMPTY FILES ===\n")
                for symbol in stats['empty_files']:
                    f.write(f"- {symbol}\n")
            
            if stats['missing_indicators']:
                f.write("\n=== MISSING INDICATORS ===\n")
                for item in stats['missing_indicators']:
                    f.write(f"\n{item['symbol']}:\n")
                    for ind in item['missing']:
                        f.write(f"  - {ind}\n")
            
            if stats['error_files']:
                f.write("\n=== ERROR FILES ===\n")
                for item in stats['error_files']:
                    f.write(f"\n{item['symbol']}:\n")
                    f.write(f"  Error: {item['error']}\n")

def main():
    verifier = IndicatorVerifier()
    stats = verifier.check_files()
    verifier.generate_report(stats)
    print("\nVerification complete! Check verification_report.txt for full details.")

if __name__ == "__main__":
    main()
