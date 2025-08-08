import yfinance as yf
import pandas as pd 

def get_stock_data(ticker, start_date, end_date):
    """
    Download historical stock data from Yahoo Finance.
    
    Parameters:
    ticker: str - Stock symbol
    start_date: str - Start data in 'YYYY-MM-DD' format
    end_date: str - End date in 'YYYY-MM-DD' format
    
    Returns:
    DataFrame with 'Close' prices
    """

    df = yf.download(ticker, start = start_date, end = end_date)
    return df[['Close']]

def calculate_annualized_volatility(close_prices):
    """
    Calculate annualized historical volatility from closing prices.
    
    Parameters:
    close_prices: pandas Series
    
    ReTURNS:
    float - annualized volatility
    """

    daily_returns = close_prices.pct_change().dropna()
    daily_std = daily_returns.std()
    annualized_vol = daily_std * (252 ** 0.5)  # Assuming 252 trading days in a year
    return float(annualized_vol)

