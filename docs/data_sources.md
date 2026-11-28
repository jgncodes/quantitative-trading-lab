# Historical market data conventions

## Scope

`yfinance` is the only provider. Step 3's `load_historical_data` returns
per-ticker Yahoo frames. Step 4's `get_market_data` returns a validated long-form
DataFrame and uses a local Parquet cache. No live requests occur in unit tests.

## Canonical daily schema

One row per `(symbol, timestamp)`. Timestamp is a timezone-naive midnight
**session label**, not an execution instant. If an input daily index has a
zone, the local date is preserved rather than converted to UTC. Intraday
and duplicate labels are rejected. Output is sorted by symbol and date.

`symbol`, `asset_class`, `currency`, and `source` are Pandas string columns.
The researcher specifies instrument classification and quote currency;
unknown currency stays missing. This metadata is not verified by Yahoo.
`open`, `high`, `low`, `close`, `adjusted_close`, and `volume` are float64.
Closing prices must exist and be finite and positive; optional fields may be
missing, but nonfinite or invalid values are rejected when present. Volume must
be nonnegative. OHLC relationships are validated with a small rounding tolerance.
Instruments that can have negative prices are outside this initial schema.

## Price adjustment and corporate actions

The loader requests `auto_adjust=False` and `actions=False`. `close` and OHLC
are Yahoo-reported fields and can already reflect splits; they are not promised
to be original execution prices. `adjusted_close` is the separately reported
adjusted series and is a historical total-return proxy for equities, not a fill
price. Do not add dividends again to adjusted-close returns. Missing adjusted
close stays missing; choose `close` explicitly if appropriate. Corporate-action
cash flows, execution-price semantics and short financing remain deferred to
portfolio accounting/backtesting. Historical vendor data can be revised and
may incorporate later-known adjustments; it is not a point-in-time archive.

## Calendars and currency

`align_prices(..., join="outer")` preserves the observed union with missing
cells; `join="inner"` keeps rows with every requested price present. It does
not generate synthetic market sessions, verify exchange holiday schedules,
or establish simultaneous equity and crypto closing times. A missing row can
mean a closure, unavailable history, or a data gap. Do not forward-fill
missing values and pretend they are tradeable bars. Use an explicit valuation
policy if mark-to-market prices are carried forward in a future backtester.
The intersection may omit weekend crypto movement; don't treat it as a full
crypto calendar for annualization. No currency conversion is implemented.
Use same-currency instruments for initial portfolio accounting.

## Cache behavior

Cache keys are SHA-256 hashes of canonical request metadata including schema
version, provider, sorted instrument metadata, date bounds and fixed download
options. The start is inclusive and end exclusive. Identical requests reuse
one entry regardless of input ticker ordering; differing ranges are independent
entries. Each entry has a Parquet file and JSON manifest recording request,
retrieval time, row count and SHA-256 checksum. Reads verify checksum, schema,
metadata and date bounds. This does not prove the provider supplied every
expected session. A missing half of an existing entry or corrupted content
raises `CacheError`; explicitly use `refresh=True` to fetch again. Successful
refresh replaces the existing snapshot; there is no TTL or incremental merging.
Writes stage both files first; individual replacements are atomic on the same
filesystem, but the pair is not a transactional database. An interruption
between replacements is detected by the checksum. Single-writer use only.
Pin closed historical date ranges when researching. Record the manifest with
experiment provenance and retain snapshots separately if needed.

Keep all provider data and cache files out of Git. Do not redistribute data
without confirming applicable rights. Cache is local convenience, not a market
feed or guarantee of complete or accurate data.

## Example

```python
from quantlab.data.cache import get_market_data
from quantlab.data.preprocessing import align_prices
from quantlab.data.schema import Instrument

instruments = [Instrument("AAPL", "equity", "USD"), Instrument("MSFT", "equity", "USD")]
data = get_market_data(instruments, "2020-01-01", "2026-01-01")
prices = align_prices(data, field="adjusted_close", join="inner")
```

Run `uv run python scripts/cache_demo.py` manually to fetch actual data. Run it
again to use the same cache. Normal CI uses mocked data only.
