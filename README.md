[![CI](https://github.com/USERNAME/quantitative-trading-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/jgncodes/quantitative-trading-lab/actions/workflows/ci.yml)

# Quantitative Trading Lab

A quantitative finance research laboratory focused on the
implementation, evaluation, and comparison of algorithmic
trading strategies using historical financial market data.

## Overview

This repository is an educational software engineering and
quantitative finance project exploring:

- Statistical arbitrage
- Mean reversion
- Momentum trading
- Stochastic processes
- Portfolio optimization
- Risk management
- Machine learning
- Deep learning
- Reinforcement learning

Each research project is implemented independently while
sharing a common quantitative research infrastructure.

## Objectives

- Understand the mathematical foundations of quantitative trading.
- Implement strategies using historical market data.
- Develop reproducible backtesting experiments.
- Evaluate strategies using standardized performance metrics.
- Investigate market inefficiencies and strategy limitations.
- Maintain professional software engineering standards.

## Technology Stack

- Python 3.12
- uv
- Hatchling

Additional numerical, statistical, and market data
dependencies will be introduced incrementally.

Yahoo Finance, through yfinance, is the planned initial
market data source.

## Installation

Install uv by following the official documentation:

https://docs.astral.sh/uv/getting-started/installation/

From the repository root, run:

```bash
uv python install 3.12
uv sync --locked
```

Verify the installation:

```bash
uv run python -c "import quantlab; print('Installation successful')"
```

## Development

Install the project and development dependencies:

```bash
uv sync --locked
```

### Run Tests

```bash
uv run pytest
```

### Code Coverage

```bash
uv run pytest --cov=quantlab --cov-report=term-missing
```

Generate an HTML coverage report:

```bash
uv run pytest --cov=quantlab --cov-report=html
```

The report is generated at `htmlcov/index.html`.

### Linting and Formatting

```bash
uv run ruff check .
uv run ruff format --check .
```

Automatically fix supported linting issues and format code:

```bash
uv run ruff check . --fix
uv run ruff format .
```

### Static Type Checking

```bash
uv run mypy src
```

### Run All Quality Checks (Windows)

```powershell
.\scripts\check.ps1
```

### Continuous Integration

GitHub Actions runs automated tests, coverage reporting,
linting, formatting, static type checking, and package
build verification on Windows and Linux.

Automated tests use deterministic data and do not require
live market data services or API credentials.

## Repository Structure

- `src/quantlab/`: Shared research infrastructure.
- `projects/`: Individual quantitative finance experiments.
- `tests/`: Automated tests.
- `data/`: Local market data storage.
- `configs/`: Experiment configurations.
- `docs/`: Technical documentation.

## Development Roadmap

Development is organized into incremental phases.

See [ROADMAP.md](ROADMAP.md) for the complete development
plan, implementation progress, and future research projects.

## Project Status

Under active development.

The initial phase focuses on establishing the shared
quantitative research infrastructure before implementing
individual trading strategies.

## Disclaimer

This repository is intended exclusively for educational
and research purposes.

It does not provide financial advice and is not intended
for live trading or real-money execution.
