# -*- coding: utf-8 -*-
from pandas import DataFrame
from ..overlap.sma import sma
from ..utils import get_offset, verify_series

def stoch(high, low, close, fast_k=None, fast_d=None, slow_d=None, offset=None, **kwargs):
    """Indicator: Stochastic Oscillator (STOCH)"""
    # Validate arguments
    high = verify_series(high)
    low = verify_series(low)
    close = verify_series(close)
    fast_k = fast_k if fast_k and fast_k > 0 else 14
    fast_d = fast_d if fast_d and fast_d > 0 else 5
    slow_d = slow_d if slow_d and slow_d > 0 else 3
    offset = get_offset(offset)

    # Calculate Result
    lowest_low   = low.rolling(fast_k).min()
    highest_high = high.rolling(fast_k).max()

    fastk = 100 * (close - lowest_low) / (highest_high - lowest_low)
    fastd = sma(fastk, length=fast_d)

    slowd = sma(fastd, length=slow_d)

    # Offset
    if offset != 0:
        fastk = fastk.shift(offset)
        fastd = fastd.shift(offset)
        slowd = slowd.shift(offset)

    # Handle fills
    if 'fillna' in kwargs:
        fastk.fillna(kwargs['fillna'], inplace=True)
        fastd.fillna(kwargs['fillna'], inplace=True)
        slowd.fillna(kwargs['fillna'], inplace=True)
    if 'fill_method' in kwargs:
        fastk.fillna(method=kwargs['fill_method'], inplace=True)
        fastd.fillna(method=kwargs['fill_method'], inplace=True)
        slowd.fillna(method=kwargs['fill_method'], inplace=True)

    # Name and Categorize it
    fastk.name = f"STOCHF_{fast_k}"
    fastd.name = f"STOCHF_{fast_d}"
    slowd.name = f"STOCH_{slow_d}"
    fastk.category = fastd.category = slowd.category = 'momentum'

    # Prepare DataFrame to return
    data = {fastk.name: fastk, fastd.name: fastd, slowd.name: slowd}
    stochdf = DataFrame(data)
    stochdf.name = f"STOCH_{fast_k}_{fast_d}_{slow_d}"
    stochdf.category = 'momentum'

    return stochdf



stoch.__doc__ = \
"""Stochastic (STOCH)

Stochastic Oscillator is a range bound momentum indicator.  It displays the location
of the close relative to the high-low range over a period.

Sources:
    https://www.tradingview.com/wiki/Stochastic_(STOCH)

Calculation:
    Default Inputs:
        fast_k=14, fast_d=5, slow_d=3
    SMA = Simple Moving Average
    lowest_low   = low for last length periods
    highest_high = high for last length periods

    FASTK = 100 * (close - lowest_low) / (highest_high - lowest_low)
    FASTD = SMA(FASTK, fast_d)

    SLOWD = SMA(FASTD, slow_d)

Args:
    high (pd.Series): Series of 'high's
    low (pd.Series): Series of 'low's
    close (pd.Series): Series of 'close's
    fast_k (int): The Look Back period.  Default: 14
    fast_d (int): The  %D period.  Default: 5
    slow_d (int): The smooth %D period.  Default: 3
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.DataFrame: fastk, fastd, slowd columns.
"""