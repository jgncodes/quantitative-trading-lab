"hisotrical market data collection (yahoo finance)"

from collections.abc import Sequence
from datetime import date

import pandas as pd
import yfinance as yf

from quantlab.data.exceptions import MarketDataError


def _normalize_tickers(
    tickers: str | Sequence[str],
) -> list[str]:
    "normalizes and validates requested ticker symbols"

    symbols = [tickers] if isinstance(tickers, str) else list(tickers)

    if not symbols:
        raise ValueError("At least one ticker must be provided.")

    normalized = []

    for symbol in symbols:
        symbol = symbol.strip().upper()

        if not symbol or any(char.isspace() for char in symbol):
            raise ValueError(f"Invalid ticker symbol: {symbol!r}")

        if "," in symbol:
            raise ValueError("Provide multiple tickers as a sequence.")

        normalized.append(symbol)

    if len(normalized) != len(set(normalized)):
        raise ValueError("Duplicate ticker symbols not allowed.")

    return normalized


def _validate_dates(start_date: str, end_date: str) -> None:
    "validaes ISO formatted dates and chronological order"
    try:
        start = date.fromisoformat(start_date)
        end = date.fromisoformat(end_date)
    except ValueError as exc:
        raise ValueError("Dates must use YYYY-MM-DD format") from exc

    if start.isoformat() != start_date or end.isoformat() != end_date:
        raise ValueError("Both dates must use YYYY-MM-DD format")

    if start >= end:
        raise ValueError("start_date must be earlier than end_date")


def _extract_ticker_data(
    raw_data: pd.DataFrame,
    symbol: str,
    single_ticker: bool,
) -> pd.DataFrame:
    "extract one ticker from a yahoo finance response"
    if isinstance(raw_data.columns, pd.MultiIndex):
        if raw_data.columns.nlevels != 2:
            raise MarketDataError("Unexpected Yahoo Finance column structure")

        if symbol not in raw_data.columns.get_level_values(0):
            raise MarketDataError(f"No data returned for {symbol}.")

        frame = raw_data.xs(symbol, axis=1, level=0)

    elif single_ticker:
        frame = raw_data.copy()

    else:
        raise MarketDataError("Unexpected response formate for multiple tickers.")

    if not isinstance(frame, pd.DataFrame):
        raise MarketDataError(f"Unexpected data structure for {symbol}.")

    if "Close" not in frame.columns:
        raise MarketDataError(f"Missing closing prices for {symbol}.")

    # removing empty rows introduced by different trading calendars
    # missing prices are never forward filled

    frame = frame.dropna(subset=["Close"]).copy()

    if frame.empty:
        raise MarketDataError(f"No useable historical data returned for {symbol}.")

    return frame.sort_index()


def load_historical_data(
    tickers: str | Sequence[str], start_date: str, end_date: str
) -> dict[str, pd.DataFrame]:
    """
    retreived daily historical market data from yahoo finance

    Parameters
    ------------
    tickers:
        one yahoo finance ticker or a sequence of ticker symbols
    start_date:
        Inclusive start ddata in YYYY-MM-DD format.
    end_date:
        Exclusive end date in YYYY-MM-DD format.

    Returns
    ------------
    dict[str, pd.DataFrame]
        Historical market data organized by ticker symbol.

    Raises
    ------------
    ValueError
        If ticker symbols or dates are invalid.
    MarketDataError
        If the download fails or a requested ticker has no usable data.
    """

    symbols = _normalize_tickers(tickers)
    _validate_dates(start_date, end_date)

    try:
        raw_data = yf.download(
            tickers=symbols,
            start=start_date,
            end=end_date,
            interval="1d",
            auto_adjust=False,
            actions=False,
            prepost=False,
            group_by="ticker",
            multi_level_index=True,
            ignore_tz=True,
            threads=False,
            progress=False,
            timeout=30,
        )
    except Exception as exc:
        raise MarketDataError(
            f"Failed to download historical data for {symbols}."
        ) from exc

    if not isinstance(raw_data, pd.DataFrame) or raw_data.empty:
        raise MarketDataError(f"Yahoo Finance returned no data for {symbols}")

    result: dict[str, pd.DataFrame] = {}

    for symbol in symbols:
        result[symbol] = _extract_ticker_data(
            raw_data=raw_data,
            symbol=symbol,
            single_ticker=len(symbols) == 1,
        )

    return result
