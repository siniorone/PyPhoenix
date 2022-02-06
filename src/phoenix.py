import src.utils.finance as fi
from src.utils.dataminer import get_stock_data
from src.utils.graphly import graphly_indicator
from src.utils.graph import graph_indicator
import numpy as np
import pandas as pd
from loguru import logger


class Phoenix():
    """
    This class is used to get data from yfinance and calculate indicators and plot them.
    it also has a method to get the DataFrame of all Calculated indicators.
    """
    def __init__(self, ticker, start_date, end_date):
        """
        Initialize the class with ticker, start_date and end_date.
        """
        logger.info(f"Phoenix: {ticker} {start_date} {end_date} Created...")
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        df = get_stock_data(ticker, start_date, end_date)
        self.date = df.index
        self.open = df["Open"]
        self.high = df["High"]
        self.low = df["Low"]
        self.close = df["Close"]
        self.hl2 = (self.high + self.low) / 2  # hl2
        self.hlc3 = (self.high + self.low + self.close) / 3  # hlc3
        self.ohlc4 = (self.open + self.high + self.low + self.close) / 4  # ohlc4
        self.volume = df["Volume"]

        # Constants
        self.n1 = 9   # Phx master
        self.n2 = 6   # Phx time 1
        self.n3 = 3   # Phx time 2
        self.n4 = 32  # LSMA 1
        self.n5 = 0   # LSMA 1
        logger.info(f"Phoenix: {self.ticker} Initial Calculation...")
        self.calculate()

    def calculate(self):
        """
        This method is used to calculate all indicators.
        """
        # Calculate The Phoenix Indicator Lines
        self.wt1 = self.tradition(self.hlc3)  # Green Line
        self.wt2 = fi.sma(self.wt1, 6)  # Red RSI Line
        self.ext1 = self.wt2.copy()
        self.ext1 = self.ext1.apply(lambda x: x-10 if x < 20 else x+10 if x > 80 else np.nan)
        self.ext2 = self.ext1.dropna()  # Yellow Dots
        self.wt3 = fi.linreg(self.wt1, self.n4)  # Blue LSMA Line
        self.wt4 = fi.ema((self.wt1-self.wt2)*2+50, self.n3)  # Energy

        # Bollinger Bands Calculation
        bb_length = 20
        self.basis = fi.sma(self.close, bb_length)
        dev01 = 1.0 * fi.stdev(self.close, bb_length)
        dev02 = 1.618 * fi.stdev(self.close, bb_length)
        dev03 = 2.618 * fi.stdev(self.close, bb_length)
        dev04 = 3.618 * fi.stdev(self.close, bb_length)
        dev05 = 4.618 * fi.stdev(self.close, bb_length)
        self.upper01 = self.basis + dev01
        self.lower01 = self.basis - dev01
        self.upper02 = self.basis + dev02
        self.lower02 = self.basis - dev02
        self.upper03 = self.basis + dev03
        self.lower03 = self.basis - dev03
        self.upper04 = self.basis + dev04
        self.lower04 = self.basis - dev04
        self.upper05 = self.basis + dev05
        self.lower05 = self.basis - dev05

    def tci(self, src):
        a = (src-fi.ema(src, self.n1))
        b = (0.025 * fi.ema(abs(src - fi.ema(src, self.n1)), self.n1))
        return fi.ema(a / b, self.n2) + 50

    def mf(self, src):
        u = src.copy()
        d = src.copy()
        for i, c in enumerate(fi.change(src)):
            if c <= 0:
                u[i] = 0
            if c >= 0:
                d[i] = 0
        return fi.rsi2((self.volume * u).rolling(window=self.n3, min_periods=1).sum(),
                       (self.volume * d).rolling(window=self.n3, min_periods=1).sum())

    def willy(self, src):
        a = 60 * (src - fi.highest(src, self.n2))
        b = (fi.highest(src, self.n2) - fi.lowest(src, self.n2))
        return a / b + 80

    def csi(self, src):
        return fi.avg(fi.rsi(src, self.n3), fi.tsi(self.open, self.n1, self.n2)*50+50)

    # Phoenix Ascending" average of tci, csi, mf, willy:
    def phoenix(self, src):
        return fi.avg(self.tci(src), self.csi(src), self.mf(src), self.willy(src))

    # Tradition average of tci, mf, rsi
    def tradition(self, src):
        return fi.avg(self.tci(src), self.mf(src), fi.rsi(src, self.n3))

    
    def to_dataframe(self):
        """
        This method is used to get the DataFrame of all Calculated indicators.
        """
        logger.info(f"Phoenix: {self.ticker} DataFrameing...")
        df = pd.DataFrame(index=self.date)
        df["open"] = self.open
        df["high"] = self.high
        df["low"] = self.low
        df["close"] = self.close
        df["hl2"] = self.hl2
        df["hlc3"] = self.hlc3
        df["ohlc4"] = self.ohlc4
        df["volume"] = self.volume
        df["green"] = self.wt1
        df["red"] = self.wt2
        df["blue"] = self.wt3
        df["energy"] = self.wt4
        df["basis"] = self.basis
        df["u1std"] = self.upper01
        df["l1std"] = self.lower01
        df["u16std"] = self.upper02
        df["l16std"] = self.lower02
        df["u26std"] = self.upper03
        df["l26std"] = self.lower03
        df["u36std"] = self.upper04
        df["l36std"] = self.lower04
        df["u46std"] = self.upper05
        df["l46std"] = self.lower05
        return df

    def graph(self, **kwargs):
        """
        This method is used to plot all indicators. using plotly
        """
        logger.info(f"Phoenix: {self.ticker} Graphling...")
        logger.info(f"Phoenix: {self.ticker} Calculating...")
        self.calculate()
        graphly_indicator(self, **kwargs)

    def graph2(self, **kwargs):
        """
        This method is used to plot all indicators. using Matplotlib and seaborn
        """
        logger.info(f"Phoenix: {self.ticker} Graphling...")
        logger.info(f"Phoenix: {self.ticker} Calculating...")
        self.calculate()
        graph_indicator(self, **kwargs)
