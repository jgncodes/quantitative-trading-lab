"""Unit tests for historical market data collection."""

from unittest.mock import patch

import numpy as np
import pandas as pd
import pytest

from quantlab.data import MarketDataError, load_historical_data

START_DATE = "2025-01-01"
END_DATE = "2025-02-01"


@pytest.fixture
def sample_data() -> pd.DataFrame:
    """Create deterministic synthetic historical prices."""
    dates = pd.date_range(
        "2025-01-02",
        periods=3,
        freq="D",
        name="Date",
    )

    return pd.DataFrame(
        {
            "Open": [100.0, 102.0, 104.0],
            "High": [103.0, 105.0, 107.0],
            "Low": [99.0, 101.0, 103.0],
            "Close": [102.0, 104.0, 106.0],
            "Adj Close": [102.0, 104.0, 106.0],
            "Volume": [1000, 1200, 1100],
        },
        index=dates,
    )


def test_single_ticker_flat_response(
    sample_data: pd.DataFrame,
) -> None:
    """Verify support for single-ticker flat columns."""
    with patch(
        "quantlab.data.loader.yf.download",
        return_value=sample_data,
    ):
        result = load_historical_data(
            "AAPL",
            START_DATE,
            END_DATE,
        )

    assert list(result) == ["AAPL"]
    pd.testing.assert_frame_equal(result["AAPL"], sample_data)


def test_single_ticker_multiindex_response(
    sample_data: pd.DataFrame,
) -> None:
    """Verify support for hierarchical single-ticker columns."""
    response = pd.concat({"AAPL": sample_data}, axis=1)

    with patch(
        "quantlab.data.loader.yf.download",
        return_value=response,
    ):
        result = load_historical_data(
            "AAPL",
            START_DATE,
            END_DATE,
        )

    pd.testing.assert_frame_equal(result["AAPL"], sample_data)


def test_multiple_tickers(
    sample_data: pd.DataFrame,
) -> None:
    """Verify that multiple ticker responses are separated."""
    response = pd.concat(
        {
            "AAPL": sample_data,
            "MSFT": sample_data,
        },
        axis=1,
    )

    with patch(
        "quantlab.data.loader.yf.download",
        return_value=response,
    ):
        result = load_historical_data(
            ["AAPL", "MSFT"],
            START_DATE,
            END_DATE,
        )

    assert set(result) == {"AAPL", "MSFT"}

    pd.testing.assert_frame_equal(result["AAPL"], sample_data)
    pd.testing.assert_frame_equal(result["MSFT"], sample_data)


def test_normalized_tickers(
    sample_data: pd.DataFrame,
) -> None:
    """Verify normalization of lowercase ticker symbols."""
    with patch(
        "quantlab.data.loader.yf.download",
        return_value=sample_data,
    ) as download:
        result = load_historical_data(
            " aapl ",
            START_DATE,
            END_DATE,
        )

    assert "AAPL" in result
    assert download.call_args.kwargs["tickers"] == ["AAPL"]


def test_download_configuration(
    sample_data: pd.DataFrame,
) -> None:
    """Verify explicit data collection conventions."""
    with patch(
        "quantlab.data.loader.yf.download",
        return_value=sample_data,
    ) as download:
        load_historical_data(
            "AAPL",
            START_DATE,
            END_DATE,
        )

    kwargs = download.call_args.kwargs

    assert kwargs["start"] == START_DATE
    assert kwargs["end"] == END_DATE
    assert kwargs["interval"] == "1d"
    assert kwargs["auto_adjust"] is False
    assert kwargs["group_by"] == "ticker"
    assert kwargs["multi_level_index"] is True


@pytest.mark.parametrize(
    "tickers",
    [
        [],
        "",
        "   ",
        "AAPL MSFT",
        "AAPL,MSFT",
        ["AAPL", "aapl"],
    ],
)
def test_invalid_tickers(
    tickers: str | list[str],
) -> None:
    """Reject invalid ticker requests before downloading."""
    with patch("quantlab.data.loader.yf.download") as download:
        with pytest.raises(ValueError):
            load_historical_data(
                tickers,
                START_DATE,
                END_DATE,
            )

    download.assert_not_called()


