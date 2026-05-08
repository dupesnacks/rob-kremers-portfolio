"""
Major signal detection — flags exceptional SMA activity that suggests
big institutional positioning, the kind of thing Raul enters trades on.

IMPORTANT: Only analyzes RECENT hits (last 5 trading days) to detect
current positioning. Historical hits across 6 months create noise —
every ticker touches short SMAs hundreds of times. We want to surface
what's happening NOW.

Alert types (from highest to lowest conviction):
1. AFFINITY_LOCK: Ticker's primary-affinity outfit fires RECENTLY on MA400+
2. CONFLUENCE: 10+ outfits firing on same ticker in recent days
3. HIGH_PERIOD_CLUSTER: 5+ recent MA400+ hits on one ticker
4. OUTFIT_SURGE: One outfit active across 15+ tickers recently
5. MAGNETIZED_HIGH: Consecutive-session hit on MA400+ (persistent magnet)
"""

import logging
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from .config import OUTFITS, is_affinity
from .engine import Hit, ScanResult
from typing import Optional, List, Dict, Set, Union

logger = logging.getLogger(__name__)

# ── Thresholds (tuned for 27 outfits, 26 tickers, 6mo history) ──────────
# Only recent hits matter for alerts — filter to last N trading days
RECENT_DAYS = 5

# CONFLUENCE: many outfits on one ticker recently
MIN_OUTFITS_FOR_CONFLUENCE = 10      # 10+ of 24 core outfits = exceptional
CONFLUENCE_CRITICAL_OUTFITS = 15     # 15+ = critical

# HIGH_PERIOD_CLUSTER: many large-period hits on one ticker recently
MIN_HIGH_PERIOD = 400                # MA400+ = institutional-grade
MIN_HIGH_PERIOD_HITS = 5             # 5+ distinct MA400+ hits
HIGH_PERIOD_CRITICAL_HITS = 8        # 8+ = critical

# OUTFIT_SURGE: one outfit across many tickers
MIN_TICKERS_FOR_SURGE = 15           # 15+ of 26 tickers = broad institutional move
SURGE_CRITICAL_TICKERS = 20          # 20+ = critical

# AFFINITY_LOCK: primary-affinity outfit on large SMA (highest conviction)
AFFINITY_LOCK_MIN_PERIOD = 400       # MA400+ on affinity ticker
AFFINITY_LOCK_CRITICAL_PERIOD = 700  # MA700+ = critical

# MAGNETIZED_HIGH: consecutive sessions on large SMA
MAGNETIZED_MIN_PERIOD = 400          # MA400+ (was 200, too noisy)
MAGNETIZED_CRITICAL_SESSIONS = 4     # 4+ sessions = critical
MAGNETIZED_CRITICAL_PERIOD = 700     # or MA700+ = critical


@dataclass
class Alert:
    level: str          # "critical", "high"
    alert_type: str     # CONFLUENCE, HIGH_PERIOD_CLUSTER, etc.
    ticker: str
    outfit: str
    summary: str
    details: dict


def _is_recent(hit: Hit, cutoff_date: str) -> bool:
    """Check if a hit's timestamp is within the recent window."""
    try:
        hit_date = hit.timestamp[:10]
        return hit_date >= cutoff_date
    except Exception:
        return False


