import pandas as pd

def liquidity_filter(options_df: pd.DataFrame,
                     max_spread_pct: 0.05,
                     min_volume = 10,
                     min_open_interest = 50):
    """
    Filter options based on liquidity criteria.
    """
    df = options_df.copy()
    df['mid'] = (df['bid'] + df['ask']) / 2.0
    df['spread_pct'] = (df['ask'] - df['bid']) / df['mid'].replace(0, pd.NA)
    out = df[
        (df['volume'] >= min_volume) &
        (df['Open Interest'] >= min_open_interest) &
        (df['spread_pct'] <= max_spread_pct)
    ].dropna(subset = ['mid'])
    return out

def option_txn_cost(mid_price, bid, ask, side):
    """
    Simple fill model: cross half-spread
    side: 'buy' or 'sell' the option
    """ 
    half_spread = (ask - bid) / 2.0
    slip = half_spread if half_spread > 0 else 0.0
    return slip #cost per 1 option (multiply by contracts)
