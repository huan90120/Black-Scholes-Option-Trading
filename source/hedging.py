import pandas as pd
from source.black_scholes import black_scholes_price, delta

def as_series(x, name = 'S'):
    if isinstance(x, pd.Series):
        s = x.dropna().astype(float)
        s.name = name
        return s
    if isinstance(x, pd.DataFrame) and x.shape[1] == 1:
        s = x.iloc[:, 0].dropna().astype(float)
        s.name = name
        return s
    raise ValueError(f"{name} must be a pandas series or single-column DataFrame")

def simulate_delta_hedge(
    S, K, T_days, r, vol_series, option_type='call',
    txn_cost_bps_stock=1.0, rebalance_daily=True
):
    """
    Simulate a delta hedge for an option with given parameters.
    Parameters:
    S : pd.Series : Series of stock prices
    K : float : Strike price of the option
    T_days : int : Number of days to expiration
    r : float : Risk-free interest rate (annualized)
    vol_series : pd.Series : Series of volatilities (annualized)
    option_type : str : 'call' for call option, 'put' for put option
    txn_cost_bps_stock : float : Transaction cost in basis points for stock trades
    rebalance_daily : bool : If True, rebalance daily; otherwise, only at expiration
    Returns:
    pd.DataFrame : DataFrame with columns for stock price, option price, delta, and P&L
    """
    #inputs as Series + align
    S = as_series(S, "S")
    vol_series = as_series(vol_series, "vol_series")

    df = pd.concat([S.rename("S"), vol_series.rename("sigma")], axis=1).dropna()
    if len(df) < 2:
        raise ValueError("Not enough data in S/vol_series (need at least 2 rows).")

    #limit to option life
    df = df.iloc[:T_days+1].copy()
    if len(df) < 2:
        raise ValueError("Slice after truncation is < 2 rows. Check dte_days vs available data.")

    #time to expiry (years), counting down
    dtes = list(range(len(df)-1, -1, -1))       # e.g. 30, 29, ..., 0
    df["T"] = [max(d, 1)/252.0 for d in dtes]   # keep >= 1 trading day

    #theoretical option price & delta
    df["opt"] = [
        black_scholes_price(s, K, t, r, sig, option_type)
        for s, t, sig in zip(df["S"], df["T"], df["sigma"])
    ]
    df["delta"] = [
        delta(s, K, t, r, sig, option_type)
        for s, t, sig in zip(df["S"], df["T"], df["sigma"])
    ]

    #hedge mechanics
    df["dS"] = df["S"].diff().fillna(0.0)
    df["delta_prev"] = df["delta"].shift(1).fillna(0.0)
    df["rehedge"] = df["delta"] - df["delta_prev"]
    df["stock_tc"] = (df["rehedge"].abs() * df["S"]) * (txn_cost_bps_stock/10000.0)

    #P&L legs
    df["opt_pnl"] = df["opt"].diff().fillna(0.0)
    df["hedge_pnl"] = -df["delta_prev"] * df["dS"]

    #final P&L
    required = ["opt_pnl", "hedge_pnl", "stock_tc"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise RuntimeError(f"Internal error: missing columns {missing}. df.columns={list(df.columns)}")

    df["pnl"] = df["opt_pnl"] + df["hedge_pnl"] - df["stock_tc"]

    return df[["S","sigma","T","opt","delta","stock_tc","opt_pnl","hedge_pnl","pnl"]]
