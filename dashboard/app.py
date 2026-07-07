import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.title("QuantLab Dashboard")

st.write("Quantitative Research & Backtesting Platform")

from data.downloader import DataDownloader
from indicators.ema import EMAIndicator
from strategies.ema_cross import EMACrossStrategy
from backtester.backtester import Backtester

ticker = st.sidebar.text_input(
    "Ticker",
    "AAPL" 
)

fast_period = st.sidebar.number_input(
    "Fast EMA",
    value=20
)

slow_period = st.sidebar.number_input(
    "Slow EMA",
    value=50
)

start_date = st.sidebar.text_input(
    "Start Date",
    "2020-01-01"
)

end_date = st.sidebar.text_input(
    "End Date",
    "2024-01-01"
)

run_button = st.sidebar.button(
    "Run Backtest"
)

if run_button:

    downloader = DataDownloader()

    df = downloader.get_data(
        ticker=ticker,
        start_date=start_date,
        end_date=end_date
    )

    fast = EMAIndicator(fast_period)
    slow = EMAIndicator(slow_period)

    strategy = EMACrossStrategy(fast,slow)

    signals = strategy.generate_signals(df)

    backtester = Backtester(initial_cash=100000)

    results = backtester.run(
        df, signals
    )

    #displaying metrics now
    col1,col2,col3 = st.columsn(3)
    with col1:
     st.metric("Total Return",
              f"{results['total_return']:.2f}%"
              )
    with col2:
     st.metric("CAGR",
              f"{results['cagr']:.2f}%"
              )
    with col3:
     st.metric(
    "Sharpe Ratio",
    f"{results['sharpe_ratio']:.2f}"
    )
    
    col4,col5,col6 = st.columns(3)

    with col4:
     st.metric(
    "Volatility",
    f"{results['volatility']*100:.2f}%"
    )
    
    with col5:
     st.metric(
    "Max Drawdown",
    f"{results['max_drawdown']:.2f}%"
    )
    with col6:
     st.metric(
    "Number of Trades",
    results["num_trades"]
    )



    st.subheader("Portfolio Equity Curve")
    st.line_chart(results["equity_curve"])

    df["EMA Fast"] = fast.calculate(df)
    df["EMA Slow"] = slow.calculate(df)

    st.subheader("Price & Moving Averages")

    st.line_chart(df[["Close", "EMA Fast", "EMA Slow"]]
    )

    #adding buy/sell markers
    st.subheader("Buy & Sell signals dashboard")
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["Close"],
            name="Close"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["EMA Fast"],
            name="EMA Fast"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["EMA Slow"],
            name="EMA Slow"   
        )
    )

    buy_points = df[signals == 1]

    fig.add_trace(
        go.Scatter(
            x=buy_points["Close"],
            mode="markers",
            name="Buy",
            marker=dict(
                symbol="triangle-up",
                size=12
            )
        )
    )

    sell_points = df[signals == -1]

    fig.add_trace(
        go.Scatter(
            x=sell_points.index,
            y=sell_points["Close"],
            mode="markers",
            name="Sell",
            marker=dict(
                symbol="triangle-down",
                size=12
            )
        )
    )

    st.plotly_chart(fig)

    st.subheader("Trade History")
    

    trade_df = pd.DataFrame(results["trade_log"])
    trade_df["buy_date"] = trade_df["buy_date"].dt.date
    trade_df["sell_date"] = trade_df["sell_date"].dt.date

    trade_df["buy_price"] = trade_df["buy_price"].round(2)
    trade_df["sell_date"] = trade_df["sell_date"].round(2)
    trade_df["profit"] = trade_df["profit"].round(2)
    trade_df["shares"] = trade_df["shares"].astype(int)

    st.dataframe(trade_df)

    st.dataframe(
        results["trade_log"]
    )

