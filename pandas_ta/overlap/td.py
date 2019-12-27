# -*- coding: utf8 -*-
from pandas import DataFrame, Series
import numpy as np
from ..utils import get_offset, verify_series

def td(high, low, close, offset=None, **kwargs):
    """Indicator: TD (Tom Demark Indicators)"""
    # Validate Arguments
    high = verify_series(high)
    low = verify_series(low)
    close = verify_series(close)
    offset = get_offset(offset)

    # Calculate Result
    cnt = close.count()
    td_b = close.copy()
    td_s = close.copy()
    td_cd_b = close.copy()
    td_cd_s = close.copy()
    td_b[:] = td_s[:] = td_cd_b[:] = td_cd_s[:] = 0
    # setup
    for i in range(4, cnt):
        td_b.iloc[i] = td_b.iloc[i-1] + 1 if close.iloc[i] < close.iloc[i-4] else 0
        td_s.iloc[i] = td_s.iloc[i-1] - 1 if close.iloc[i] > close.iloc[i-4] else 0

        # countdown
        td_cd_b.iloc[i] = td_cd_b.iloc[i] + 1 if td_b.iloc[i] >= 9 and close.iloc[i] < low.iloc[i-2] else td_cd_b.iloc[i]
        td_cd_s.iloc[i] = td_cd_s.iloc[i] + 1 if td_s.iloc[i] >= 9 and close.iloc[i] > high.iloc[i - 2] else td_cd_s.iloc[i]

        td_cd_b.iloc[i] = 0 if td_b.iloc[i] < 9 else td_cd_b.iloc[i]
        td_cd_s.iloc[i] = 0 if td_s.iloc[i] < 9 else td_cd_s.iloc[i]

    # Offset
    if offset != 0:
        td_b = td_b.shift(offset)
        td_s = td_s.shift(offset)
        td_cd_b = td_cd_b.shift(offset)
        td_cd_s = td_cd_s.shift(offset)

    # Name and Categorize it
    td_b.name = f"TD_B"
    td_s.name = f"TD_S"
    td_cd_b.name = "TD_COUNTDOWN_B"
    td_cd_s.name = "TD_COUNTDOWN_S"
    td_b.category = td_s.category = td_cd_b.category = td_cd_s.category = 'overlap'

    # Prepare DataFrame to return
    data = {td_b.name: td_b, td_s.name: td_s, td_cd_b.name: td_cd_b, td_cd_s.name: td_cd_s}
    td = DataFrame(data)
    td.name = f"TD"
    td.category = 'overlap'

    return td