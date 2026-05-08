"""
Schwab API data fetcher — primary data source for real-time OHLC candles.
Uses OAuth2 with automatic token refresh. Falls back to yfinance on failure.

Schwab API supported minute frequencies: 1, 5, 10, 15, 30
For unsupported intervals (3m, 20m, 2h, 4h), we resample from smaller candles.

Token lifecycle:
    - Access token: 30 minutes
    - Refresh token: 7 days (must re-authenticate via browser after expiry)
"""

import base64
import json
import logging
import os
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlencode, unquote

import pandas as pd
from pandas import DataFrame
import requests
from typing import Optional, List, Dict, Set, Union

logger = logging.getLogger(__name__)

# ── Configuration ────────────────────────────────────────────────────────────

_BASE_URL = "https://api.schwabapi.com"
_AUTH_URL = "https://api.schwabapi.com/v1/oauth/authorize"
_TOKEN_URL = "https://api.schwabapi.com/v1/oauth/token"
_PRICE_HISTORY_URL = _BASE_URL + "/marketdata/v1/pricehistory"

_APP_KEY = os.environ.get("SCHWAB_APP_KEY", "")
_APP_SECRET = os.environ.get("SCHWAB_APP_SECRET", "")
_CALLBACK_URL = os.environ.get("SCHWAB_CALLBACK_URL", "https://127.0.0.1:8080/callback")

# Token file stored at workspace root (4 levels up from this file)
_TOKEN_PATH = Path(__file__).resolve().parent.parent.parent.parent / ".schwab_token.json"

# Rate limiting: 120 requests per minute
_REQUEST_TIMESTAMPS: list[float] = []
_RATE_LIMIT = 120
_RATE_WINDOW = 60  # seconds


# ── Schwab-specific timeframe mapping ────────────────────────────────────────

SCHWAB_TIMEFRAMES: dict[str, dict] = {
    "1m": {"frequency": 1, "frequencyType": "minute", "periodType": "day", "period": 10, "resample_from": None, "resample_factor": 1},
    "3m": {"frequency": 1, "frequencyType": "minute", "periodType": "day", "period": 10, "resample_from": "1m", "resample_factor": 3},
    "5m": {"frequency": 5, "frequencyType": "minute", "periodType": "day", "period": 10, "resample_from": None, "resample_factor": 1},
    "10m": {"frequency": 10, "frequencyType": "minute", "periodType": "day", "period": 10, "resample_from": None, "resample_factor": 1},
    "15m": {"frequency": 15, "frequencyType": "minute", "periodType": "day", "period": 10, "resample_from": None, "resample_factor": 1},
    "20m": {"frequency": 5, "frequencyType": "minute", "periodType": "day", "period": 10, "resample_from": "5m", "resample_factor": 4},
    "30m": {"frequency": 30, "frequencyType": "minute", "periodType": "day", "period": 10, "resample_from": None, "resample_factor": 1},
    "1h": {"frequency": 30, "frequencyType": "minute", "periodType": "day", "period": 10, "resample_from": "30m", "resample_factor": 2},
    "2h": {"frequency": 30, "frequencyType": "minute", "periodType": "day", "period": 10, "resample_from": "30m", "resample_factor": 4},
    "4h": {"frequency": 30, "frequencyType": "minute", "periodType": "day", "period": 10, "resample_from": "30m", "resample_factor": 8},
    "1D": {"frequency": 1, "frequencyType": "daily", "periodType": "year", "period": 20, "resample_from": None, "resample_factor": 1},
    "1W": {"frequency": 1, "frequencyType": "weekly", "periodType": "year", "period": 20, "resample_from": None, "resample_factor": 1},
}


# ── Token Management ─────────────────────────────────────────────────────────

def _load_token() -> Optional[dict]:
    """Load saved token from disk."""
    if _TOKEN_PATH.exists():
        try:
            with open(_TOKEN_PATH) as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            logger.warning("Failed to read token file, will need re-auth")
            return None


def _save_token(token: dict):
    """Persist token to disk."""
    token["saved_at"] = time.time()
    with open(_TOKEN_PATH, "w") as f:
        json.dump(token, f, indent=2)
    logger.info("Token saved to %s", _TOKEN_PATH)


def _is_token_expired(token: dict) -> bool:
    """Check if the access token is expired (30-minute lifetime)."""
    saved_at = token.get("saved_at", 0)
    expires_in = token.get("expires_in", 1800)  # default 30 min
    return time.time() > saved_at + expires_in - 60  # refresh 1 min early


def _is_refresh_token_expired(token: dict) -> bool:
    """Check if the refresh token is expired (7-day lifetime)."""
    saved_at = token.get("saved_at", 0)
    # Schwab refresh tokens expire after 7 days
    return time.time() > saved_at + (7 * 24 * 3600) - 3600  # 1 hr buffer


