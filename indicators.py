import pandas as pd
import talib

def calculate_indicators(dataframe):
    """
    Calculate various technical indicators and add them as columns to the DataFrame.
    :param dataframe: pandas DataFrame with columns ['open', 'high', 'low', 'close', 'volume']
    :return: pandas DataFrame with added indicators
    """
    # Calculate moving averages
    dataframe['SMA'] = talib.SMA(dataframe['close'], timeperiod=14)
    dataframe['EMA'] = talib.EMA(dataframe['close'], timeperiod=14)

    # Relative Strength Index
    dataframe['RSI'] = talib.RSI(dataframe['close'], timeperiod=14)

    # Bollinger Bands
    dataframe['UpperBB'], dataframe['MiddleBB'], dataframe['LowerBB'] = talib.BBANDS(
        dataframe['close'], timeperiod=14, nbdevup=2, nbdevdn=2, matype=0
    )

    # Average True Range
    dataframe['ATR'] = talib.ATR(dataframe['high'], dataframe['low'], dataframe['close'], timeperiod=14)

    # MACD
    dataframe['MACD'], dataframe['MACD_Signal'], dataframe['MACD_Hist'] = talib.MACD(
        dataframe['close'], fastperiod=12, slowperiod=26, signalperiod=9
    )

    # Stochastic Oscillator
    dataframe['Stochastic_K'], dataframe['Stochastic_D'] = talib.STOCH(
        dataframe['high'], dataframe['low'], dataframe['close'], 
        fastk_period=14, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0
    )

    return dataframe
