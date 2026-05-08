"""
OHLC data fetcher — Schwab API only (real-time), plus Coinbase for BTC.
Handles timeframe resampling for intervals not natively supported.
No yfinance fallback — if Schwab is unavailable, fetches fail with a clear error.
"""

import logging
from datetime import datetime, timezone

import pandas as pd
import requests

from .config import TIMEFRAMES, yf_symbol
from typing import Optional, List, Dict, Set, Union

logger = logging.getLogger(__name__)

# Track which data source was used for the current scan
_data_source_stats = {"schwab": 0, "yfinance": 0, "failed": 0}


def get_data_source_stats() -> dict:
    """Return counts of Schwab vs yfinance fetches in the current scan."""
    return dict(_data_source_stats)


def reset_data_source_stats():
    """Reset data source counters (call at start of each scan)."""
    _data_source_stats.update(schwab=0, yfinance=0, failed=0)


def fetch_ohlc(ticker: str, timeframe: str) -> Optional[pd.DataFrame]:
    """
    Fetch OHLC data for a ticker at a given timeframe.
    Routes BTC to Coinbase, everything else to Schwab.
    Returns DataFrame with columns: Open, High, Low, Close, Volume
    Index is DatetimeIndex (UTC).
    Returns None on failure.
    """
    if ticker == "BTC":
        df = _fetch_ohlc_coinbase(timeframe)
        if df is not None and not df.empty:
            _data_source_stats["schwab"] += 1  # count in schwab bucket (successful fetch)
            return df
        _data_source_stats["failed"] += 1
        return None

    df = _fetch_ohlc_schwab(ticker, timeframe)
    if df is not None and not df.empty:
        _data_source_stats["schwab"] += 1
        return df

    _data_source_stats["failed"] += 1
    return None


# Coinbase granularity mapping: our timeframe → seconds
_COINBASE_GRANULARITY = {
    "1m": 60, "3m": 60, "5m": 300, "10m": 300, "15m": 900,
    "20m": 900, "30m": 900, "1h": 3600, "2h": 3600, "4h": 3600,
    "1D": 86400, "1W": 86400,
}
_COINBASE_RESAMPLE = {
    "3m": 3, "10m": 2, "20m": (4, 300), "30m": 2, "2h": 2, "4h": 4, "1W": 7,
}


