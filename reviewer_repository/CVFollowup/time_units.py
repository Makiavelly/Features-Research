"""Explicit datetime resolution before integer conversion for temporal sampling."""
import numpy as np
import pandas as pd

def unix_seconds(values):
    series=pd.Series(values)
    if not pd.api.types.is_datetime64_any_dtype(series.dtype):
        raise TypeError('Expected datetime dtype; integer timestamp units must be specified explicitly')
    stamps=pd.to_datetime(series,utc=True).dt.as_unit('ns')
    if stamps.isna().any():raise ValueError('Missing cutoff timestamps')
    return (stamps.astype('int64').to_numpy()//1_000_000_000).astype(np.int64)
