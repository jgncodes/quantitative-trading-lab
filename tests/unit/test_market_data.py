"""Offline tests of schema normalization, validation, alignment and Parquet cache."""

from pathlib import Path
from unittest.mock import patch

import numpy as np
import pandas as pd
import pytest

from quantlab.data.cache import CacheError, get_market_data
from quantlab.data.preprocessing import align_prices, normalize_market_data
from quantlab.data.schema import COLUMNS, Instrument
from quantlab.data.validation import DataValidationError, validate_market_data

START = "2025-01-03"
END = "2025-01-07"
STOCK = Instrument("aapl", "equity", "usd")
CRYPTO = Instrument("BTC-USD", "crypto", "USD")


@pytest.fixture
def raw() -> dict[str, pd.DataFrame]:
    """Friday/Monday stock sessions and a seven-day crypto calendar."""
    stock = pd.DataFrame(
        {
            "Open": [100.0, 102.0],
            "High": [105.0, 106.0],
            "Low": [98.0, 100.0],
            "Close": [102.0, 104.0],
            "Adj Close": [101.0, 103.0],
            "Volume": [1000, 1200],
        },
        index=pd.to_datetime(["2025-01-03", "2025-01-06"]),
    )
    crypto = pd.DataFrame(
        {
            "Close": [200.0, 201.0, 202.0, 203.0],
            "Adj Close": [200.0, 201.0, 202.0, 203.0],
        },
        index=pd.date_range(START, periods=4),
    )
    return {"AAPL": stock, "BTC-USD": crypto}


def test_normalization(raw: dict[str, pd.DataFrame]) -> None:
    frame = normalize_market_data(raw, [STOCK, CRYPTO])
    assert list(frame.columns) == list(COLUMNS)
    assert len(frame) == 6
    assert frame["symbol"].tolist() == ["AAPL"] * 2 + ["BTC-USD"] * 4
    assert frame.loc[0, "close"] == 102.0
    assert frame.loc[0, "adjusted_close"] == 101.0
    assert frame.loc[frame["symbol"] == "BTC-USD", "volume"].isna().all()
    assert frame["source"].eq("yfinance").all()
    validate_market_data(frame)


def test_optional_currency_and_adjusted_price(raw: dict[str, pd.DataFrame]) -> None:
    frame = normalize_market_data(
        {"AAPL": raw["AAPL"].drop(columns="Adj Close")}, [Instrument("AAPL", "equity")]
    )
    assert frame["currency"].isna().all()
    assert frame["adjusted_close"].isna().all()
    with pytest.raises(DataValidationError, match="lacks all"):
        align_prices(frame)
    assert align_prices(frame, field="close").iloc[0, 0] == 102.0


def test_session_labels_and_sorting(raw: dict[str, pd.DataFrame]) -> None:
    frame = raw["AAPL"].iloc[::-1].copy()
    frame.index = pd.DatetimeIndex(frame.index).tz_localize("America/New_York")
    result = normalize_market_data({"AAPL": frame}, [STOCK])
    assert result["timestamp"].tolist() == list(pd.to_datetime([START, "2025-01-06"]))


@pytest.mark.parametrize(
    "field,value",
    [
        ("Close", 0.0),
        ("Close", np.nan),
        ("Close", np.inf),
        ("High", 1.0),
        ("Volume", -1.0),
        ("Open", "not-a-number"),
    ],
)
def test_bad_values(raw: dict[str, pd.DataFrame], field: str, value: object) -> None:
    stock = raw["AAPL"].copy()
    stock[field] = value
    with pytest.raises(DataValidationError):
        normalize_market_data({"AAPL": stock}, [STOCK])


def test_duplicate_observations(raw: dict[str, pd.DataFrame]) -> None:
    stock = pd.concat([raw["AAPL"], raw["AAPL"].iloc[:1]])
    with pytest.raises(DataValidationError, match="Duplicate"):
        normalize_market_data({"AAPL": stock}, [STOCK])


def test_intraday_labels_rejected(raw: dict[str, pd.DataFrame]) -> None:
    stock = raw["AAPL"].copy()
    stock.index = pd.DatetimeIndex(stock.index) + pd.Timedelta(hours=12)
    with pytest.raises(DataValidationError, match="midnight"):
        normalize_market_data({"AAPL": stock}, [STOCK])


def test_missing_ticker(raw: dict[str, pd.DataFrame]) -> None:
    with pytest.raises(DataValidationError, match="symbols"):
        normalize_market_data({"AAPL": raw["AAPL"]}, [STOCK, CRYPTO])


