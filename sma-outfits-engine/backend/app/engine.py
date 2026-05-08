"""
SMA computation engine and OHLC hit detection.
Core algorithm: for each candle in the last 999, check if O/H/L/C
precisely matches (exact penny) any rolling SMA value at that candle.
"""

import logging
import math
from dataclasses import dataclass, field
from datetime import datetime, timezone

import numpy as np
import pandas as pd

from .config import (
    OUTFITS,
    INSTITUTIONAL_HOURS_MULTIPLIER,
    TIMEFRAME_SCALE,
    is_affinity,
    position_weights,
    outfits_for_ticker,
)
from .fetcher import fetch_ohlc, is_market_hours
from typing import Optional, List, Dict, Set, Union

logger = logging.getLogger(__name__)

# Maximum candles to look back for hit accumulation
HIT_LOOKBACK = 999


@dataclass
class Hit:
    """A single OHLC-to-SMA hit."""
    outfit: str
    ticker: str
    timeframe: str
    sma_period: int
    ohlc_component: str   # "open", "high", "low", "close"
    price: float
    sma_value: float
    delta: float
    side: str             # "long" or "short"
    weight: float
    timestamp: str


@dataclass
class ScanResult:
    """Result of a full scan across all EOT combinations."""
    hits: list[Hit] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    tickers_scanned: int = 0
    combos_checked: int = 0
    scan_time: str = ""


def compute_sma(series: pd.Series, period: int) -> pd.Series:
    """Compute Simple Moving Average for a given period."""
    if len(series) < period:
        return pd.Series(dtype=float)
    return series.rolling(window=period, min_periods=period).mean()


def detect_hits_for_ticker(
    ticker: str,
    timeframe: str,
    ohlc_df: pd.DataFrame,
    outfits: Optional[dict] = None,
) -> List[Hit]:
    """
    Detect all OHLC-to-SMA hits for one ticker on one timeframe.

    Checks the last 999 candles (or all available). For each candle,
    computes rolling SMA values as of that candle's position and checks
    if any OHLC component exactly matches (penny-level) the SMA value.
    """
    if outfits is None:
        outfits = OUTFITS

    if ohlc_df is None or len(ohlc_df) < 2:
        return []

    # Filter outfits to only those known to operate on this ticker.
    # If the ticker has defined affinities, only scan those + system outfits.
    # If no affinities are defined (unknown ticker), scan all outfits.
    allowed = outfits_for_ticker(ticker)
    if allowed is not None:
        outfits = {k: v for k, v in outfits.items() if k in allowed}

    # Filter outfits to only those that apply on this timeframe.
    # An outfit with a "timeframes" key only fires on its declared list
    # (e.g. Russia Pres 2000 arbitrage fires only on 1m/3m/5m/15m).
    # Outfits without a "timeframes" key fire on all timeframes (default).
    outfits = {
        k: v for k, v in outfits.items()
        if "timeframes" not in v or timeframe in v["timeframes"]
    }

    hits = []
    n = len(ohlc_df)
    lookback = min(n, HIT_LOOKBACK)
    start_idx = n - lookback  # index into ohlc_df where we begin checking

    close_series = ohlc_df["Close"]

    # Round OHLC columns to 2 decimal places for exact penny matching
    open_rounded = ohlc_df["Open"].round(2)
    high_rounded = ohlc_df["High"].round(2)
    low_rounded = ohlc_df["Low"].round(2)
    close_rounded = ohlc_df["Close"].round(2)

    # Determine institutional hours for each candle in the lookback window
    inst_hours_flags = []
    for i in range(start_idx, n):
        try:
            ts = ohlc_df.index[i]
            if hasattr(ts, "to_pydatetime"):
                ts = ts.to_pydatetime()
            if ts.tzinfo is None:
                ts = ts.replace(tzinfo=timezone.utc)
            inst_hours_flags.append(is_market_hours(ts))
        except Exception:
            inst_hours_flags.append(False)

    timestamps = [str(ohlc_df.index[i]) for i in range(start_idx, n)]

    for outfit_name, outfit_cfg in outfits.items():
        periods = outfit_cfg["periods"]
        pos_weights_list = position_weights(outfit_name)
        affinity_mult = 2.0 if is_affinity(outfit_name, ticker) else 1.0

        for idx, period in enumerate(periods):
            if len(close_series) < period:
                continue

            # Compute rolling SMA for this period across ALL candles
            sma_series = close_series.rolling(window=period, min_periods=period).mean()
            # Round to 2 decimal places for exact penny matching
            sma_rounded = sma_series.round(2)

            pos_w = pos_weights_list[idx] if idx < len(pos_weights_list) else 1.0

            # Check each candle in the lookback window
            for j in range(lookback):
                bar_idx = start_idx + j
                sma_val = sma_rounded.iloc[bar_idx]

                if pd.isna(sma_val) or sma_val == 0:
                    continue

                hours_mult = INSTITUTIONAL_HOURS_MULTIPLIER if inst_hours_flags[j] else 1.0
                # Period magnitude scaling: large-period SMAs are rarer and more
                # significant. log2(period)/6.5 normalizes so MA100≈1.0, MA818≈1.5,
                # MA9≈0.5. This prevents short-period outfits (e.g. REPEATER_9
                # with MA54 max) from drowning out institutional signals on MA400+.
                period_scale = math.log2(max(period, 2)) / 6.5
                # Timeframe scaling: normalizes hit value across timeframes so
                # that fast-TF hits (e.g. 1m) don't drown out slow-TF hits purely
                # from sample-size. A 1m MA16 touch is ~15x more frequent than a
                # 15m MA16 touch for the same SMA period. Baseline 30m = 1.0.
                tf_scale = TIMEFRAME_SCALE.get(timeframe, 1.0)
                weight = pos_w * affinity_mult * hours_mult * period_scale * tf_scale
                ts_str = timestamps[j]

                # Check each OHLC component for exact penny match
                # Only count ONE hit per candle per SMA (dedup across OHLC components)
                ohlc_vals = [
                    ("open", open_rounded.iloc[bar_idx]),
                    ("high", high_rounded.iloc[bar_idx]),
                    ("low", low_rounded.iloc[bar_idx]),
                    ("close", close_rounded.iloc[bar_idx]),
                ]

                matched_comp = None
                matched_val = None
                for comp_name, comp_val in ohlc_vals:
                    if pd.isna(comp_val) or comp_val == 0:
                        continue
                    if comp_val == sma_val:
                        matched_comp = comp_name
                        matched_val = comp_val
                        break  # one hit per candle per SMA — take first match

                if matched_comp is not None:
                    delta = float(ohlc_df.iloc[bar_idx][matched_comp.capitalize()] - sma_series.iloc[bar_idx])
                    # Determine side by close position relative to SMA
                    bar_close = close_rounded.iloc[bar_idx]
                    side = "long" if bar_close >= sma_val else "short"

                    hits.append(Hit(
                        outfit=outfit_name,
                        ticker=ticker,
                        timeframe=timeframe,
                        sma_period=period,
                        ohlc_component=matched_comp,
                        price=float(matched_val),
                        sma_value=float(sma_val),
                        delta=round(delta, 4),
                        side=side,
                        weight=round(weight, 2),
                        timestamp=ts_str,
                    ))

    return hits


