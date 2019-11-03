# -*- coding: utf-8 -*-
from ..overlap.sma import sma
from ..utils import get_offset, verify_series

def bias(close, length=None, offset=None, **kwargs):
    """Indicator: Bias (i.e Relative Deviation)"""
    # Validate Arguments
    close = verify_series(close)
    length = int(length) if length and length > 1 else 30
    offset = get_offset(offset)

    # Calculate Result
    mean = sma(close=close, length=length, **kwargs)
    bias = (close - mean) / mean

    # Offset
    if offset != 0:
        bias = bias.shift(offset)

    # Name & Category
    bias.name = f"BIAS_{length}"
    bias.category = 'statistics'

    return bias



bias.__doc__ = \
"""Bias, i.e Relative Deviation

Sources:

Calculation:
    Default Inputs:
        length=30, std=1
    SMA = Simple Moving Average
    mean = SMA(close, length)
    BIAS = (close - mean) / mean

Args:
    close (pd.Series): Series of 'close's
    length (int): It's period.  Default: 30
    offset (int): How many periods to offset the result.  Default: 0

Kwargs:
    fillna (value, optional): pd.DataFrame.fillna(value)
    fill_method (value, optional): Type of fill method

Returns:
    pd.Series: New feature generated.
"""