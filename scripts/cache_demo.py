"""Download (if needed), validate, cache and align a small market dataset."""

from pathlib import Path

from quantlab.data.cache import get_market_data
from quantlab.data.preprocessing import align_prices
from quantlab.data.schema import Instrument


def main() -> None:
    """Demonstrate the cache using observed equity and crypto sessions."""
    instruments = [Instrument("AAPL", "equity", "USD"), Instrument("BTC-USD", "crypto", "USD")]
    cache_dir = Path(__file__).resolve().parents[1] / "data" / "cache"
    data = get_market_data(instruments, "2025-01-01", "2026-01-01", cache_dir=cache_dir)
    print("Canonical data:")
    print(data.head())
    print("\nObservations per asset:")
    print(data.groupby("symbol").size())
    outer = align_prices(data, field="close", join="outer")
    inner = align_prices(data, field="close", join="inner")
    print(f"\nObserved union: {len(outer)} dates; intersection: {len(inner)} dates.")
    print("\nMissing values in outer alignment (not filled):")
    print(outer.isna().sum())
    print(f"\nLocal cache: {cache_dir}")


if __name__ == "__main__":
    main()
