# Quantitative Trading Lab — Development Roadmap

> Living project document. Keep this file at the root of the GitHub repository and update it after each completed development step or significant design decision. It is the primary handoff document for continuing development in a new ChatGPT or Codex conversation.

| Project information | Status |
| --- | --- |
| Proposed repository name | `quantitative-trading-lab` |
| Purpose | Educational quantitative finance research and software engineering portfolio |
| Language | Python 3.12 |
| Market data provider | `yfinance` only |
| Current phase | Phase 0 — Core infrastructure |
| Current step | Step 2 — Testing infrastructure and GitHub Actions |
| Phase 0 progress | 1/10 steps confirmed complete |
| First strategy project | Project 01 — Pairs Trading |
| Last updated | 2026-11-24 |

Step 1 is complete based on the user's confirmation on 2026-11-24 and terminal screenshots showing successful editable installation, local import and package builds. Step 2 is in progress; its local quality checks and GitHub workflow have not yet been verified. See the development log for evidence and remaining uncertainties.

## 1. Project vision

Build one public GitHub repository containing independent quantitative finance experiments, progressing from basic statistical trading to portfolio optimization, machine learning, deep learning and reinforcement learning. Each project should teach a distinct concept and reuse a shared, tested Python research framework.

The repository is intended to:

- Develop practical knowledge of how quantitative trading strategies work, including why they fail.
- Apply statistics, mathematics, optimization, software engineering and machine learning to real historical market data.
- Support equities, ETFs, cryptocurrencies and other instruments available through Yahoo Finance, without restricting research to crypto.
- Compare strategies using reproducible experiments, realistic assumptions, appropriate baselines and out-of-sample evaluation.
- Demonstrate professional engineering through modular design, tests, documentation, continuous integration and version control.
- Eventually publish a research dashboard on GitHub Pages if useful.

**Scope:** This is a learning and historical research platform, not a production trading system or a recommendation to trade real capital. No live brokerage integration or automatic real-money execution is planned for Phase 0.

## 2. Agreed development decisions

| Decision | Rationale |
| --- | --- |
| Use only `yfinance` initially | No API keys; one source for many asset classes; less integration overhead. |
| Daily historical data first | Simpler, appropriate for initial statistical strategies; avoids unsupported microstructure claims. |
| Build the core before strategy projects | Reuse data collection, accounting, backtesting, metrics and reporting. |
| Use a Python `src/` package layout | Keep shared functionality importable and testable. |
| Develop incrementally | Implement one step, test it, document it, commit it, then move on. |
| Configure CI early | Tests and quality checks are part of development, not an afterthought. |
| Keep CI offline | Mock Yahoo Finance calls and use deterministic synthetic fixtures. |
| Implement an educational backtester | Learn execution and accounting mechanics directly; cross-check against known results and, later, other tools if useful. |
| Keep strategies independent | Projects may depend on `quantlab`, but not on one another. |
| Start with Pairs Trading | This was the original motivation for the repository, even though simpler strategies exist. |
| Avoid premature abstractions | No multi-provider interface, unused dependencies or complex infrastructure until justified. |

## 3. Initial technology stack

| Component | Technology |
| --- | --- |
| Language | Python 3.12 |
| Packaging and dependency management | `pyproject.toml`, `uv`, `uv.lock` |
| Market data | `yfinance` |
| Numerical computing | NumPy |
| Data processing | Pandas |
| Local storage | PyArrow / Parquet |
| Statistics | SciPy, Statsmodels |
| Initial optimization | SciPy |
| Visualization | Matplotlib |
| Configuration | PyYAML |
| Tests and coverage | Pytest, pytest-cov |
| Linting and formatting | Ruff |
| Type checking | Mypy |
| Continuous integration | GitHub Actions |
| Exploratory analysis | Jupyter (when needed) |

Install dependencies as the relevant step requires them. Heavy ML/RL libraries, additional data providers, databases, live execution and web dashboard dependencies are deferred. Commit the lockfile for reproducibility. No API credentials are needed for the initial data source.

## 4. Target repository architecture

This is a target layout, not a requirement to create every file in Step 1. Add modules when they have real functionality and tests.

