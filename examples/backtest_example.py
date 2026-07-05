from data.downloader import DataDownloader
from indicators.ema import EMAIndicator
from strategies.ema_cross import EMACrossStrategy
from backtester.backtester import Backtester


downloader = DataDownloader()

df = downloader.get_data(
    ticker = "AAPL",
    start_date="2020-01-01",
    end_date="2024-01-01"
)

fast = EMAIndicator(20)
slow = EMAIndicator(50)

strategy = EMACrossStrategy(fast, slow)

signals = strategy.generate_signals(df)

backtester = Backtester(initial_cash=100000)

results = backtester.run(df, signals)


print(results)

