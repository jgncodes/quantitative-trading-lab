"""Validate canonical daily observations without inventing missing values."""

import numpy as np
import pandas as pd

from quantlab.data.exceptions import MarketDataError
from quantlab.data.schema import ASSET_CLASSES, COLUMNS, NUMERIC_COLUMNS, PRICE_COLUMNS


class DataValidationError(MarketDataError):
    """Market data violates the canonical daily schema."""


def validate_market_data(frame: pd.DataFrame) -> None:
    """Raise on invalid schema, values, duplicate keys or inconsistent metadata."""
    if list(frame.columns) != list(COLUMNS) or frame.empty:
        raise DataValidationError("Expected nonempty canonical market data columns.")

    if not pd.api.types.is_datetime64_any_dtype(frame["timestamp"].dtype):
        raise DataValidationError("timestamp must have a datetime64 dtype.")
    dates = pd.DatetimeIndex(frame["timestamp"])
    if dates.hasnans or dates.tz is not None or not dates.equals(dates.normalize()):
        raise DataValidationError("Expected timezone-naive midnight session labels.")

    for column in ("symbol", "asset_class", "currency", "source"):
        if not isinstance(frame[column].dtype, pd.StringDtype):
            raise DataValidationError(f"{column} must have Pandas string dtype.")
        values = frame[column].dropna()
        if values.str.strip().eq("").any() or values.str.strip().ne(values).any():
            raise DataValidationError(f"Invalid whitespace in {column}.")
    if frame[["symbol", "asset_class", "source", "close"]].isna().any().any():
        raise DataValidationError("Missing required market data values.")
    if not frame["symbol"].str.upper().eq(frame["symbol"]).all():
        raise DataValidationError("Symbols must be uppercase.")
    if not frame["asset_class"].isin(ASSET_CLASSES).all():
        raise DataValidationError("Unknown asset class.")
    if not frame["source"].eq("yfinance").all():
        raise DataValidationError("Unexpected data source.")
    if frame.duplicated(["symbol", "timestamp"]).any():
        raise DataValidationError("Duplicate symbol/timestamp observations.")
    for column in ("asset_class", "currency", "source"):
        if frame.groupby("symbol")[column].nunique(dropna=False).gt(1).any():
            raise DataValidationError(f"Inconsistent {column} for a symbol.")

    for column in NUMERIC_COLUMNS:
        if frame[column].dtype != np.dtype("float64"):
            raise DataValidationError(f"{column} must have float64 dtype.")
        values = frame[column].dropna()
        if not np.isfinite(values.to_numpy()).all():
            raise DataValidationError(f"Nonfinite values in {column}.")
        if column in PRICE_COLUMNS and values.le(0).any():
            raise DataValidationError(f"Nonpositive prices in {column}.")
        if column == "volume" and values.lt(0).any():
            raise DataValidationError("Negative trading volume.")

    # Small numerical tolerance for vendor rounding; missing values remain missing.
    for lower, upper in (
        ("low", "high"),
        ("low", "open"),
        ("low", "close"),
        ("open", "high"),
        ("close", "high"),
    ):
        if (frame[lower] - frame[upper] > 1e-8 + 1e-6 * frame[upper].abs()).any():
            raise DataValidationError(f"Inconsistent OHLC values: {lower} > {upper}.")