```text
quantitative-trading-lab/
├── README.md
├── ROADMAP.md
├── CONTRIBUTING.md
├── LICENSE
├── pyproject.toml
├── uv.lock
├── .gitignore
├── .github/
│   └── workflows/
│       └── ci.yml
├── src/
│   └── quantlab/
│       ├── __init__.py
│       ├── data/
│       │   ├── loader.py
│       │   ├── cache.py
│       │   ├── schema.py
│       │   └── validation.py
│       ├── statistics/
│       │   ├── returns.py
│       │   ├── correlation.py
│       │   ├── stationarity.py
│       │   └── volatility.py
│       ├── backtesting/
│       │   ├── portfolio.py
│       │   ├── engine.py
│       │   ├── execution.py
│       │   └── costs.py
│       ├── metrics/
│       │   ├── performance.py
│       │   ├── risk.py
│       │   └── trading.py
│       ├── strategies/
│       │   └── base.py
│       └── visualization/
│           ├── plots.py
│           └── reports.py
├── projects/
│   └── 01_pairs_trading/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── data/
│   ├── raw/
│   ├── processed/
│   └── cache/
├── configs/
│   └── default.yaml
└── docs/
    ├── architecture.md
    ├── methodology.md
    └── metrics.md
```

Core data flow:

```text
Yahoo Finance (yfinance)
    -> data loader
    -> validation, normalization and local cache
    -> strategy (signals or target positions)
    -> execution and portfolio accounting
    -> backtest results
    -> performance metrics and research reports
```

Only the data layer should directly call `yfinance`. Strategies receive standardized data rather than downloading it themselves. Separate strategy decisions from simulated execution. Keep the core independent of individual experiments.

## 5. Phase 0 — Core infrastructure

### Progress tracker

| Step | Deliverable | Status | Estimated focused effort |
| --- | --- | --- | --- |
| 1 | Repository initialization and Python packaging | Complete | 1–2 hours |
| 2 | Testing infrastructure and GitHub Actions | In progress | 1–2 hours |
| 3 | Historical market data collection | Not started | 1–2 hours |
| 4 | Data validation, preprocessing and caching | Not started | 2–3 hours |
| 5 | Mathematical and statistical utilities | Not started | 2–4 hours |
| 6 | Portfolio accounting and position management | Not started | 3–5 hours |
| 7 | Backtesting and execution engine | Not started | 4–8 hours |
| 8 | Performance and risk metrics | Not started | 3–5 hours |
| 9 | Visualization and reporting | Not started | 2–4 hours |
| 10 | End-to-end validation and documentation | Not started | 2–3 hours |

**Estimated total: 21–38 focused hours.** This is a rough estimate for an initial educational framework, not a deadline or a production-quality implementation estimate. Difficult data or accounting edge cases may require additional work.

Allowed status values: `Not started`, `In progress`, `Blocked`, `Complete`. Mark a step complete only after its acceptance checks have been verified. Record any partial implementation or blockers in the development log.

### Step 1 — Repository initialization and Python packaging

- [x] Create or initialize the Git repository and establish the root directory structure.
- [x] Configure Python 3.12 and a local virtual environment using `uv`.
- [x] Create `pyproject.toml` and the minimal installable `src/quantlab` package.
- [x] Generate and commit `uv.lock`.
- [x] Add `.gitignore` (virtual environments, caches, local data, generated artifacts and secrets).
- [x] Add initial README, this roadmap and basic contribution guidance.
- [x] Add an open-source license before publishing (LICENSE file visible in Git status; exact license text not inspected).
- [x] Verify a clean environment can install and import the package.
- [x] Commit the verified scaffold.

**Acceptance:** a clean checkout can install the package, import `quantlab` and follow documented setup instructions. No strategy implementation is required yet.

Completion is user-confirmed. Screenshots independently show Python 3.12.9, successful editable installation, import from `src/quantlab/__init__.py`, and both distribution builds. The final clean-environment retry, staged file review and commit hash were not separately shown.

Suggested commit: `chore: initialize quantitative trading research package`

### Step 2 — Testing infrastructure and GitHub Actions

- [ ] Configure Pytest, pytest-cov, Ruff and Mypy in `pyproject.toml`.
- [ ] Establish `tests/unit`, `tests/integration` and `tests/fixtures`.
- [ ] Add a minimal package smoke test.
- [ ] Create `.github/workflows/ci.yml` for pushes and pull requests.
- [ ] Install locked dependencies and run linting, formatting, tests, coverage and type checks (using documented scope).
- [ ] Ensure default CI needs neither network market-data requests nor credentials.
- [ ] Verify checks locally and on GitHub, if the remote exists.

