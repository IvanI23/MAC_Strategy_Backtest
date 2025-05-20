import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

#Customize the ticker and date range to test your needs
ticker = 'AAPL' 
start = '2015-01-01'
end = '2024-12-31'

#Initialize data processing
data = yf.download(ticker, start=start, end=end)
data.to_csv(f"data/{ticker}_data.csv")
df = pd.read_csv(
    f"data/{ticker}_data.csv",
    skiprows=3,
    names=["Date", "Close", "High", "Low", "Open", "Volume"],
    header=None,
    parse_dates=["Date"],
    index_col="Date"
)

df["SMA_50"] = df["Close"].rolling(window=50).mean()
df["SMA_200"] = df["Close"].rolling(window=200).mean()

#Set up Moving Average Crossover Strategy
df["Signal"] = 0
df.loc[df["SMA_50"] > df["SMA_200"], "Signal"] = 1
df.loc[df["SMA_50"] < df["SMA_200"], "Signal"] = 0
df["Position"] = df["Signal"].diff()

#Plotting the signals
plt.figure(figsize=(14, 8))
plt.plot(df["Close"], label="Close Price", alpha=0.5)
plt.plot(df["SMA_50"], label="50-day SMA", linestyle="--")
plt.plot(df["SMA_200"], label="200-day SMA", linestyle="--")

plt.plot(df[df["Position"] == 1].index,
         df["SMA_50"][df["Position"] == 1],
         "^", markersize=10, color="green", label="Buy Signal")

plt.plot(df[df["Position"] == -1].index,
         df["SMA_50"][df["Position"] == -1],
         "v", markersize=10, color="red", label="Sell Signal")

plt.title("Moving Average Crossover Strategy")
plt.xlabel("Date")
plt.ylabel("Price ($)")
plt.legend()
plt.grid(True)
plt.show()


"""     Backtesting the strategy    """


#Initialize portfolio
initial_capital = 100000
cash = initial_capital
holding = 0
portfolio_values = []

#Simulate the strategy
for date, row in df.iterrows():
    price = row["Close"]
    position = row["Position"]

    if position == 1 and cash >= price:
        holding += cash // price
        cash -= (cash // price) * price
    elif position == -1 and holding > 0:
        cash += holding * price
        holding = 0

    portfolio_value = cash + holding * price
    portfolio_values.append(portfolio_value)

df["Strategy_Portfolio_Value"] = portfolio_values

#Simulate Buy & Hold strategy
first_price = df["Close"].iloc[0]
shares_bought = initial_capital // first_price
cash_left = initial_capital - (shares_bought * first_price)
df["BuyHold_Portfolio_Value"] = df["Close"] * shares_bought + cash_left

#Plot results
plt.figure(figsize=(14, 8))
plt.plot(df.index, df["Strategy_Portfolio_Value"], label="Strategy Value", linewidth=2)
plt.plot(df.index, df["BuyHold_Portfolio_Value"], label="Buy & Hold Value", linewidth=2, color='orange')
plt.title("Moving Average Crossover Strategy vs Buy & Hold")
plt.xlabel("Date")
plt.ylabel("Portfolio Value ($)")
plt.legend()
plt.grid(True)
plt.show()


"""     Performance Analysis    """

#Daily Returns
df["Strategy_Daily_Returns"] = df["Strategy_Portfolio_Value"].pct_change()
df["BuyHold_Daily_Returns"] = df["BuyHold_Portfolio_Value"].pct_change()

#Cumulative Returns 
cumulative_strategy_return = (df["Strategy_Portfolio_Value"].iloc[-1] / df["Strategy_Portfolio_Value"].iloc[0]) - 1
cumulative_buyhold_return = (df["BuyHold_Portfolio_Value"].iloc[-1] / df["BuyHold_Portfolio_Value"].iloc[0]) - 1

#Annualized Returns
annualized_strategy_return = (1 + df["Strategy_Daily_Returns"].mean()) ** 252 - 1
annualized_buyhold_return = (1 + df["BuyHold_Daily_Returns"].mean()) ** 252 - 1

#CAGR
cagr_strategy = (df["Strategy_Portfolio_Value"].iloc[-1] / df["Strategy_Portfolio_Value"].iloc[0]) ** (1 / ((df.index[-1] - df.index[0]).days / 365)) - 1
cagr_buyhold = (df["BuyHold_Portfolio_Value"].iloc[-1] / df["BuyHold_Portfolio_Value"].iloc[0]) ** (1 / ((df.index[-1] - df.index[0]).days / 365)) - 1

#Volatility
strategy_volatility = df["Strategy_Daily_Returns"].std() * (252 ** 0.5)
buyhold_volatility = df["BuyHold_Daily_Returns"].std() * (252 ** 0.5)

#Sharpe Ratio
risk_free_rate = 0.01
sharpe_strategy = (df["Strategy_Daily_Returns"].mean() - risk_free_rate / 252) / df["Strategy_Daily_Returns"].std()
sharpe_buyhold = (df["BuyHold_Daily_Returns"].mean() - risk_free_rate / 252) / df["BuyHold_Daily_Returns"].std()

#Drawdown Analysis
df["Strategy_CumMax"] = df["Strategy_Portfolio_Value"].cummax()
df["Strategy_Drawdown"] = df["Strategy_Portfolio_Value"] / df["Strategy_CumMax"] - 1
df["BH_CumMax"] = df["BuyHold_Portfolio_Value"].cummax()
df["BH_Drawdown"] = df["BuyHold_Portfolio_Value"] / df["BH_CumMax"] - 1

#Write results to txt file
with open(f"results/{ticker}_performance_analysis.txt", "w") as f:
    f.write(f"Analysis of {ticker} from {start} to {end}\n")
    f.write("\n")
    f.write(f"Cumulative Strategy Return: {cumulative_strategy_return:.2%}\n")
    f.write(f"Cumulative Buy & Hold Return: {cumulative_buyhold_return:.2%}\n")
    f.write(f"Annualized Strategy Return: {annualized_strategy_return:.2%}\n")
    f.write(f"Annualized Buy & Hold Return: {annualized_buyhold_return:.2%}\n")
    f.write(f"CAGR Strategy: {cagr_strategy:.2%}\n")
    f.write(f"CAGR Buy & Hold: {cagr_buyhold:.2%}\n")
    f.write(f"Strategy Volatility: {strategy_volatility:.2%}\n")
    f.write(f"Buy & Hold Volatility: {buyhold_volatility:.2%}\n")
    f.write(f"Sharpe Ratio Strategy: {sharpe_strategy:.2f}\n")
    f.write(f"Sharpe Ratio Buy & Hold: {sharpe_buyhold:.2f}\n")
    f.write(f"Max Drawdown Strategy: {df['Strategy_Drawdown'].min():.2%}\n")
    f.write(f"Max Drawdown Buy & Hold: {df['BH_Drawdown'].min():.2%}\n")





