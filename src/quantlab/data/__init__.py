"""market data collection and processing utitlies"""

from quantlab.data.exceptions import MarketDataError
from quantlab.data.loader import load_historical_data

__all__ = [
    "MarketDataError",
    "load_historical_data",
]
