"""demonstrate historical market data collection."""

from quantlab.data import MarketDataError, load_historical_data


def main() -> None:
    """download and summarize sample historical market data"""
    tickers = [
        "AAPL",
        "MSFT",
        "SPY",
        "BTC-USD",
        "ETH-USD",
    ]

    try:
        data = load_historical_data(
            tickers=tickers, start_date="2020-01-01", end_date="2026-01-01"
        )

    except MarketDataError as exc:
        raise SystemExit(f"Download failed: {exc}") from exc

    print("\nHistorical Market Data")
    print("=" * 70)

    for symbol, frame in data.items():
        print(f"\nTicker: {symbol}")
        print("=" * 70)

        print(f"Observations: {len(frame):,}")
        print(f"First observation: {frame.index.min()}")
        print(f"Last observation: {frame.index.max()}")
        print(f"Columns: {list(frame.columns)}")

        print("\nMost recent observations:")
        print(frame.tail())

        print("\nMissing values:")
        print(frame.isna().sum())

    print("\nAll requested datasets downloaded successfully.")


if __name__ == "__main__":
    main()
