import talib
import pandas as pd

def calculate_indicators(data):
    # Ensure close column is numeric
    close = data["close"].astype(float)

    # Calculate indicators
    data["SMA"] = talib.SMA(close, timeperiod=10)
    data["EMA"] = talib.EMA(close, timeperiod=10)
    data["RSI"] = talib.RSI(close, timeperiod=14)

    # MACD
    macd, macd_signal, macd_hist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    data["MACD"] = macd
    data["MACD_Signal"] = macd_signal
    data["MACD_Hist"] = macd_hist

    # ATR (Average True Range)
    high = data["high"].astype(float)
    low = data["low"].astype(float)
    data["ATR"] = talib.ATR(high, low, close, timeperiod=14)

    # Bollinger Bands
    upperband, middleband, lowerband = talib.BBANDS(close, timeperiod=20)
    data["UpperBB"] = upperband
    data["MiddleBB"] = middleband
    data["LowerBB"] = lowerband

    # Return updated DataFrame
    return data