**Acceptance:** repeatable local checks pass; CI is configured and actual GitHub status is recorded when available. Introduce coverage thresholds once meaningful core functionality exists.

Suggested commit: `ci: establish automated tests and code quality checks`

### Step 3 — Historical market data collection

- [ ] Implement the isolated `yfinance` loader for one or multiple tickers, date ranges and daily frequency.
- [ ] Normalize single-ticker and multi-ticker response layouts.
- [ ] Handle invalid requests, empty results, partial ticker failures and network errors explicitly.
- [ ] Define start/end-date semantics (Yahoo download end dates are exclusive) and price-adjustment behavior explicitly.
- [ ] Support equities, ETFs and crypto ticker formats.
- [ ] Write mocked provider tests with no live calls in CI.
- [ ] Run an optional manual live smoke check for a stock and cryptocurrency.

**Acceptance:** the loader returns predictable data for supported instruments and clear errors for failed requests. No other market data provider is added.

Suggested commit: `feat: implement Yahoo Finance historical data loader`

### Step 4 — Data validation, preprocessing and Parquet caching

- [ ] Define a canonical long-form data schema and validate required fields.
- [ ] Normalize dates/timestamps, sort observations, detect duplicates and validate numeric prices.
- [ ] Preserve unavailable data as missing; do not silently invent prices, volume or trading bars.
- [ ] Document adjustment policy for splits, dividends, total-return proxies and execution prices.
- [ ] Distinguish equity sessions from 24/7 crypto observations; do not fill market closures as tradable bars.
- [ ] Implement Parquet cache with request identity, metadata, cache refresh and clear handling of corrupted entries.
- [ ] Test round-trips, cache hits/misses, validation and alignment on synthetic data.
- [ ] Keep raw and cached market data local and out of Git.

Initial schema (exact implementation to be finalized during this step):

| Field | Description |
| --- | --- |
| `timestamp` | Normalized observation time or session label, with documented convention |
| `symbol` | Yahoo Finance ticker |
| `asset_class` | Equity, ETF, crypto or another supported classification |
| `open`, `high`, `low`, `close` | OHLC fields with documented adjustment policy |
| `adjusted_close` | Adjusted series when available under the selected request mode |
| `volume` | Reported volume, nullable where unavailable |
| `currency` | Quote currency when known |
| `source` | `yfinance` |

Set `auto_adjust` explicitly rather than relying on changing defaults. Do not confuse adjusted series with raw executable prices, or count dividends twice. Do not aggregate assets in different currencies without an explicit conversion method; initial portfolio tests can use USD instruments.

**Acceptance:** normalized data can be cached, loaded and validated consistently, with documented calendar and adjustment semantics.

Suggested commit: `feat: normalize and cache historical market data`

### Step 5 — Mathematical and statistical utilities

- [ ] Implement simple and logarithmic returns.
- [ ] Implement rolling means, standard deviations and Z-scores.
- [ ] Implement return correlation and covariance matrices.
- [ ] Implement volatility and annualization with explicit frequency conventions.
- [ ] Add ADF and Engle-Granger cointegration helpers where appropriate.
- [ ] Test known values, constant series, missing values, insufficient history and invalid inputs.
- [ ] Ensure rolling calculations only use information available at the evaluation time.

**Acceptance:** statistical outputs match hand-calculated or trusted reference examples, and edge cases have documented behavior.

Suggested commit: `feat: add tested quantitative statistical utilities`

### Step 6 — Portfolio accounting and position management

- [ ] Define cash, signed positions, holdings value and total portfolio equity.
- [ ] Support multiple assets and long/short positions.
- [ ] Track trades, position changes, realized/unrealized P&L as appropriate and transaction costs.
- [ ] Define gross and net exposure, sizing and leverage assumptions.
- [ ] Define behavior for missing prices, insufficient buying power and short proceeds.
- [ ] Document the corporate action and short-financing treatment used by the initial simulation.
- [ ] Test cash conservation, long/short P&L, position closing, fees and multi-asset accounting with hand-worked fixtures.

