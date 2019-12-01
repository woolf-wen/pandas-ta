# -*- coding: utf-8 -*-
from numpy import log as nplog
from ..utils import get_offset, verify_series

def entropy(close, length=None, offset=None, **kwargs):
    """Indicator: Shannon Entropy"""
    # Validate Arguments
    close = verify_series(close)
    length = int(length) if length and length > 0 else 10
    offset = get_offset(offset)

    src = close

    # Calculate Result
    p = src / src.rolling(length).sum()
    ep = -(p * nplog(p)/nplog(2)).rolling(length).sum()

    # Offset
    if offset != 0:
        ep = ep.shift(offset)

    # Name & Category
    ep.name = f"ENTROPY_{length}"
    ep.category = 'statistics'

    return ep