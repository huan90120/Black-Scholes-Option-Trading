import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from source.data_loader import get_stock_data
from source.rv_forecasting import ewma_vol
from source.backtest import run_mispricing_backtest

#Parameters
TICKER = "AAPL"
START = "2022-01-01"
END = "2023-01-01"
R = 0.03
DTE_DAYS = 7
OPTION_TYPE = 'call'
MISPRICING_THRESHOLD = 0.003
STOCK_TC_BPS = 1.0
SIM_IV_NOISE_BPS = 180
SIM_IV_SEED = 42

#IV Simulator
def simulate_market_iv(rv_series: pd.Series, noise_bp: int = 120,
                       seed: int = 42) -> pd.Series:
    """
    Make a fake IV series around RV and noise for demonstration.
    noise_bp: basis points of vol (100bp = 1 vol point) std dev.
    """
    np.random.seed(seed)
    rv = rv_series.dropna().astype(float)
    noise = np.random.normal(0, noise_bp / 10000.0, size = len(rv))
    iv = (rv.values + noise).clip(0.01, 1.5)
    out = pd.Series(iv, index = rv.index, name = "sim_iv")
    return out

#main program
def main():
    print(f"\n=== Simulated-IV pipeline for {TICKER}")

    #load prices and compute RV
    df = get_stock_data(TICKER, START, END)
    close = df['Close'].asfreq("B").ffill()
    rv = ewma_vol(close, lam = 0.94)
    rv = rv.reindex(close.index).ffill()

    #simulate market IV (for plotting)
    sim_iv = simulate_market_iv(rv, noise_bp = SIM_IV_NOISE_BPS, seed = SIM_IV_SEED)
    sim_iv = sim_iv.reindex(close.index).ffill()
    iv_minus_rv = (sim_iv - rv).dropna()

    #run existing mispricing backtest
    trades, summary = run_mispricing_backtest(
        ticker = TICKER,
        start = START,
        end = END,
        r = R,
        dte_days = DTE_DAYS,
        option_type = OPTION_TYPE,
        mispricing_threshold = MISPRICING_THRESHOLD,
        stock_tc_bps = STOCK_TC_BPS,
        iv_noise_bp = SIM_IV_NOISE_BPS,
        iv_seed = SIM_IV_SEED
    )

    print("Summary:")
    for k, v in summary.items():
        print(f" {k}: {v}")

    #PLOTS

    #price
    plt.figure()
    close.tail(250).plot()
    plt.title(f"{TICKER} - Price (Last 250 Days)")
    plt.xlabel("Date")
    plt.ylabel("Price")
    
    #RV timeseries
    plt.figure()
    rv.tail(250).plot()
    plt.title(f"{TICKER} - EWMA RV (Annualized, Last 250 Days)")
    plt.xlabel("Date")
    plt.ylabel("Volatility")

    #IV vs RV
    plt.figure()
    rv.tail(250).plot(label = "RV")
    sim_iv.tail(250).plot(label = "Sim IV")
    plt.title(f"{TICKER} - Simulated IV vs RV (Last 250 Days)")
    plt.xlabel("Date")
    plt.ylabel("Volatility")
    plt.legend()

    #Histogram of IV - RV
    plt.figure()
    iv_minus_rv.plot(kind = 'hist', bins = 30)
    plt.title(f"{TICKER} - Distribution of Sim IV - RV")
    plt.xlabel("Volatility Points")
    plt.ylabel("Frequency")
    
    #Per trade pnl bars
    if len(trades) > 0:
        trades_sorted = trades.sort_values('date')
        plt.figure()
        x = trades_sorted['date'].astype(str).values
        y = trades_sorted['pnl'].values
        plt.bar(x, y)
        plt.title(f"{TICKER} - Per-Trade PNL")
        plt.xticks(rotation = 45, ha = 'right')
        plt.ylabel('PNL')

    #cumulating pnl
    plt.figure()
    trades_sorted["cum_pnl"] = trades_sorted["pnl"].cumsum()
    plt.plot(trades_sorted["date"], trades_sorted["cum_pnl"])
    plt.title(f"{TICKER} - Cumulative PNL")
    plt.xlabel("Trade Date")
    plt.ylabel("Cumulative PNL")


#execute
if __name__ == "__main__":
    main()
