"""Canonical daily market data schema and explicit instrument metadata."""

from dataclasses import dataclass

from quantlab.data.loader import _normalize_tickers

SCHEMA_VERSION = 1
PRICE_COLUMNS = ("open", "high", "low", "close", "adjusted_close")
NUMERIC_COLUMNS = (*PRICE_COLUMNS, "volume")
COLUMNS = ("timestamp", "symbol", "asset_class", *NUMERIC_COLUMNS, "currency", "source")
ASSET_CLASSES = frozenset(
    {"equity", "etf", "crypto", "forex", "index", "futures", "other"}
)
YAHOO_COLUMNS = {
    "Open": "open",
    "High": "high",
    "Low": "low",
    "Close": "close",
    "Adj Close": "adjusted_close",
    "Volume": "volume",
}


@dataclass(frozen=True, slots=True)
class Instrument:
    """Researcher-supplied instrument metadata; no currency inference."""

    symbol: str
    asset_class: str
    currency: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "symbol", _normalize_tickers(self.symbol)[0])
        kind = self.asset_class.strip().lower()
        if kind not in ASSET_CLASSES:
            raise ValueError(f"Unsupported asset class: {kind!r}")
        object.__setattr__(self, "asset_class", kind)
        if self.currency is not None:
            currency = self.currency.strip().upper()
            if not currency or any(c.isspace() for c in currency):
                raise ValueError("Currency must be a nonempty quote currency code.")
            object.__setattr__(self, "currency", currency)
