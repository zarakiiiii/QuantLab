from strategies.base import Strategy
import numpy as np
import pandas as pd

class EMACrossStrategy(Strategy):

    def __init__(self,fast_ema,slow_ema):
        self.fast_ema = fast_ema
        self.slow_ema = slow_ema

    def generate_signals(self, df: pd.DataFrame) -> pd.Series:

        fast = self.fast_ema.calculate(df)
        slow = self.slow_ema.calculate(df)

        buy = (fast > slow) & (fast.shift(1) <= slow.shift(1))

        sell = (fast < slow) & (fast.shift(1) >= slow.shift(1))

        signals = np.where(buy,1,np.where(sell,-1,0))

        return pd.Series(
            signals,
            index=df.index,
            name="Signals"
        )