def _dedup_hits_by_date(hits: list[Hit]) -> List[Hit]:
    """
    Deduplicate hits across timeframes for the same calendar date.

    The same price event (e.g., NVDA touching MA256 at $120.50) appears on
    the 5m, 15m, 30m, and 1h charts simultaneously. Per Raul's "time index
    hash map" design, each (ticker, outfit, sma_period, date) combination
    counts as at most ONE hit — the one with the highest weight.
    """
    best: dict[tuple, Hit] = {}
    for hit in hits:
        # Extract date from timestamp (handles both "2026-03-20 10:30:00-04:00"
        # and ISO format strings)
        date_str = hit.timestamp[:10]
        key = (hit.ticker, hit.outfit, hit.sma_period, date_str)
        if key not in best or hit.weight > best[key].weight:
            best[key] = hit
    return list(best.values())


def run_scan(
    tickers: list[str],
    timeframes: list[str],
    outfits: Optional[dict] = None,
    progress_callback=None,
) -> ScanResult:
    """
    Run a full scan across all ticker x timeframe x outfit combinations.
    This is the main entry point for the detection engine.
    """
    if outfits is None:
        outfits = OUTFITS

    result = ScanResult(scan_time=datetime.now(timezone.utc).isoformat())
    total = len(tickers) * len(timeframes)
    done = 0

    for ticker in tickers:
        ticker_had_data = False
        ticker_hits: list[Hit] = []

        for tf in timeframes:
            done += 1
            if progress_callback:
                progress_callback(done, total, ticker, tf)

            try:
                ohlc_df = fetch_ohlc(ticker, tf)
            except Exception as e:
                result.errors.append(f"{ticker}@{tf}: {e}")
                continue

            if ohlc_df is None or ohlc_df.empty:
                continue

            ticker_had_data = True
            result.combos_checked += len(outfits)

            hits = detect_hits_for_ticker(ticker, tf, ohlc_df, outfits)
            ticker_hits.extend(hits)

        if ticker_had_data:
            result.tickers_scanned += 1
            # Deduplicate across timeframes: one hit per (outfit, sma, date)
            deduped = _dedup_hits_by_date(ticker_hits)
            result.hits.extend(deduped)

    return result