def _get_basic_auth() -> str:
    """Generate Basic auth header from app key and secret."""
    credentials = f"{_APP_KEY}:{_APP_SECRET}"
    encoded = base64.b64encode(credentials.encode()).decode()
    return f"Basic {encoded}"


def _refresh_access_token(token: dict) -> Optional[dict]:
    """Use refresh token to get a new access token."""
    refresh_token = token.get("refresh_token")
    if not refresh_token:
        logger.error("No refresh token available")
        return None

    try:
        resp = requests.post(
            _TOKEN_URL,
            headers={
                "Authorization": _get_basic_auth(),
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
            },
            timeout=30,
        )
        resp.raise_for_status()
        new_token = resp.json()
        # Preserve refresh_token if not returned in response
        if "refresh_token" not in new_token:
            new_token["refresh_token"] = refresh_token
        _save_token(new_token)
        logger.info("Access token refreshed successfully")
        return new_token
    except Exception:
        logger.exception("Failed to refresh access token")
        return None


def get_access_token() -> Optional[str]:
    """
    Get a valid access token. Refreshes automatically if expired.
    Returns None if no token available (needs initial auth).
    """
    token = _load_token()
    if token is None:
        logger.warning("No Schwab token found. Run initial auth flow first.")
        return None

    if _is_refresh_token_expired(token):
        logger.error("Schwab refresh token expired (>7 days). Re-authenticate via browser.")
        return None

    if _is_token_expired(token):
        token = _refresh_access_token(token)
        if token is None:
            return None

    return token.get("access_token")


def get_auth_url() -> str:
    """Generate the OAuth2 authorization URL for browser-based login."""
    params = {
        "response_type": "code",
        "client_id": _APP_KEY,
        "redirect_uri": _CALLBACK_URL,
    }
    return f"{_AUTH_URL}?{urlencode(params)}"


