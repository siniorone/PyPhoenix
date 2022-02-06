import talib
import pandas as pd


# Standard deviation of the last n values of src
def stdev(src, n):
    return talib.STDDEV(src, n)


# Linear regression of the last n values of src
def linreg(src, n):
    return talib.LINEARREG(src, n)


# Simple moving average of the last n values of src
def sma(src, n):
    return talib.SMA(src, n)


# exponential moving average of the last n values of src
def ema(src, n):
    return talib.EMA(src, n)


# relative strength index (RSI) of the last n values of src
def rsi(src, n):
    return talib.RSI(src, n)


# Calculate RSI with two Series.
def rsi2(u, d):
    return 100 - 100 / (1 + u / d)


# reletive strength index (RSI) of the last (period) values of dataframe
def rsi_(df, periods=14, ema=True):
    """
    Returns a pd.Series with the relative strength index.
    """
    close_delta = df.diff()
    # Make two series: one for lower closes and one for higher closes
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)

    if ema is True:
        # Use exponential moving average
        ma_up = up.ewm(com=periods-1, adjust=True, min_periods=periods).mean()
        ma_down = down.ewm(com=periods-1, adjust=True, min_periods=periods).mean()
    else:
        # Use simple moving average
        ma_up = up.rolling(window=periods, adjust=False).mean()
        ma_down = down.rolling(window=periods, adjust=False).mean()

    rsi = ma_up / ma_down
    rsi = 100 - (100/(1 + rsi))
    return rsi


# Change of each element of scr from the previous y elements
def change(src, y=1):
    mysrc = src.copy()
    for i in range(len(src)):
        if i < y:
            mysrc[i] = 0
        if i > 0:
            mysrc[i] = src[i] - src[i-y]
    return mysrc


# sum of the last (lenght) elements of src
def sum_(src: pd.DataFrame, length: int) -> int:
    return sum(src[len(src)-length:])


# sliding sum of last (lenght) elements of src
def sliding_sum(src, lenght):
    mysrc = src.copy()
    for i in range(len(src)):
        if i < lenght:
            mysrc[i] = 0
        if i > 0:
            mysrc[i] = sum_(src[i-lenght:i], lenght)
    return mysrc


# Find th highest value of src in the last (length) elements
def highest(src, length):
    mysrc = src.copy()
    for i in range(len(src)):
        if i == 0:
            mysrc[i] = 0
        elif i < length:
            mysrc[i] = max(src[0:i])
        elif i > length:
            mysrc[i] = max(src[i-length:i])
    return mysrc


# Find the lowest value of src in the last (length) elements
def lowest(src, length):
    mysrc = src.copy()
    for i in range(len(src)):
        if i == 0:
            mysrc[i] = 0
        elif i < length:
            mysrc[i] = min(src[0:i])
        elif i > length:
            mysrc[i] = min(src[i-length:i])
    return mysrc


# Double smoothed
def double_smooth(src, long, short):
    fist_smooth = ema(src, long)
    return ema(fist_smooth, short)


# True strength index. It uses moving averages of the underlying momentum of a financial instrument.
def tsi(src, short, long):
    pc = change(src)
    double_smoothed_pc = double_smooth(pc, long, short)
    double_smoothed_abs_pc = double_smooth(pc.abs(), long, short)
    tsi_value = (double_smoothed_pc / double_smoothed_abs_pc)
    return tsi_value


# Calculates average of all given series (elementwise).
def avg(*args):
    return sum(args) / len(args)
