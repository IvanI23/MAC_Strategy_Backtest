# MAC_Strategy_Backtest

A Python script to backtest a Moving Average Crossover strategy on a selected stock, complete with strategy logic, performance visualization, and analysis.

## Strategy Logic

The Strategy uses 50-day SMA and 200-day SMA.  
Bullish signals are created when the 50-day SMA crosses above the 200-day SMA.  
Bearish signals are created when the 50-day SMA crosses below the 200-day SMA.

## Core

- Historical data retrieved from Yahoo Finance  
- Contain Buy/Sell plots  
- Strategy Simulation  
- Buy & Hold simulation  

## Performance metrics

- Cumualative returns  
- Annualised returns  
- CAGR  
- Volatility  
- Sharpe ratio  
- Max drawdown  

## Requirements

- python 3.7+  
- pandas  
- matplotlib  
- yfinance  

## Install Command

```
pip install pandas matplotlib yfinance
```
