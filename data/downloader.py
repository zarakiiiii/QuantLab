import pandas as pd
import yfinance as yf
from pathlib import Path

class DataDownloader:
    def __init__(self):
        self.cache_folder = Path("data/cache")
        self.cache_folder.mkdir(parents=True, exist_ok=True)
    def get_data(self,ticker: str,start_date: str,end_date: str) -> pd.DataFrame:
        cache_file = self.cache_folder / f"{ticker}.csv"

        if cache_file.exists():
            print(f"Loading {ticker} from cache...")
            df = self._load_cache(ticker)
        else:
            print(f"Downloading {ticker} from Yahoo Finance...")
            df = self._download(ticker, start_date, end_date)
            self._save_cache(df, ticker)
        df = df.loc[start_date:end_date]

        return df
    def _normalize_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        df = df.sort_index()
        return df
    def _download(self, ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
        

        df = yf.download(
            ticker,
            start = start_date,
            end = end_date,
            progress=False
        )

        df = self._normalize_dataframe(df)
        

        if df.empty:
            raise ValueError(f"No data found for {ticker}")
        return df

    def _save_cache(self, df: pd.DataFrame,ticker: str):

        cache_file = self.cache_folder / f"{ticker}.csv"
        df.to_csv(cache_file)

    def _load_cache(self,ticker: str) -> pd.DataFrame:
        cache_file = self.cache_folder / f"{ticker}.csv"

        return pd.read_csv(
            cache_file,
            index_col=0,
            parse_dates=True
        ) 