def complete_auth(auth_code: str) -> Optional[dict]:
    """
    Exchange authorization code for access + refresh tokens.
    Called after user completes browser login and gets redirected to callback URL.
    """
    # URL-decode the auth code if it came from a browser redirect
    auth_code = unquote(auth_code)

    logger.info("Exchanging auth code for tokens...")
    logger.info(" Token URL: %s", _TOKEN_URL)
    logger.info(" Callback URL: %s", _CALLBACK_URL)
    logger.info(" App Key (first 8): %s...", _APP_KEY[:8] if _APP_KEY else "MISSING")
    logger.info(" Code (first 20): %s...", auth_code[:20] if auth_code else "MISSING")

    try:
        resp = requests.post(
            _TOKEN_URL,
            headers={
                "Authorization": _get_basic_auth(),
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data={
                "grant_type": "authorization_code",
                "code": auth_code,
                "redirect_uri": _CALLBACK_URL,
            },
            timeout=30,
        )

        if resp.status_code != 200:
            logger.error(
                "Schwab token exchange failed: HTTP %d — %s",
                resp.status_code, resp.text,
            )
            logger.error(
                "Common causes: (1) App Key/Secret have l/I or O/0 character errors, "
                "(2) Callback URL in .env doesn't exactly match Schwab portal, "
                "(3) Auth code expired or was already used"
            )
            return None

        token = resp.json()
        _save_token(token)
        logger.info("Initial authentication successful!")
        return token
    except Exception as e:
        logger.exception("Failed to complete initial auth: %s", str(e))
        return None


# ── Rate Limiting ────────────────────────────────────────────────────────────

def _rate_limit():
    """Enforce 120 requests/minute rate limit."""
    now = time.time()
    # Remove timestamps older than the window
    while _REQUEST_TIMESTAMPS and _REQUEST_TIMESTAMPS[0] < now - _RATE_WINDOW:
        _REQUEST_TIMESTAMPS.pop(0)

    if len(_REQUEST_TIMESTAMPS) >= _RATE_LIMIT:
        sleep_time = _REQUEST_TIMESTAMPS[0] + _RATE_WINDOW - now + 0.1
        if sleep_time > 0:
            logger.info("Rate limit hit, sleeping %.1fs", sleep_time)
            time.sleep(sleep_time)

    _REQUEST_TIMESTAMPS.append(time.time())


# ── Price History Fetching ───────────────────────────────────────────────────

def _fetch_candles_raw(
    symbol: str,
    frequency: int,
    frequency_type: str,
    period_type: str,
    period: int,
) -> Optional[List[dict]]:
    """
    Fetch raw candle data from Schwab API.
    Returns list of candle dicts with keys: open, high, low, close, volume, datetime
    """
    access_token = get_access_token()
    if access_token is None:
        return None

    _rate_limit()

    params = {
        "symbol": symbol,
        "periodType": period_type,
        "period": period,
        "frequencyType": frequency_type,
        "frequency": frequency,
        "needExtendedHoursData": "false",
    }

    try:
        resp = requests.get(
            _PRICE_HISTORY_URL,
            headers={"Authorization": f"Bearer {access_token}"},
            params=params,
            timeout=30,
        )

        if resp.status_code == 401:
            # Token might have just expired, try refreshing
            token = _load_token()
            if token:
                token = _refresh_access_token(token)
                if token:
                    resp = requests.get(
                        _PRICE_HISTORY_URL,
                        headers={"Authorization": f"Bearer {token['access_token']}"},
                        params=params,
                        timeout=30,
                    )

        resp.raise_for_status()
        data = resp.json()
        candles = data.get("candles", [])

        if not candles:
            logger.warning("No candles returned for %s", symbol)
            return None

        return candles

    except requests.exceptions.HTTPError as e:
        logger.warning("Schwab API error for %s: %s", symbol, e)
        return None
    except Exception:
        logger.exception("Failed to fetch candles for %s from Schwab", symbol)
        return None


def _candles_to_dataframe(candles: list[dict]) -> pd.DataFrame:
    """Convert Schwab candle list to pandas DataFrame matching yfinance format."""
    records = []
    for c in candles:
        # Schwab datetime is epoch milliseconds
        ts = pd.Timestamp(c["datetime"], unit="ms", tz="UTC")
        records.append({
            "Open": c["open"],
            "High": c["high"],
            "Low": c["low"],
            "Close": c["close"],
            "Volume": c.get("volume", 0),
            "_ts": ts,
        })

    df = pd.DataFrame(records)
    if df.empty:
        return df

    df = df.set_index("_ts")
    df.index.name = "Datetime"
    return df


def _resample_ohlc(df: pd.DataFrame, factor: int) -> pd.DataFrame:
    """Resample OHLC data by combining `factor` consecutive candles."""
    if df.empty or factor <= 1:
        return df

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

    resampled.index = grouped.apply(lambda g: g.index[0])
    resampled.index.name = df.index.name

    return resampled


def fetch_ohlc_schwab(ticker: str, timeframe: str) -> Optional[DataFrame]:
    """
    Fetch OHLC data from Schwab API for a given ticker and timeframe.
    Handles resampling for unsupported intervals.
    Returns DataFrame with columns: Open, High, Low, Close, Volume
    Returns None on failure.
    """
    tf_cfg = SCHWAB_TIMEFRAMES.get(timeframe)
    if tf_cfg is None:
        logger.warning("Unknown timeframe for Schwab: %s", timeframe)
        return None

    # Fetch the base candle data
    candles = _fetch_candles_raw(
        symbol=ticker,
        frequency=tf_cfg["frequency"],
        frequency_type=tf_cfg["frequencyType"],
        period_type=tf_cfg["periodType"],
        period=tf_cfg["period"],
    )

    if candles is None:
        return None

    df = _candles_to_dataframe(candles)
    if df.empty:
        return None

    # Resample if needed
    if tf_cfg["resample_from"] is not None:
        df = _resample_ohlc(df, tf_cfg["resample_factor"])

    return df


# ── Auth Status & Endpoints ──────────────────────────────────────────────────

def is_authenticated() -> bool:
    """Check if we have a valid (non-expired) Schwab token."""
    token = _load_token()
    if token is None:
        return False
    if _is_refresh_token_expired(token):
        return False
    return True


def auth_status() -> dict:
    """Return detailed auth status for the API."""
    token = _load_token()
    if token is None:
        return {
            "authenticated": False,
            "reason": "no_token",
            "auth_url": get_auth_url(),
            "instructions": "Visit the auth_url in a browser, log in to Schwab, "
            "then POST the callback code to /api/schwab/callback",
        }

    if _is_refresh_token_expired(token):
        return {
            "authenticated": False,
            "reason": "refresh_expired",
            "auth_url": get_auth_url(),
            "instructions": "Refresh token expired (>7 days). Re-authenticate via browser.",
        }

    if _is_token_expired(token):
        # Try auto-refresh
        new_token = _refresh_access_token(token)
        if new_token is None:
            return {
                "authenticated": False,
                "reason": "refresh_failed",
                "auth_url": get_auth_url(),
            }
        return {"authenticated": True, "reason": "token_refreshed"}

    saved_at = token.get("saved_at", 0)
    expires_in = token.get("expires_in", 1800)
    remaining = max(0, saved_at + expires_in - time.time())

    return {
        "authenticated": True,
        "access_token_expires_in": int(remaining),
        "refresh_token_expires_in": int(max(0, saved_at + 7 * 86400 - time.time())),
    }


def is_schwab_available() -> bool:
    """Check if Schwab API is configured and authenticated."""
    if not _APP_KEY or not _APP_SECRET:
        return False
    return is_authenticated()