**Acceptance:** deterministic accounting examples reconcile to expected cash, positions and equity. Unsupported brokerage or margin behavior is clearly documented rather than implied.

Suggested commit: `feat: implement multi-asset portfolio accounting`

### Step 7 — Backtesting and execution engine

- [ ] Define a minimal strategy interface with clear input/output and position semantics.
- [ ] Process historical observations chronologically.
- [ ] Separate signal timestamps from fill timestamps; for the initial daily model, use an explicitly documented next-available-bar execution convention.
- [ ] Implement configurable commissions and slippage; model or explicitly disclose borrowing/financing assumptions for shorts.
- [ ] Support buy-and-hold and multi-asset long/short simulations.
- [ ] Record orders/trades, equity, exposure, turnover and costs.
- [ ] Test look-ahead prevention, execution timing, missing bars, costs and accounting consistency.
- [ ] Define how positions are valued when an instrument is closed or a bar is missing; do not simulate trades at nonexistent prices.

**Acceptance:** a hand-calculated example and a synthetic long/short example produce expected trades and equity; signals cannot execute before their information is available. This initial engine need not support live trading, order books or market impact models.

Suggested commit: `feat: implement historical backtesting and execution engine`

### Step 8 — Performance and risk metrics

- [ ] Implement cumulative return, annualized return and annualized volatility.
- [ ] Implement Sharpe, Sortino and Calmar ratios with documented conventions.
- [ ] Implement maximum drawdown and drawdown series.
- [ ] Implement win rate, profit factor, number of trades and transaction costs where meaningful.
- [ ] Implement benchmark comparison and applicable beta, VaR and CVaR calculations.
- [ ] Support explicit annualization frequencies and risk-free-rate assumptions.
- [ ] Define behavior for no trades, zero variance, zero drawdown and insufficient observations.
- [ ] Compare results against deterministic examples.

**Acceptance:** metrics are reproducible, use consistent units and conventions and do not silently produce misleading values for undefined cases. Prioritize core return/risk metrics before optional advanced metrics.

Suggested commit: `feat: add standardized performance and risk metrics`

### Step 9 — Visualization and reporting

- [ ] Generate equity curve and benchmark comparison plots.
- [ ] Generate drawdown, return distribution and trade/position plots.
- [ ] Export metrics and trades in machine-readable JSON/CSV formats.
- [ ] Store experiment parameters, data provenance and assumptions alongside results.
- [ ] Make output directories configurable and use a headless plotting backend in automated tests.
- [ ] Test that expected report artifacts are produced.

**Acceptance:** a sample run generates standardized reports without requiring an interactive display or manual editing.

Suggested commit: `feat: generate reproducible backtest reports and plots`

### Step 10 — End-to-end validation and documentation

- [ ] Run a complete offline synthetic-data pipeline from data normalization to report generation.
- [ ] Perform a manual historical-data smoke test for equities and crypto when connectivity permits.
- [ ] Verify buy-and-hold and multi-asset long/short examples.
- [ ] Review all CI checks and relevant coverage reports; target approximately 90% coverage for critical mathematical and accounting logic while prioritizing meaningful tests.
- [ ] Document install, test, run and troubleshooting commands that actually work.
- [ ] Document data-source limitations, adjustment policy, calendars, backtesting assumptions and known risks.
- [ ] Verify a clean checkout is reproducible using locked dependencies.
- [ ] Update the root README and this roadmap with actual outcomes.

**Acceptance:** the Phase 0 acceptance checklist below is satisfied or any explicitly deferred limitation is recorded and agreed upon before moving to Project 01.

Suggested commit: `docs: finalize phase zero research infrastructure`

### Phase 0 acceptance checklist

- [ ] Reproducible package installation from a clean checkout.
- [ ] Historical stock and cryptocurrency retrieval using `yfinance` only (manual live verification recorded separately from offline tests).
- [ ] Standardized, validated historical market data and local Parquet caching.
- [ ] Documented price adjustments, calendars, date boundaries and missing-data policy.
- [ ] Tested returns, Z-scores, correlation and other initial statistical utilities.
- [ ] Verified buy-and-hold and multi-asset long/short backtests.
- [ ] Verified cash, position and equity accounting with known test values.
- [ ] Explicit execution timing and costs; look-ahead prevention tested.
- [ ] Performance metrics and equity/drawdown plots generated automatically.
- [ ] Offline unit and integration tests pass; GitHub Actions status verified when available.
- [ ] Root README and methodology documentation describe actual behavior and limitations.
- [ ] Development log and next-step handoff updated.

