import yfinance as yf
import pandas as pd
from loguru import logger


# Get stock data from Yahoo Finance
def get_stock_data(ticker, start_date, end_date) -> pd.DataFrame:
    """
    This function returns the stock data for the ticker
    """
    logger.info(f"Downloading data for {ticker} from {start_date} to {end_date}")
    return yf.download(ticker, start_date, end_date)