def _fetch_ohlc_coinbase(timeframe: str) -> Optional[pd.DataFrame]:
    """Fetch BTC-USD candles from Coinbase Exchange API (no auth required)."""
    try:
        granularity = _COINBASE_GRANULARITY.get(timeframe)
        if granularity is None:
            logger.warning("Coinbase: unsupported timeframe %s", timeframe)
            return None

        # Determine how many candles to fetch (max 300 per request)
        url = "https://api.exchange.coinbase.com/products/BTC-USD/candles"
        params = {"granularity": granularity}
        resp = requests.get(url, params=params, timeout=10,
                            headers={"User-Agent": "OpenClaw/1.0"})
        resp.raise_for_status()
        data = resp.json()

        if not data or not isinstance(data, list):
            logger.warning("Coinbase: empty response for BTC @ %s", timeframe)
            return None

        # Coinbase returns: [[timestamp, low, high, open, close, volume], ...]
        # Sorted newest-first, so reverse
        data.reverse()
        df = pd.DataFrame(data, columns=["timestamp", "Low", "High", "Open", "Close", "Volume"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s", utc=True)
        df.set_index("timestamp", inplace=True)
        df = df[["Open", "High", "Low", "Close", "Volume"]].astype(float)

        # Resample if needed (e.g. 3m from 1m, 10m from 5m, etc.)
        resample_info = _COINBASE_RESAMPLE.get(timeframe)
        if resample_info is not None:
            if isinstance(resample_info, tuple):
                factor, _ = resample_info
            else:
                factor = resample_info
            df = _resample_ohlc(df, factor)

        if len(df) < 10:
            logger.warning("Coinbase: only %d candles for BTC @ %s", len(df), timeframe)
            return None

        return df

    except requests.exceptions.RequestException as e:
        logger.warning("Coinbase fetch failed for BTC @ %s: %s", timeframe, e)
        return None
    except Exception:
        logger.warning("Coinbase fetch error for BTC @ %s", timeframe, exc_info=True)
        return None


def _fetch_ohlc_schwab(ticker: str, timeframe: str) -> Optional[pd.DataFrame]:
    """Fetch from Schwab API. Returns None with error logging if unavailable."""
    try:
        from .schwab_fetcher import is_schwab_available, fetch_ohlc_schwab
        if not is_schwab_available():
            logger.warning("Schwab API not authenticated — cannot fetch %s @ %s. Re-authenticate at /api/schwab/auth", ticker, timeframe)
            return None
        return fetch_ohlc_schwab(ticker, timeframe)
    except ImportError:
        logger.error("schwab_fetcher module not available — cannot fetch data. Schwab is the only data source.")
        return None
    except Exception:
        logger.warning("Schwab fetch failed for %s @ %s", ticker, timeframe)
        return None


def _resample_ohlc(df: pd.DataFrame, factor: int) -> pd.DataFrame:
    """
    Resample OHLC data by combining `factor` consecutive candles.
    E.g., factor=2 on 1h data → 2h candles.
    """
    if df.empty or factor <= 1:
        return df

    # Group every `factor` rows together
    n = len(df)
    groups = [i // factor for i in range(n)]
    grouped = df.groupby(groups)

    resampled = pd.DataFrame({
        "Open": grouped["Open"].first(),
        "High": grouped["High"].max(),
        "Low": grouped["Low"].min(),
        "Close": grouped["Close"].last(),
    })

    if "Volume" in df.columns:
        resampled["Volume"] = grouped["Volume"].sum()

    # Use the timestamp of the first candle in each group
    resampled.index = grouped.apply(lambda g: g.index[0])
    resampled.index.name = df.index.name

    return resampled


def fetch_latest_price(ticker: str) -> Optional[float]:
    """Get the latest price for a ticker via Schwab (or Coinbase for BTC)."""
    if ticker == "BTC":
        try:
            df = _fetch_ohlc_coinbase("5m")
            if df is not None and not df.empty:
                return float(df["Close"].iloc[-1])
        except Exception:
            pass
        return None
    try:
        from .schwab_fetcher import is_schwab_available, fetch_ohlc_schwab
        if not is_schwab_available():
            return None
        df = fetch_ohlc_schwab(ticker, "5m")
        if df is not None and not df.empty:
            return float(df["Close"].iloc[-1])
    except Exception:
        pass
    return None


def classify_time_window(dt: Optional[datetime] = None) -> Optional[str]:
    """
    Classify a datetime into a market time window.
    Returns 'open', 'midday', 'close', or None (outside market hours).
    - open: 9:30 AM - 10:30 AM ET
    - midday: 11:30 AM - 1:00 PM ET
    - close: 3:00 PM - 4:00 PM ET (institutional hour)
    """
    if dt is None:
        dt = datetime.now(timezone.utc)
    et = _to_eastern(dt)
    if et is None or et.weekday() >= 5:
        return None
    h, m = et.hour, et.minute
    t = h * 60 + m  # minutes since midnight
    if 570 <= t < 630:      # 9:30 - 10:30
        return "open"
    elif 690 <= t < 780:    # 11:30 - 13:00
        return "midday"
    elif 900 <= t < 960:    # 15:00 - 16:00
        return "close"
    return None


def current_time_window() -> Optional[str]:
    """Return the current time window name, or None if outside all windows."""
    return classify_time_window(datetime.now(timezone.utc))


def _to_eastern(dt: datetime) -> Optional[datetime]:
    """Convert a datetime to US/Eastern."""
    import zoneinfo
    try:
        return dt.astimezone(zoneinfo.ZoneInfo("America/New_York"))
    except Exception:
        from datetime import timedelta
        return dt - timedelta(hours=4)


def is_market_hours(dt: Optional[datetime] = None) -> bool:
    """Check if a given time falls within institutional hours (9:30-16:00 ET)."""
    if dt is None:
        dt = datetime.now(timezone.utc)
    # Convert to Eastern (UTC-5 standard, UTC-4 DST — approximate)
    import zoneinfo
    try:
        et = dt.astimezone(zoneinfo.ZoneInfo("America/New_York"))
    except Exception:
        # Fallback: assume UTC-4 during market season
        from datetime import timedelta
        et = dt - timedelta(hours=4)
    hour, minute = et.hour, et.minute
    market_open = (hour == 9 and minute >= 30) or hour >= 10
    market_close = hour < 16
    weekday = et.weekday() < 5  # Mon-Fri
    return market_open and market_close and weekday
