from source.backtest import run_mispricing_backtest

trades, summary = run_mispricing_backtest(
    ticker = "AAPL",
    start = '2022-01-01',
    end = '2023-01-01',
    r = 0.03,
    dte_days = 30,
    option_type = 'call',
    mispricing_threshold = 0.01,
    stock_tc_bps = 1.0
)

print(summary)
print(trades.head())
