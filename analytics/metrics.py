import pandas as pd
import numpy as np

def max_drawdown(equity_curve: pd.Series) -> float:
    running_max = equity_curve.cummax()
    drawdown = (
        equity_curve-running_max
        ) / running_max
    return drawdown.min()*100

def volatility(equity_curve: pd.Series) -> float:
    daily_returns = equity_curve.pct_change() 
    return daily_returns.std() * np.sqrt(252)
#252 trading days in a year, we want to report annual volatility

def sharpe_ratio(equity_curve: pd.Series) -> float:
    daily_returns = equity_curve.pct_change().dropna()

    return (
        daily_returns.mean()
        /
        daily_returns.std()
    ) * np.sqrt(252)

def cagr(
        initial_portfolio: float,
        final_portfolio: float,
        df: pd.DataFrame
) -> float:
    years = (
        df.index[-1] - df.index[0]
    ).days/365.25
    return (
           (final_portfolio / initial_portfolio) ** (1/years) 
           - 1
    )*100