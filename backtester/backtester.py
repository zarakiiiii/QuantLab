import pandas as pd
from analytics.metrics import (
    max_drawdown,
    volatility,
    sharpe_ratio,
    cagr
)
class Backtester:

    def __init__(self,initial_cash=100000):
        self.initial_cash = initial_cash

    def run(self, df, signals) -> dict:
        trade_log = []
        equity_curve = []

        cash = self.initial_cash
        shares = 0.0
        holding_stock = False
        num_trades=0

        for i in range(len(df)):
            current_price = df["Close"].iloc[i]
            current_signal = signals.iloc[i]

            if current_signal == 1 and not holding_stock:
                    shares = cash / current_price
                    cash=0
                    holding_stock = True
                    num_trades += 1
                    buy_price = current_price
                    buy_date = df.index[i]

            elif current_signal == -1 and holding_stock:
                sold_shares=shares
                cash = sold_shares*current_price
                shares=0
                holding_stock = False
                trade_log.append({
                    "buy_date": buy_date,
                    "buy_price": buy_price,
                    "sell_date": df.index[i],
                    "sell_price": current_price,
                    "shares": sold_shares,
                    "profit": (current_price - buy_price)*sold_shares
                })

            portfolio_value = cash + shares*current_price
            equity_curve.append(portfolio_value)
                  
        last_price = df["Close"].iloc[-1]
        if holding_stock:
            final_portfolio = cash + shares*last_price

        else:
           final_portfolio = cash

        total_return = (
        final_portfolio-self.initial_cash) / self.initial_cash * 100
        
        equity_curve = pd.Series(
            equity_curve,
            index=df.index,
            name="Equity Curve"
        )

        mdd = max_drawdown(equity_curve)
        vol = volatility(equity_curve)
        sharpe = sharpe_ratio(equity_curve)
        annual_cagr = cagr(self.initial_cash,final_portfolio,df)

        return {
            "final_portfolio": final_portfolio,
            "total_return": total_return,
            "num_trades": num_trades,
            "trade_log": trade_log,
            "equity_curve": equity_curve,

            "cagr": annual_cagr,
            "volatility": vol,
            "sharpe_ratio": sharpe,
            "max_drawdown": mdd
        }
    

    
            
