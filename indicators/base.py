from abc import ABC, abstractmethod
import pandas as pd

class Indicator(ABC):

    @abstractmethod
    def calculate(self, df: pd.DataFrame) -> pd.Series:
        pass

