# -*- coding: utf-8 -*-
from ..utils import get_drift, get_offset, verify_series

def rsi(close, length=None, drift=None, offset=None, **kwargs):
    """Indicator: Relative Strength Index (RSI)"""
    # Validate arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 14
    drift = get_drift(drift)
    offset = get_offset(offset)

    # Calculate Result
    negative = close.diff(drift)
    positive = negative.copy()

    positive[positive < 0] = 0  # Make negatives 0 for the postive series
    negative[negative > 0] = 0  # Make postives 0 for the negative series

    positive_avg = positive.ewm(com=length, adjust=False).mean()
    negative_avg = negative.ewm(com=length, adjust=False).mean().abs()

    rsi = 100 * positive_avg / (positive_avg + negative_avg)

    # Offset
    if offset != 0:
        rsi = rsi.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        rsi.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        rsi.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    rsi.name = f"RSI_{length}"
    rsi.category = 'momentum'

    return rsi



rsi.__doc__ = \
"""Relative Strength Index (RSI)

The Relative Strength Index is popular momentum oscillator used to measure the
velocity as well as the magnitude of directional price movements.

Sources:
    https://www.tradingview.com/wiki/Relative_Strength_Index_(RSI)

Calculation:
    Default Inputs:
        length=14, drift=1
    ABS = Absolute Value
    EMA = Exponential Moving Average
    positive = close if close.diff(drift) > 0 else 0
    negative = close if close.diff(drift) < 0 else 0
    pos_avg = EMA(positive, length)
    neg_avg = ABS(EMA(negative, length))
    RSI = 100 * pos_avg / (pos_avg + neg_avg)

Args:
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 1
    drift (int): The difference period.   Default: 1
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""


from pandas import DataFrame
from ..overlap.sma import sma

def stoch_rsi(close, length=None, smoothK=None, smoothD=None, drift=None, offset=None, **kwargs):
    """Indicator: Stochastic RSI (Stoch RSI)"""
    # Validate arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 14
    smoothK = int(smoothK) if smoothK and smoothK > 0 else 3
    smoothD = int(smoothD) if smoothD and smoothD > 0 else 3

    # Calculate RSI
    data_rsi = rsi(close, length=length, drift=drift,offset=offset, **kwargs)

    # Calculate Result
    min = data_rsi.rolling(length).min()
    max = data_rsi.rolling(length).max()

    stoch_rsi = 100 * (data_rsi - min) / (max - min)

    stoch_rsi_k = sma(stoch_rsi, smoothK)
    stoch_rsi_d = sma(stoch_rsi_k, smoothD)

    stoch_rsi_k.name = f"STOCH_RSI_K_{smoothK}_{smoothD}_{length}"
    stoch_rsi_d.name = f"STOCH_RSI_D_{smoothK}_{smoothD}_{length}"

    stoch_rsi_k.category = stoch_rsi_d.category = 'momentum'

    # Prepare DataFrame to return
    data = {stoch_rsi_k.name: stoch_rsi_k, stoch_rsi_d.name: stoch_rsi_d}
    stoch_rsif = DataFrame(data)
    stoch_rsif.name = f"Stoch_RSI_{smoothK}_{smoothD}_{length}"
    stoch_rsif.category = 'momentum'

    return stoch_rsif



stoch_rsi.__doc__ = \
"""Stochastic RSI (Stoch RSI)

The Stochastic RSI indicator (Stoch RSI) is essentially an indicator of an indicator. It is used in 
technical analysis to provide a stochastic calculation to the RSI indicator. This means that it is a 
measure of RSI relative to its own high/low range over a user defined period of time.

Sources:
    https://www.tradingview.com/wiki/Stochastic_RSI_(STOCH_RSI)

Calculation:
    Default Inputs:
        length=14, drift=1
    ABS = Absolute Value
    EMA = Exponential Moving Average
    Stoch RSI = 100* (RSI - Lowest Low RSI) / (Highest High RSI - Lowest Low RSI)

Args:
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 1
    drift (int): The difference period.   Default: 1
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""