def _recent_cutoff() -> str:
    """Get the date string for RECENT_DAYS ago."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=RECENT_DAYS)
    return cutoff.strftime("%Y-%m-%d")


def detect_alerts(result: ScanResult, active_programs: Optional[List[dict]] = None) -> List[dict]:
    """
    Analyze scan results for major signals. Only considers recent hits
    (last 5 trading days) to filter out historical noise.
    Returns list of alert dicts sorted by severity (critical first).
    """
    alerts: list[Alert] = []
    cutoff = _recent_cutoff()

    # Filter to recent hits only
    recent_hits = [h for h in result.hits if _is_recent(h, cutoff)]

    if not recent_hits:
        return []

    # Index recent hits by ticker and by outfit
    hits_by_ticker: dict[str, list[Hit]] = defaultdict(list)
    hits_by_outfit: dict[str, list[Hit]] = defaultdict(list)

    for hit in recent_hits:
        hits_by_ticker[hit.ticker].append(hit)
        hits_by_outfit[hit.outfit].append(hit)

    # ── 1. AFFINITY_LOCK (highest conviction) ────────────────────────────
    # Ticker's "home" outfit fires on MA400+ recently. This is exactly
    # what Raul trades — e.g., TSLL hitting TSLA(420) at MA420.
    for ticker, hits in hits_by_ticker.items():
        best_affinity_hit = None
        for hit in hits:
            if hit.sma_period >= AFFINITY_LOCK_MIN_PERIOD and is_affinity(hit.outfit, ticker):
                if best_affinity_hit is None or hit.sma_period > best_affinity_hit.sma_period:
                    best_affinity_hit = hit
        if best_affinity_hit:
            h = best_affinity_hit
            level = "critical" if h.sma_period >= AFFINITY_LOCK_CRITICAL_PERIOD else "high"
            alerts.append(Alert(
                level=level,
                alert_type="AFFINITY_LOCK",
                ticker=ticker,
                outfit=h.outfit,
                summary=f"{ticker}: {h.outfit} MA{h.sma_period} @ ${h.price:.2f} on {h.timeframe}",
                details={
                    "sma_period": h.sma_period,
                    "timeframe": h.timeframe,
                    "price": h.price,
                    "sma_value": h.sma_value,
                    "side": h.side,
                    "weight": h.weight,
                    "timestamp": h.timestamp,
                },
            ))

    # ── 2. CONFLUENCE — many outfits on one ticker recently ──────────────
    for ticker, hits in hits_by_ticker.items():
        outfits_firing = set(h.outfit for h in hits)
        core_outfits = {o for o in outfits_firing if OUTFITS.get(o, {}).get("category") != "System"}
        if len(core_outfits) >= MIN_OUTFITS_FOR_CONFLUENCE:
            high_period_count = sum(1 for h in hits if h.sma_period >= MIN_HIGH_PERIOD)
            level = "critical" if len(core_outfits) >= CONFLUENCE_CRITICAL_OUTFITS else "high"
            best_hit = max(hits, key=lambda h: h.weight)
            alerts.append(Alert(
                level=level,
                alert_type="CONFLUENCE",
                ticker=ticker,
                outfit=f"{len(core_outfits)} outfits",
                summary=f"{ticker}: {len(core_outfits)} outfits converging, {high_period_count} MA400+ hits",
                details={
                    "outfits": sorted(core_outfits),
                    "outfit_count": len(core_outfits),
                    "high_period_hits": high_period_count,
                    "top_sma": f"MA{best_hit.sma_period}",
                    "top_timeframe": best_hit.timeframe,
                },
            ))

    # ── 3. HIGH_PERIOD_CLUSTER — many MA400+ hits on one ticker ──────────
    for ticker, hits in hits_by_ticker.items():
        high_hits = [h for h in hits if h.sma_period >= MIN_HIGH_PERIOD]
        if len(high_hits) >= MIN_HIGH_PERIOD_HITS:
            unique_periods = sorted(set(h.sma_period for h in high_hits), reverse=True)
            max_period = unique_periods[0]
            level = "critical" if len(high_hits) >= HIGH_PERIOD_CRITICAL_HITS else "high"
            outfits_involved = sorted(set(h.outfit for h in high_hits))
            alerts.append(Alert(
                level=level,
                alert_type="HIGH_PERIOD_CLUSTER",
                ticker=ticker,
                outfit=outfits_involved[0] if outfits_involved else "",
                summary=f"{ticker}: {len(high_hits)} MA400+ hits across {', '.join(f'MA{p}' for p in unique_periods[:4])}",
                details={
                    "hit_count": len(high_hits),
                    "periods": unique_periods[:8],
                    "max_period": max_period,
                    "outfits": outfits_involved,
                },
            ))

    # ── 4. OUTFIT_SURGE — one outfit across many tickers ─────────────────
    for outfit, hits in hits_by_outfit.items():
        if OUTFITS.get(outfit, {}).get("category") == "System":
            continue
        tickers_hit = set(h.ticker for h in hits)
        if len(tickers_hit) >= MIN_TICKERS_FOR_SURGE:
            high_hits = [h for h in hits if h.sma_period >= MIN_HIGH_PERIOD]
            level = "critical" if len(tickers_hit) >= SURGE_CRITICAL_TICKERS else "high"
            alerts.append(Alert(
                level=level,
                alert_type="OUTFIT_SURGE",
                ticker="BROAD",
                outfit=outfit,
                summary=f"{outfit}: {len(tickers_hit)} tickers ({len(high_hits)} with MA400+ hits)",
                details={
                    "tickers": sorted(tickers_hit),
                    "ticker_count": len(tickers_hit),
                    "high_period_hits": len(high_hits),
                },
            ))

    # ── 5. MAGNETIZED_HIGH — consecutive sessions on MA400+ ──────────────
    if active_programs:
        for prog in active_programs:
            if (prog.get("is_magnetized") and
                prog.get("sma_period", 0) >= MAGNETIZED_MIN_PERIOD and
                prog.get("status") == "active"):
                consec = prog.get("consecutive_sessions", 0)
                period = prog["sma_period"]
                level = ("critical" if period >= MAGNETIZED_CRITICAL_PERIOD
                         or consec >= MAGNETIZED_CRITICAL_SESSIONS else "high")
                alerts.append(Alert(
                    level=level,
                    alert_type="MAGNETIZED_HIGH",
                    ticker=prog.get("ticker", ""),
                    outfit=prog.get("outfit_key", ""),
                    summary=(f"{prog.get('ticker')}: magnetized {consec} sessions "
                             f"on MA{period} ({prog.get('outfit_key')})"),
                    details={
                        "sma_period": period,
                        "timeframe": prog.get("timeframe", ""),
                        "consecutive_sessions": consec,
                        "entry_price": prog.get("entry_price"),
                        "sma_value": prog.get("sma_value"),
                        "protocol": prog.get("protocol"),
                    },
                ))

    # Deduplicate AFFINITY_LOCK (one per ticker)
    seen = set()
    deduped = []
    for a in alerts:
        key = (a.ticker, a.alert_type)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(a)

    # Sort: critical first, then high; within same level by alert type priority
    type_order = {
        "AFFINITY_LOCK": 0,
        "CONFLUENCE": 1,
        "HIGH_PERIOD_CLUSTER": 2,
        "MAGNETIZED_HIGH": 3,
        "OUTFIT_SURGE": 4,
    }
    level_order = {"critical": 0, "high": 1}
    deduped.sort(key=lambda a: (
        level_order.get(a.level, 9),
        type_order.get(a.alert_type, 9),
        a.ticker,
    ))

    return [
        {
            "level": a.level,
            "type": a.alert_type,
            "ticker": a.ticker,
            "outfit": a.outfit,
            "summary": a.summary,
            "details": a.details,
        }
        for a in deduped
    ]