## 6. Initial data universe and limitations

Use a small configurable universe during development rather than downloading thousands of tickers. The following are candidates for research, not trading recommendations.

| Category | Candidate tickers |
| --- | --- |
| Technology | AAPL, MSFT, NVDA, GOOGL, AMD |
| Financials | JPM, BAC, V, MA |
| Consumer goods | KO, PEP, PG |
| Energy | XOM, CVX |
| Equity ETFs | SPY, VOO, QQQ, IWM |
| Crypto | BTC-USD, ETH-USD, SOL-USD |
| Commodity ETFs | GLD, SLV |
| Fixed-income ETFs | TLT, BND |
| Market reference series | ^VIX, ^GSPC |

Data conventions and known limitations:

- Daily US equities use exchange sessions; crypto trades continuously. Use appropriate calendar alignment and explicit annualization (commonly 252 equity or 365 crypto daily periods, not a universal constant).
- Yahoo Finance indices are reference series, not necessarily directly tradable assets. ETFs may serve as tradable proxies when appropriate.
- Historical ticker availability varies. Do not assume every symbol has data for the full requested date range.
- `yfinance` is an unofficial client, not a guaranteed exchange-grade feed. Requests can fail or return incomplete/revised data. Record retrieval dates and assumptions, and inspect data quality.
- Do not infer executable cross-exchange arbitrage, order book state, funding rates or real-time fills from aggregate daily prices.
- Public source code and synthetic fixtures can be committed; do not redistribute third-party market data without checking applicable terms. Store downloaded data locally.
- A universe composed of current tickers can introduce survivorship bias. Document this limitation; do not claim point-in-time universe coverage without appropriate data.

