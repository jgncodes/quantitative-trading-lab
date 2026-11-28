"""Local request-addressed Parquet cache for daily Yahoo Finance observations."""

import hashlib
import json
from collections.abc import Sequence
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from tempfile import TemporaryDirectory

import pandas as pd

from quantlab.data.exceptions import MarketDataError
from quantlab.data.loader import _validate_dates, load_historical_data
from quantlab.data.preprocessing import normalize_market_data
from quantlab.data.schema import SCHEMA_VERSION, Instrument
from quantlab.data.validation import DataValidationError, validate_market_data


class CacheError(MarketDataError):
    """Cache entry cannot be safely read or written."""


def _digest(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def _validate_request_data(
    frame: pd.DataFrame, instruments: Sequence[Instrument], start: str, end: str
) -> None:
    validate_market_data(frame)
    if set(frame["symbol"]) != {item.symbol for item in instruments}:
        raise DataValidationError("Dataset symbols do not match request.")
    if (frame["timestamp"] < pd.Timestamp(start)).any() or (
        frame["timestamp"] >= pd.Timestamp(end)
    ).any():
        raise DataValidationError(
            "Dataset contains observations outside request range."
        )
    for item in instruments:
        rows = frame.loc[frame["symbol"] == item.symbol]
        if not rows["asset_class"].eq(item.asset_class).all():
            raise DataValidationError("Instrument classification mismatch.")
        if item.currency is None:
            matches = rows["currency"].isna().all()
        else:
            matches = (
                rows["currency"].notna().all()
                and rows["currency"].eq(item.currency).all()
            )
        if not matches:
            raise DataValidationError("Instrument currency mismatch.")


def get_market_data(
    instruments: Sequence[Instrument],
    start_date: str,
    end_date: str,
    *,
    cache_dir: str | Path = Path("data/cache"),
    refresh: bool = False,
) -> pd.DataFrame:
    """Return validated canonical data; fetch only on a miss or explicit refresh.

    A corrupted or incomplete cache entry raises CacheError. Refresh explicitly
    to replace it. This initial cache assumes one writer at a time.
    """
    _validate_dates(start_date, end_date)
    items = sorted(instruments, key=lambda item: item.symbol)
    symbols = [item.symbol for item in items]
    if not symbols or len(set(symbols)) != len(symbols):
        raise ValueError("Provide a nonempty sequence of unique instruments.")
    request = {
        "schema_version": SCHEMA_VERSION,
        "source": "yfinance",
        "interval": "1d",
        "auto_adjust": False,
        "actions": False,
        "start_date": start_date,
        "end_date": end_date,
        "instruments": [asdict(item) for item in items],
    }
    key = hashlib.sha256(
        json.dumps(request, sort_keys=True).encode("utf-8")
    ).hexdigest()
    directory = Path(cache_dir)
    parquet_path = directory / f"{key}.parquet"
    metadata_path = directory / f"{key}.json"

    if not refresh and (parquet_path.exists() or metadata_path.exists()):
        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            if metadata["request"] != request or metadata["sha256"] != _digest(
                parquet_path
            ):
                raise ValueError("Cache request or checksum mismatch.")
            frame = pd.read_parquet(parquet_path, engine="pyarrow")
            if len(frame) != metadata["rows"]:
                raise ValueError("Cache row count mismatch.")
            _validate_request_data(frame, items, start_date, end_date)
            return frame
        except Exception as exc:
            raise CacheError(
                f"Invalid cache entry {key}; retry with refresh=True."
            ) from exc

    raw = load_historical_data(symbols, start_date, end_date)
    frame = normalize_market_data(raw, items)
    _validate_request_data(frame, items, start_date, end_date)
    try:
        directory.mkdir(parents=True, exist_ok=True)
        # Stage both files before replacing the existing entry.
        with TemporaryDirectory(dir=directory) as temporary:
            staged_data = Path(temporary) / parquet_path.name
            staged_metadata = Path(temporary) / metadata_path.name
            frame.to_parquet(staged_data, engine="pyarrow", index=False)
            metadata = {
                "request": request,
                "retrieved_at_utc": datetime.now(UTC).isoformat(),
                "rows": len(frame),
                "sha256": _digest(staged_data),
            }
            staged_metadata.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
            staged_data.replace(parquet_path)
            staged_metadata.replace(metadata_path)
    except Exception as exc:
        raise CacheError(f"Could not write cache entry {key}.") from exc
    return frame
