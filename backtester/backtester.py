class Backtester:

    def __init__(self,initial_cash=100000):
        self.initial_cash = initial_cash

    def run(self, df, signals) -> dict:
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

            elif current_signal == -1 and holding_stock:
                cash = shares*current_price
                shares=0
                holding_stock = False
                  
        last_price = df["Close"].iloc[-1]
        if holding_stock:
            final_portfolio = cash + shares*df["Close"].iloc[-1]

        else:
           final_portfolio = cash

        total_return = (
            final_portfolio-self.initial_cash) / self.initial_cash * 100
            
        return {
            "final_portfolio": final_portfolio,
            "total_return": total_return,
            "num_trades": num_trades
        }
    

    
            
