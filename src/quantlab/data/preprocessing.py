"""Normalize Yahoo daily data and align observed trading sessions explicitly."""

from collections.abc import Mapping, Sequence
from typing import Literal

import numpy as np
import pandas as pd

from quantlab.data.schema import COLUMNS, NUMERIC_COLUMNS, YAHOO_COLUMNS, Instrument
from quantlab.data.validation import DataValidationError, validate_market_data


def normalize_market_data(
    raw: Mapping[str, pd.DataFrame], instruments: Sequence[Instrument]
) -> pd.DataFrame:
    """Convert Step 3 per-ticker frames to canonical long-form observations."""
    symbols = [item.symbol for item in instruments]
    if not symbols or len(set(symbols)) != len(symbols):
        raise ValueError("Provide a nonempty sequence of unique instruments.")
    if set(raw) != set(symbols):
        raise DataValidationError("Downloaded symbols do not match requested instruments.")

    frames: list[pd.DataFrame] = []
    for item in instruments:
        frame = raw[item.symbol]
        if frame.empty or not frame.columns.is_unique or "Close" not in frame.columns:
            raise DataValidationError(f"Invalid source columns or rows: {item.symbol}.")
        if not isinstance(frame.index, pd.DatetimeIndex):
            raise DataValidationError("Expected a daily DatetimeIndex.")
        dates = frame.index.tz_localize(None) if frame.index.tz is not None else frame.index
        if dates.hasnans or not dates.equals(dates.normalize()):
            raise DataValidationError("Daily data must use midnight session labels.")
        normalized = pd.DataFrame({"timestamp": dates}, index=range(len(frame)))
        renamed = frame.rename(columns=YAHOO_COLUMNS)
        for column in NUMERIC_COLUMNS:
            if column not in renamed.columns:
                normalized[column] = np.nan
                continue
            try:
                normalized[column] = pd.to_numeric(renamed[column], errors="raise").astype(
                    "float64"
                ).to_numpy()
            except (TypeError, ValueError) as exc:
                raise DataValidationError(f"Invalid numeric field: {item.symbol}/{column}.") from exc
        for column, value in (("symbol", item.symbol), ("asset_class", item.asset_class),
                              ("currency", item.currency), ("source", "yfinance")):
            normalized[column] = pd.Series(value, index=normalized.index, dtype="string")
        frames.append(normalized.loc[:, list(COLUMNS)])

    result = pd.concat(frames, ignore_index=True).sort_values(
        ["symbol", "timestamp"], ignore_index=True
    )
    validate_market_data(result)
    return result


def align_prices(
    frame: pd.DataFrame,
    *,
    field: Literal["close", "adjusted_close"] = "adjusted_close",
    join: Literal["inner", "outer"] = "inner",
) -> pd.DataFrame:
    """Pivot on observed session labels; never fill closures or missing prices."""
    validate_market_data(frame)
    if field not in {"close", "adjusted_close"} or join not in {"inner", "outer"}:
        raise ValueError("Unsupported price field or join mode.")
    prices = frame.pivot(index="timestamp", columns="symbol", values=field).sort_index()
    if prices.isna().all().any():
        raise DataValidationError(f"At least one instrument lacks all {field} values.")
    if join == "inner":
        prices = prices.dropna(how="any")
    if prices.empty:
        raise DataValidationError("No common observations for the requested alignment.")
    return prices
