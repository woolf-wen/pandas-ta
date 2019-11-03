# -*- coding: utf-8 -*-
from ..overlap.hlc3 import hlc3
from ..overlap.sma import sma
from ..statistics.mad import mad
from ..utils import get_offset, verify_series

def cci(high, low, close, length=None, c=None, offset=None, **kwargs):
    """Indicator: Commodity Channel Index (CCI)"""
    # Validate Arguments
    high = verify_series(high)
    low = verify_series(low)
    close = verify_series(close)
    length = int(length) if length and length > 0 else 21
    c = float(c) if c and c > 0 else 0.015
    min_periods = int(kwargs['min_periods']) if 'min_periods' in kwargs and kwargs['min_periods'] is not None else length
    offset = get_offset(offset)

    # Calculate Result
    typical_price = hlc3(high=high, low=low, close=close)
    mean_typical_price = sma(typical_price, length=length)
    mad_typical_price = mad(typical_price, length=length)

    cci = typical_price - mean_typical_price
    cci /= c * mad_typical_price

    # Offset
    if offset != 0:
        cci = cci.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        cci.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        cci.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    cci.name = f"CCI_{length}_{c}"
    cci.category = 'momentum'

    return cci



cci.__doc__ = \
"""Commodity Channel Index (CCI)

Commodity Channel Index is a momentum oscillator used to primarily identify
overbought and oversold levels relative to a mean.

Sources:
    https://www.tradingview.com/wiki/Commodity_Channel_Index_(CCI)

Calculation:
    Default Inputs:
        length=20, c=0.015
    SMA = Simple Moving Average
    MAD = Mean Absolute Deviation
    tp = typical_price = hlc3 = (high + low + close) / 3
    mean_tp = SMA(tp, length)
    mad_tp = MAD(tp, length)
    CCI = (tp - mean_tp) / (c * mad_tp)

Args:
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 20
    c (float):  Scaling Constant.  Default: 0.015
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""


from pandas import DataFrame

def stoch_cci(high, low, close, length=None, smoothK=None, smoothD=None, offset=None, **kwargs):
    """Indicator: Stochastic CCI (Stoch CCI)"""
    # Validate arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 14
    smoothK = int(smoothK) if smoothK and smoothK > 0 else 3
    smoothD = int(smoothD) if smoothD and smoothD > 0 else 3

    # Calculate CCI
    data_cci = cci(high, low, close, length=length, offset=offset, **kwargs)

    # Calculate Result
    min = data_cci.rolling(length).min()
    max = data_cci.rolling(length).max()

    stoch_cci = 100 * (data_cci - min) / (max - min)

    stoch_cci_k = sma(stoch_cci, smoothK)
    stoch_cci_d = sma(stoch_cci_k, smoothD)

    stoch_cci_k.name = f"STOCH_CCI_K_{smoothK}_{smoothD}_{length}"
    stoch_cci_d.name = f"STOCH_CCI_D_{smoothK}_{smoothD}_{length}"

    stoch_cci_k.category = stoch_cci_d.category = 'momentum'

    # Prepare DataFrame to return
    data = {stoch_cci_k.name: stoch_cci_k, stoch_cci_d.name: stoch_cci_d}
    stoch_ccif = DataFrame(data)
    stoch_ccif.name = f"Stoch_CCI_{smoothK}_{smoothD}_{length}"
    stoch_ccif.category = 'momentum'

    return stoch_ccif



stoch_cci.__doc__ = \
"""Stochastic CCI (Stoch CCI)

The Stochastic CCI indicator (Stoch CCI) is essentially an variation indicator of Stochastic RSI. It is used in 
technical analysis to provide a stochastic calculation to the RSI indicator. This means that it is a 
measure of RSI relative to its own high/low range over a user defined period of time.

Sources:
    https://www.tradingview.com/wiki/Stochastic_RSI_(STOCH_RSI)

Calculation:
    Default Inputs:
        length=14, drift=1
    ABS = Absolute Value
    EMA = Exponential Moving Average
    Stoch RSI = 100* (CCI - Lowest Low CCI) / (Highest High CCI - Lowest Low CCI)

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