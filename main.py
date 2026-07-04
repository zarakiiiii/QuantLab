from data.downloader import DataDownloader

downloader = DataDownloader()

df = downloader.get_data(
    ticker="AAPL",
    start_date="2020-01-01",
    end_date="2024-01-01"
)

print(df.head())