from data.downloader import DataDownloader
from indicators.ema import EMAIndicator

downloader = DataDownloader()

df = downloader.get_data(
    "AAPL",
    "2020-01-01",
    "2024-01-01"
)

ema20 = EMAIndicator(period=20)

df["EMA20"]=ema20.calculate(df)

print(df.head())