Reference: [yfinance repository](https://github.com/ranaroussi/yfinance). No additional data provider is in the current scope.

## 7. Strategy project roadmap

The plan is to work through increasingly complex projects after Phase 0. Pairs Trading remains Project 01 by preference; the ordering thereafter prioritizes progressive learning. Project IDs below are a proposed long-term sequence, not a commitment to implement every item or introduce additional providers. Research time estimates for individual projects are intentionally deferred until scope and infrastructure are known.

### Level 1 — Fundamentals

| ID | Project folder | Learning objective |
| --- | --- | --- |
| 01 | `01_pairs_trading` | Correlation, cointegration, hedge ratios, spread Z-scores |
| 02 | `02_mean_reversion` | Rolling statistics and reversal signals |
| 03 | `03_momentum_trading` | Trend following |
| 04 | `04_time_series_momentum` | Multi-horizon individual asset momentum |
| 05 | `05_breakout_trading` | Historical range breakouts |
| 06 | `06_cross_sectional_momentum` | Relative asset ranking |
| 07 | `07_volatility_breakout` | Volatility compression and expansion |
| 08 | `08_kelly_criterion` | Position sizing and estimation uncertainty |
| 09 | `09_volatility_targeting` | Exposure management |
| 10 | `10_minimum_variance_portfolio` | Covariance-based allocation |

### Level 2 — Statistical modeling

| ID | Project folder | Learning objective |
| --- | --- | --- |
| 11 | `11_markowitz_optimization` | Efficient frontier |
| 12 | `12_risk_parity` | Equal risk contributions |
| 13 | `13_lead_lag_trading` | Cross-correlation and lagged signals |
| 14 | `14_factor_investing` | Price-derived factors and cross-sectional portfolios |
| 15 | `15_ornstein_uhlenbeck` | Stochastic mean reversion and half-life |
| 16 | `16_garch_volatility` | Conditional volatility forecasting |
| 17 | `17_hierarchical_risk_parity` | Clustering and portfolio allocation |
| 18 | `18_kalman_filter_pairs` | Time-varying hedge ratios |
| 19 | `19_basket_statistical_arbitrage` | Multi-asset equilibrium relationships |
| 20 | `20_pca_statistical_arbitrage` | Common factors and residual signals |

### Level 3 — Advanced modeling and arbitrage

| ID | Project folder | Learning objective | Data status |
| --- | --- | --- | --- |
| 21 | `21_market_regime_detection` | HMMs and clustering | Daily research feasible |
| 22 | `22_regime_based_trading` | Conditional strategy selection | Daily research feasible |
| 23 | `23_black_litterman` | Market equilibrium and investor views | Assumptions/inputs needed |
| 24 | `24_cvar_optimization` | Tail-risk optimization | Daily research feasible |
| 25 | `25_cross_exchange_arbitrage` | Venue-specific pricing | Deferred |
| 26 | `26_triangular_arbitrage` | Executable conversion cycles | Deferred |
| 27 | `27_funding_rate_arbitrage` | Perpetual futures funding | Deferred |
| 28 | `28_cash_and_carry_arbitrage` | Spot/futures basis and financing | Deferred for realistic crypto execution |
| 29 | `29_dynamic_hedging` | Exposure reduction | Daily research feasible for simple hedges |
| 30 | `30_robust_portfolio_optimization` | Uncertain returns and covariance estimates | Daily research feasible |

### Level 4 — Machine learning and market microstructure

| ID | Project folder | Learning objective | Data status |
| --- | --- | --- | --- |
| 31 | `31_ml_direction_prediction` | Classification | Daily research feasible |
| 32 | `32_ml_return_prediction` | Regression | Daily research feasible |
| 33 | `33_market_anomaly_detection` | Unsupervised anomaly detection | Daily research feasible |
| 34 | `34_ensemble_trading` | Combining predictions | Daily research feasible |
| 35 | `35_order_book_imbalance` | Limit order book features | Deferred |
| 36 | `36_order_flow_trading` | Trade-level execution data | Deferred |
| 37 | `37_sentiment_trading` | Time-aligned external text signals | Deferred |
| 38 | `38_deep_time_series_forecasting` | LSTM, GRU, TCN comparisons | Daily research feasible |
| 39 | `39_nonlinear_statistical_arbitrage` | Kernel and neural spread models | Daily research feasible |
| 40 | `40_market_making` | Bid/ask placement and inventory | Deferred for empirical execution research |

### Level 5 — Deep learning and reinforcement learning

| ID | Project folder | Learning objective | Data status |
| --- | --- | --- | --- |
| 41 | `41_transformer_trading` | Multivariate temporal modeling | Daily research feasible |
| 42 | `42_rl_single_asset_trading` | Sequential buy/sell/hold policies | Daily simulation feasible |
| 43 | `43_rl_position_sizing` | Continuous sizing decisions | Daily simulation feasible |
| 44 | `44_graph_neural_network_trading` | Cross-asset graph relationships | Daily research feasible |
| 45 | `45_rl_statistical_arbitrage` | Learning spread entry and exit policies | Daily simulation feasible |
| 46 | `46_rl_portfolio_allocation` | Dynamic multi-asset allocations | Daily simulation feasible |
| 47 | `47_adaptive_strategy_selection` | Bandits/RL strategy switching | Daily simulation feasible |
| 48 | `48_rl_optimal_execution` | Execution costs and market impact | Deferred for empirical execution research |
| 49 | `49_rl_market_making` | Inventory-aware quoting policies | Deferred for empirical execution research |
| 50 | `50_multi_agent_trading` | Interacting learning agents | Synthetic simulation possible; realistic validation deferred |

Deferred projects can be skipped without changing their IDs. They remain future ideas, not permission to introduce additional data providers. Synthetic simulations may teach mechanics, but must not be represented as validated historical trading performance. Daily-data feasibility does not imply sufficient sample size, a reliable predictive edge or profitability.

## 8. Project 01 — Pairs Trading

**Status:** Planned; blocked on Phase 0 completion.

**Research question:** Do statistically selected asset pairs exhibit sufficiently stable mean reversion to produce out-of-sample simulated returns after costs?

Initial implementation scope:

1. Retrieve aligned historical prices using the core loader.
2. Screen candidate pairs with correlation of returns.
3. Test candidate price relationships for cointegration using training data only; correlation alone does not establish cointegration.
4. Estimate a hedge ratio and construct a spread (e.g., regression residual).
5. Calculate rolling spread Z-scores using available historical observations.
6. Generate long/short spread positions with configurable entry, exit and stop thresholds.
7. Backtest with explicit fill timing, hedge-ratio-aware sizing, fees, slippage and short-cost assumptions.
8. Evaluate on unseen data against appropriate passive/cash benchmarks and report both successful and unsuccessful pairs.

Illustrative initial parameters for experimentation (not optimized or proven): entry at Z-score ±2, exit near zero, stop near absolute Z-score 4. Fit thresholds and hedge parameters only on permitted historical data; do not select parameters based on final test performance.

Candidate pairs: KO/PEP, V/MA, XOM/CVX, JPM/BAC, SPY/VOO and BTC-USD/ETH-USD. These are hypotheses to investigate, not verified cointegrated or profitable pairs.

Possible reports: correlation heatmap, spread and Z-score plots, positions, trades, equity curve, benchmark, drawdown and summary metrics. Discuss instability, multiple testing, pair-selection bias, trading costs and shorting limitations.

## 9. Individual project conventions

Use a consistent folder pattern, scaled to complexity:

```text
projects/01_pairs_trading/
├── README.md
├── config.yaml
├── main.py
├── src/
│   ├── strategy.py
│   └── analysis.py
├── notebooks/
│   └── exploration.ipynb
├── tests/
│   └── test_strategy.py
└── results/
    ├── metrics.json
    ├── trades.csv
    └── figures/
```

The project README must state the question, theory, data, assumptions, reproduction commands, evaluation protocol, findings and limitations. Small projects can use fewer files. Results may be stored locally; only commit appropriate permitted outputs and avoid committing raw third-party data.

### Definition of completion for a strategy project

- [ ] Explain the mathematical theory and research hypothesis.
- [ ] Use the shared core to obtain and validate data.
- [ ] Implement a configurable strategy and relevant tests.
- [ ] Include a meaningful baseline with comparable constraints.
- [ ] Separate training/validation/test chronologically; use walk-forward evaluation when suitable.
- [ ] Avoid leakage, look-ahead, unrealistic fills and unreported costs.
- [ ] Generate standardized metrics and visualizations where applicable.
- [ ] Record experiment configuration, data provenance and reproducibility instructions.
- [ ] Discuss risks, negative results, limitations and potential improvements.
- [ ] Run all relevant checks, update documentation and commit the project.

## 10. Engineering and research standards

### Local quality checks

The following are the proposed Step 2 command conventions. They have not yet been verified locally for this repository. The source-only Mypy scope and package-only coverage scope are intentional for the initial setup.

```bash
uv sync --locked
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked mypy src
uv run --locked pytest --cov=quantlab --cov-report=term-missing --cov-report=html --cov-report=xml
uv build
```

CI should use locked dependencies, run applicable quality checks and produce a coverage report. Build/install verification can be added once packaging is configured. Keep live data smoke tests optional and separate. Add tests for every new core behavior, especially deterministic financial accounting and edge cases. Coverage is a diagnostic, not a substitute for correctness.

### Backtesting integrity

- No look-ahead bias: signals, feature transformations, pair selection, model fitting and tuning may only use data available at their simulated decision time.
- No data leakage: use chronological splits and keep the final test set untouched during development decisions.
- No false precision: account for fees, slippage, liquidity constraints and short-financing assumptions as appropriate; identify what is not modeled.
- Use explicit position semantics, execution timing, calendar, currency, corporate action and annualization conventions.
- Maintain comparable benchmarks, costs and capital constraints across comparable experiments.
- Report unsuccessful experiments and avoid equating historical profitability with future returns.
- Seed stochastic experiments where possible and record versions, parameters, data retrieval dates and evaluation periods.

## 11. Long-term phases

| Phase | Deliverable | Status |
| --- | --- | --- |
| 0 | Core infrastructure | In progress (1/10) |
| 1 | Traditional statistical trading projects | Planned |
| 2 | Advanced statistical and stochastic models | Planned |
| 3 | Portfolio optimization and arbitrage | Planned; some methods deferred for data limitations |
| 4 | Machine learning trading strategies | Planned |
| 5 | Deep learning and reinforcement learning | Planned |
| 6 | Optional GitHub Pages research dashboard | Planned |

The numbered levels in the strategy catalog describe approximate difficulty; the phases are broader milestones and need not match levels exactly. Build the core incrementally as projects expose new needs. Do not build the dashboard, live execution infrastructure or deferred strategies ahead of the tested research foundation.

## 12. Development log and handoff

### Current checkpoint

- **Last completed step:** Phase 0, Step 1 — Repository initialization and Python packaging (user-confirmed; partial terminal evidence recorded below).
- **Current phase:** Phase 0 — Core infrastructure.
- **Next action:** Step 2 — Testing infrastructure and GitHub Actions. Install development dependencies, configure tools, add a package smoke test, create the CI workflow, run local checks and verify GitHub results if a remote exists.
- **Repository state:** Windows local checkout, branch `main` observed; `quantlab` editable installation and package build successful. Remote URL and final Step 1 commit hash not supplied.
- **Tests / CI:** Not yet verified. Step 2 configuration is proposed: Pytest discovery in `tests` and `projects`, Ruff lint/format, strict Mypy scoped to `src`, branch coverage of `quantlab`, and a Windows/Linux GitHub Actions matrix. Do not set a coverage threshold yet.
- **Known blockers:** Earlier PATH and import issues resolved. Optional environment deletion initially failed due to an access-denied error; user subsequently confirmed Step 1 complete, but final clean-environment output was not shown. No known active blocker. Exact license text not inspected.
- **Data source:** `yfinance` only. Do not add CoinGecko, Alpaca, CCXT or any other provider unless the scope is explicitly changed later.
- **User workflow:** Work through one development step at a time, explain what is being built and why, test before progressing, suggest a descriptive Git commit, and update this file after verified milestones.

### History

| Date | Phase / step | Outcome | Verification / commit |
| --- | --- | --- | --- |
| 2026-11-24 | Planning | Agreed on a reusable, tested, yfinance-only quantitative research repository; defined Phase 0 and selected Pairs Trading as the first project. | Planning document only; no implementation verified. |
| 2026-11-24 | Phase 0, Step 1 | Completed repository initialization and Python packaging, per user confirmation. Added minimal `quantlab` package, `pyproject.toml`, lockfile and initial documentation. `.gitattributes` and missing `.gitkeep` files were recommended during final review. | Terminal evidence: Python 3.12.9; editable installation; successful import from local source; built `.tar.gz` and `.whl`. Final clean recreation and commit hash not separately shown. |
| 2026-11-24 | Phase 0, Step 2 | Began testing and CI setup. Proposed Pytest, pytest-cov, Ruff, Mypy, smoke test and Windows/Linux CI. | Pending local and remote verification; no tests or CI results claimed. |

### How to update this file

After each completed step or significant change:

1. Update the top status table and last-updated date.
2. Check off only verified tasks and acceptance criteria; change the step status accordingly.
3. Record implemented files, commands run, actual test/coverage/CI results and any commit hash available.
4. Add a dated development log entry; record deviations and reasons rather than silently changing the plan.
5. Update the current checkpoint with the exact next action, blockers and pending decisions.
6. Keep the roadmap in Git so changes to the project plan are versioned alongside implementation.

Suggested log entry template:

```markdown
### YYYY-MM-DD — Phase X, Step Y

- Status:
- Implemented:
- Files added/changed:
- Verification commands and actual results:
- Git commit (if available):
- Decisions or deviations:
- Known limitations / blockers:
- Next action:
```

### Resume prompt for a new conversation

Upload the latest `ROADMAP.md` to the new chat (and share the current repository files or accessible repository when relevant), then use this prompt:

> We are continuing my Quantitative Trading Lab repository. Read the attached ROADMAP.md in full and use it as the source of truth for the project scope, architecture, development standards, progress and next action. We are using Python 3.12 and yfinance as the only market data provider. We are building a reusable tested core before implementing individual quantitative finance projects, beginning with Pairs Trading. Inspect the available repository state and reconcile it with the roadmap before making changes. Continue from the current checkpoint, not from the beginning, and work on one step at a time. Explain the purpose, provide concrete implementation instructions or code, include automated tests, and specify how to verify the step. Do not claim tests, commits or CI succeeded unless actually verified. Do not expand the scope or add other data providers without my approval. When I confirm the step is complete, update the roadmap with verified progress, results, decisions and the next action, and suggest an appropriate Git commit message.

---

**Next milestone: complete Phase 0, Step 2 — Testing infrastructure and GitHub Actions.**
