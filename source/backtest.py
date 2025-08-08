import numpy as np
import pandas as pd
from source.data_loader import get_stock_data, calculate_annualized_volatility
from source.rv_forecasting import realized_vol, ewma_vol
from source.hedging import simulate_delta_hedge
from source.black_scholes import black_scholes_price
from source.iv_solver import implied_vol

def synthesize_market_iv(rv_series: pd.Series, seed=42, noise_bp=120) -> pd.Series:
    """
    Simulated market IV = RV + Gaussian noise (bp = basis points; 100 bp = 1 vol point).
    """
    np.random.seed(seed)
    rv = rv_series.dropna().astype(float)
    noise = np.random.normal(0, noise_bp/10000.0, size=len(rv))
    iv = (rv.values + noise).clip(0.01, 1.5)
    return pd.Series(iv, index=rv.index, name="iv_mkt")

def build_signal_series(close: pd.Series, lam=0.94) -> pd.Series:
    """
    Your RV forecast (EWMA).
    """
    rv = ewma_vol(close, lam=lam)
    return rv

def run_mispricing_backtest(
    ticker="AAPL",
    start="2020-01-01",
    end="2024-12-31",
    r=0.03,
    dte_days=7,
    option_type='call',
    mispricing_threshold = 0.003,   # 0.3 vol points
    stock_tc_bps=1.0,
    iv_noise_bp=180,                     # more noise -> more entries
    iv_seed=42,
    allow_overlapping=True               # False = one trade per dte window
):
    """
    Backtest: whenever |IV - RV| > threshold, open a delta-hedged trade for dte_days.
    """
    #Prices (Series) on business days
    df = get_stock_data(ticker, start, end)
    close = df["Close"].asfreq("B").ffill().dropna()

    #Model vol (RV) and simulated market IV
    rv = build_signal_series(close, lam=0.94).reindex(close.index).ffill()
    iv = synthesize_market_iv(rv, seed=iv_seed, noise_bp=iv_noise_bp).reindex(close.index).ffill()

    #Mispricing signal
    diff = (iv - rv).dropna()
    # (Diagnostics – helpful while debugging)
    # print("days:", len(close), "signals above thr:", (diff.abs() > mispricing_threshold_volpts).sum())

    #Candidate entry indices (ensure enough room for dte window)
    indices = np.where(diff.abs().values > mispricing_threshold)[0]
    indices = [i for i in indices if i + dte_days < len(close)]

    trades = []
    i = 0
    while i < len(indices):
        t = indices[i]
        date = close.index[t]
        S0 = float(close.iloc[t])
        sigma_rv = float(rv.iloc[t])
        sigma_iv = float(iv.iloc[t])
        side = 'sell' if (sigma_iv - sigma_rv) > 0 else 'buy'

        #ATM-ish strike
        K = round(S0)

        #Slice the next dte_days+1 points
        S_slice   = close.iloc[t : t + dte_days + 1]
        vol_slice = rv.iloc[t : t + dte_days + 1]

        #Simulate delta-hedged P&L using YOUR model vol (rv)
        res = simulate_delta_hedge(
            S_slice, K, dte_days, r, vol_slice,
            option_type=option_type, txn_cost_bps_stock=stock_tc_bps
        )
        pnl_hedged = float(res["pnl"].sum())
        trade_pnl = pnl_hedged if side == 'buy' else -pnl_hedged

        trades.append({
            'date': date, 'side': side, 'K': K, 'S0': S0,
            'rv': sigma_rv, 'iv_mkt': sigma_iv,
            'dte': dte_days, 'pnl': trade_pnl
        })

        #Skip forward
        if allow_overlapping:
            i += 1              #allow entries on consecutive days
        else:
            #jump to the first candidate after this window
            next_block_start = t + dte_days
            while i < len(indices) and indices[i] <= next_block_start:
                i += 1

    trade_df = pd.DataFrame(trades)
    if trade_df.empty:
        return trade_df, {'n_trades': 0, 'total_pnl': 0, 'avg_pnl': 0, 'win_rate': 0}

    summary = {
        'n_trades': int(len(trade_df)),
        'total_pnl': float(trade_df['pnl'].sum()),
        'avg_pnl': float(trade_df['pnl'].mean()),
        'win_rate': float((trade_df['pnl'] > 0).mean())
    }
    return trade_df, summary
