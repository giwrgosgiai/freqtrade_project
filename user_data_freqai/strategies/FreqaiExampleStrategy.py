from freqtrade.strategy import IStrategy, merge_informative_pair
from pandas import DataFrame
import numpy as np
import talib.abstract as ta
from freqtrade.strategy.interface import IStrategy
from typing import Dict, List, Optional

class FreqaiExampleStrategy(IStrategy):
    # Ορισμός παραμέτρων στρατηγικής
    minimal_roi = {
        "0": 0.1,  # 10% κέρδος
        "60": 0.05,  # 5% κέρδος μετά από 1 ώρα
        "120": 0.01  # 1% κέρδος μετά από 2 ώρες
    }
    
    stoploss = -0.10  # 10% stop loss
    timeframe = '5m'
    
    # Προετοιμασία δεδομένων για το AI μοντέλο
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Υπολογισμός τεχνικών δεικτών
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
        dataframe['macd'], dataframe['macdsignal'], dataframe['macdhist'] = ta.MACD(dataframe)
        dataframe['ema20'] = ta.EMA(dataframe, timeperiod=20)
        
        return dataframe
    
    # Σήμα εισόδου
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (dataframe['rsi'] < 30) & 
            (dataframe['close'] < dataframe['ema20']) & 
            (dataframe['macd'] > dataframe['macdsignal']),
            'enter_long'] = 1
        
        dataframe.loc[
            (dataframe['rsi'] > 70) & 
            (dataframe['close'] > dataframe['ema20']) & 
            (dataframe['macd'] < dataframe['macdsignal']),
            'enter_short'] = 1
        
        return dataframe
    
    # Σήμα εξόδου
    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (dataframe['rsi'] > 70) | 
            (dataframe['close'] > dataframe['ema20']),
            'exit_long'] = 1
        
        dataframe.loc[
            (dataframe['rsi'] < 30) | 
            (dataframe['close'] < dataframe['ema20']),
            'exit_short'] = 1
        
        return dataframe 