import pandas as pd
import numpy as np

def ensure_series(close):
    if isinstance(close, pd.DataFrame):
        if close.shape[1] != 1:
            raise ValueError("close must be a series or a single-column DataFrame")
        close = close.iloc[:, 0]
    return close.astype(float)

def realized_vol(close: pd.Series, window = 21):
    close = ensure_series(close)
    rets = close.pct_change().dropna()
    vol = rets.rolling(window).std() * np.sqrt(252)
    vol.name = f"rv_{window}"
    return vol

def ewma_vol(close: pd.Series, lam = 0.94):
    close = ensure_series(close)
    rets = close.pct_change().dropna()
    ewma_var = rets.pow(2).ewm(alpha  = (1 - lam)).mean()
    ewma_std = np.sqrt(ewma_var)
    vol = ewma_std * np.sqrt(252)
    vol.name = f"ewma_{lam}"
    return vol