@pytest.mark.parametrize("join,expected_rows", [("inner", 2), ("outer", 4)])
def test_alignment(raw: dict[str, pd.DataFrame], join: str, expected_rows: int) -> None:
    frame = normalize_market_data(raw, [STOCK, CRYPTO])
    prices = align_prices(frame, join=join)  # type: ignore[arg-type]
    assert len(prices) == expected_rows
    assert list(prices.columns) == ["AAPL", "BTC-USD"]
    if join == "outer":
        assert pd.isna(prices.loc[pd.Timestamp("2025-01-04"), "AAPL"])
    else:
        assert prices.loc[pd.Timestamp(START), "AAPL"] == 101.0


def test_cache_roundtrip_and_order_independence(
    raw: dict[str, pd.DataFrame], tmp_path: Path
) -> None:
    with patch("quantlab.data.cache.load_historical_data", return_value=raw) as loader:
        first = get_market_data([STOCK, CRYPTO], START, END, cache_dir=tmp_path)
        second = get_market_data([CRYPTO, STOCK], START, END, cache_dir=tmp_path)
    loader.assert_called_once_with(["AAPL", "BTC-USD"], START, END)
    pd.testing.assert_frame_equal(first, second)
    assert len(list(tmp_path.glob("*.parquet"))) == 1
    assert len(list(tmp_path.glob("*.json"))) == 1


def test_cache_refresh(raw: dict[str, pd.DataFrame], tmp_path: Path) -> None:
    with patch("quantlab.data.cache.load_historical_data", return_value=raw) as loader:
        first = get_market_data([STOCK, CRYPTO], START, END, cache_dir=tmp_path)
        updated = {symbol: frame.copy() for symbol, frame in raw.items()}
        updated["BTC-USD"]["Close"] = 250.0
        loader.return_value = updated
        second = get_market_data(
            [STOCK, CRYPTO], START, END, cache_dir=tmp_path, refresh=True
        )
        third = get_market_data([STOCK, CRYPTO], START, END, cache_dir=tmp_path)
    assert loader.call_count == 2
    assert not first.equals(second)
    pd.testing.assert_frame_equal(second, third)


@pytest.mark.parametrize(
    "corruption", ["parquet", "metadata", "missing_parquet", "missing_metadata"]
)
def test_corruption_requires_explicit_refresh(
    raw: dict[str, pd.DataFrame], tmp_path: Path, corruption: str
) -> None:
    with patch("quantlab.data.cache.load_historical_data", return_value=raw) as loader:
        get_market_data([STOCK, CRYPTO], START, END, cache_dir=tmp_path)
        parquet = next(tmp_path.glob("*.parquet"))
        manifest = next(tmp_path.glob("*.json"))
        if corruption == "parquet":
            parquet.write_bytes(b"corrupt")
        elif corruption == "metadata":
            manifest.write_text("{}", encoding="utf-8")
        elif corruption == "missing_parquet":
            parquet.unlink()
        else:
            manifest.unlink()
        with pytest.raises(CacheError, match="refresh=True"):
            get_market_data([STOCK, CRYPTO], START, END, cache_dir=tmp_path)
        assert loader.call_count == 1
        repaired = get_market_data(
            [STOCK, CRYPTO], START, END, cache_dir=tmp_path, refresh=True
        )
        assert len(repaired) == 6
    assert loader.call_count == 2


def test_cache_key_includes_dates_and_metadata(
    raw: dict[str, pd.DataFrame], tmp_path: Path
) -> None:
    with patch("quantlab.data.cache.load_historical_data", return_value=raw) as loader:
        get_market_data([STOCK, CRYPTO], START, END, cache_dir=tmp_path)
        get_market_data([STOCK, CRYPTO], START, "2025-01-08", cache_dir=tmp_path)
        get_market_data(
            [Instrument("AAPL", "equity"), CRYPTO], START, END, cache_dir=tmp_path
        )
    assert loader.call_count == 3
    assert len(list(tmp_path.glob("*.parquet"))) == 3


def test_reject_outside_requested_range(
    raw: dict[str, pd.DataFrame], tmp_path: Path
) -> None:
    with patch("quantlab.data.cache.load_historical_data", return_value=raw):
        with pytest.raises(DataValidationError, match="outside"):
            get_market_data([STOCK, CRYPTO], START, "2025-01-06", cache_dir=tmp_path)
    assert not list(tmp_path.iterdir())


def test_failed_refresh_preserves_entry(
    raw: dict[str, pd.DataFrame], tmp_path: Path
) -> None:
    with patch("quantlab.data.cache.load_historical_data", return_value=raw) as loader:
        first = get_market_data([STOCK, CRYPTO], START, END, cache_dir=tmp_path)
        loader.side_effect = RuntimeError("Simulated download failure")
        with pytest.raises(RuntimeError, match="Simulated"):
            get_market_data(
                [STOCK, CRYPTO], START, END, cache_dir=tmp_path, refresh=True
            )
        second = get_market_data([STOCK, CRYPTO], START, END, cache_dir=tmp_path)
    pd.testing.assert_frame_equal(first, second)
