from indicators.base import Indicator
import pandas as pd

class EMAIndicator(Indicator):

    def __init__(self, period: int, column: str = "Close"):
        self.period = period
        self.column = column

    def calculate(self, df) -> pd.Series:
        close_prices = df[self.column]

        ema = close_prices.ewm(span=self.period, adjust="False").mean()
        #2 ways of ema adjust = true/false , false matches broker platforms ema
        return ema
   