@pytest.mark.parametrize(
    ("start", "end"),
    [
        ("invalid", "2025-02-01"),
        ("2025-01-01", "invalid"),
        ("2025-02-01", "2025-01-01"),
        ("2025-01-01", "2025-01-01"),
        ("20250101", "2025-02-01"),
    ],
)
def test_invalid_dates(
    start: str,
    end: str,
) -> None:
    """Reject invalid or incorrectly ordered dates."""
    with patch("quantlab.data.loader.yf.download") as download:
        with pytest.raises(ValueError):
            load_historical_data(
                "AAPL",
                start,
                end,
            )

    download.assert_not_called()


@pytest.mark.parametrize(
    "response",
    [None, pd.DataFrame()],
)
def test_empty_response(
    response: pd.DataFrame | None,
) -> None:
    """Reject empty Yahoo Finance responses."""
    with patch(
        "quantlab.data.loader.yf.download",
        return_value=response,
    ):
        with pytest.raises(MarketDataError):
            load_historical_data(
                "AAPL",
                START_DATE,
                END_DATE,
            )


def test_network_failure() -> None:
    """Convert external download errors into market data errors."""
    with patch(
        "quantlab.data.loader.yf.download",
        side_effect=ConnectionError("Network unavailable"),
    ):
        with pytest.raises(MarketDataError):
            load_historical_data(
                "AAPL",
                START_DATE,
                END_DATE,
            )


def test_partial_download_failure(
    sample_data: pd.DataFrame,
) -> None:
    """Reject requests when a ticker is missing."""
    response = pd.concat({"AAPL": sample_data}, axis=1)

    with patch(
        "quantlab.data.loader.yf.download",
        return_value=response,
    ):
        with pytest.raises(MarketDataError, match="MSFT"):
            load_historical_data(
                ["AAPL", "MSFT"],
                START_DATE,
                END_DATE,
            )


def test_all_missing_ticker_prices(
    sample_data: pd.DataFrame,
) -> None:
    """Reject ticker responses containing no closing prices."""
    response = sample_data.copy()
    response["Close"] = np.nan

    with patch(
        "quantlab.data.loader.yf.download",
        return_value=response,
    ):
        with pytest.raises(MarketDataError):
            load_historical_data(
                "AAPL",
                START_DATE,
                END_DATE,
            )


def test_missing_close_column(
    sample_data: pd.DataFrame,
) -> None:
    """Reject responses without a closing-price column."""
    response = sample_data.drop(columns=["Close"])

    with patch(
        "quantlab.data.loader.yf.download",
        return_value=response,
    ):
        with pytest.raises(MarketDataError):
            load_historical_data(
                "AAPL",
                START_DATE,
                END_DATE,
            )


def test_missing_observations(
    sample_data: pd.DataFrame,
) -> None:
    """Verify missing closing prices are not forward-filled."""
    response = sample_data.copy()
    response.loc[response.index[1], "Close"] = np.nan

    with patch(
        "quantlab.data.loader.yf.download",
        return_value=response,
    ):
        result = load_historical_data(
            "AAPL",
            START_DATE,
            END_DATE,
        )

    assert len(result["AAPL"]) == 2
    assert result["AAPL"]["Close"].notna().all()


def test_different_trading_calendars(
    sample_data: pd.DataFrame,
) -> None:
    """Preserve different stock and cryptocurrency observations."""
    stock = sample_data.iloc[:2].copy()
    crypto = sample_data.copy()

    response = pd.concat(
        {
            "AAPL": stock,
            "BTC-USD": crypto,
        },
        axis=1,
    )

    with patch(
        "quantlab.data.loader.yf.download",
        return_value=response,
    ):
        result = load_historical_data(
            ["AAPL", "BTC-USD"],
            START_DATE,
            END_DATE,
        )

    assert len(result["AAPL"]) == 2
    assert len(result["BTC-USD"]) == 3


def test_chronological_order(
    sample_data: pd.DataFrame,
) -> None:
    """Verify historical observations are sorted chronologically."""
    response = sample_data.iloc[::-1]

    with patch(
        "quantlab.data.loader.yf.download",
        return_value=response,
    ):
        result = load_historical_data(
            "AAPL",
            START_DATE,
            END_DATE,
        )

    assert result["AAPL"].index.is_monotonic_increasing
