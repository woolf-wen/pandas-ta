# -*- coding: utf-8 -*-
from ..overlap import vwap
from ..utils import get_offset, verify_series

def turning_point(high, low, close, volume, length=None, offset=None, **kwargs):
    """Indicator: Bias (i.e Relative Deviation)"""
    # Validate Arguments
    close = verify_series(close)
    length = int(length) if length and length > 1 else 30
    offset = get_offset(offset)

    # Calculate Result
    vw = vwap(high=high, low=low, close=close, volume=volume, **kwargs)
    tp = ( ((vw.shift(-1) < vw) & (vw.shift(1) < vw)) | ((vw.shift(-1) > vw) & (vw.shift(1) > vw)) ).astype(int)
    points = tp.rolling(length).sum()

    # Offset
    if offset != 0:
        points = points.shift(offset)

    # Name & Category
    points.name = f"TURNINGPOINT_{length}"
    points.category = 'statistics'

    return points
