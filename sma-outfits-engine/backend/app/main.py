"""
FastAPI application — SMA Outfits Detection Engine.
REST API serving outfit rankings, ticker rankings, signals, and institutional bias.
"""

import asyncio
import json
import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path

# Load .env — try python-dotenv first, fall back to manual loader.
# Ensures credentials load regardless of how uvicorn is started.
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")
except ImportError:
    _env_candidates = [
        Path(__file__).resolve().parent.parent.parent / ".env",
        Path.home() / "clawd" / "sma-outfits-engine" / ".env",
        Path.home() / "clawd" / ".env",
    ]
    for _p in _env_candidates:
        if _p.exists():
            for _line in _p.read_text().splitlines():
                _line = _line.strip()
                if _line and not _line.startswith("#") and "=" in _line:
                    _k, _v = _line.split("=", 1)
                    os.environ.setdefault(_k.strip(), _v.strip())
            break
from datetime import datetime, timezone
from typing import Any, Optional, List, Dict

from fastapi import FastAPI, BackgroundTasks, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse


class PrettyJSONResponse(JSONResponse):
    """JSON response with indentation for browser readability."""
    def render(self, content: Any) -> bytes:
        return json.dumps(content, indent=2, ensure_ascii=False).encode("utf-8")

from .config import (
    OUTFITS,
    TICKERS,
    TICKERS_LIGHT,
    TICKERS_TSLA,
    TIMEFRAMES,
    PRIMARY_TIMEFRAMES,
    SECONDARY_TIMEFRAMES,
)
from .database import (
    init_db, save_scan, load_latest_scan, get_active_programs,
    load_scan_snapshots, load_momentum_data, get_snapshot_dates,
)
from .engine import run_scan, ScanResult
from .fetcher import fetch_latest_price, fetch_ohlc, classify_time_window, current_time_window, get_data_source_stats, reset_data_source_stats
from .alerts import detect_alerts
from .ranking import (
    compute_outfit_ranking,
    compute_ticker_ranking,
    compute_institutional_bias,
    hits_to_signals,
    compute_ticker_detail,
    update_active_programs,
    build_scan_snapshot,
    enrich_rankings_with_momentum,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ── App state ───────────────────────────────────────────────────────────────

scan_in_progress = False
scan_progress = {"done": 0, "total": 0, "ticker": "", "timeframe": ""}
latest_result: Optional[ScanResult] = None
latest_alerts: list[dict] = []


_scheduler_task: Optional[asyncio.Task] = None


async def _scheduled_scan_loop():
    """
    Background loop that triggers scans at institutional time windows.
    Checks every 60 seconds; if we're inside a window that hasn't been
    scanned today, triggers a light scan automatically.
    """
    import zoneinfo
    scanned_windows: dict[str, set[str]] = {}  # {date: {window, ...}}

    while True:
        try:
            await asyncio.sleep(60)  # check every 60 seconds
            now = datetime.now(timezone.utc)
            try:
                et = now.astimezone(zoneinfo.ZoneInfo("America/New_York"))
            except Exception:
                from datetime import timedelta
                et = now - timedelta(hours=4)

            today = et.strftime("%Y-%m-%d")
            window = classify_time_window(now)

            if window is None:
                continue

            logger.debug("Window check: %s at %s ET", window, et.strftime("%H:%M"))

            # Reset scanned windows on new day
            if today not in scanned_windows:
                scanned_windows.clear()
                scanned_windows[today] = set()

            if window in scanned_windows[today]:
                continue

            if scan_in_progress:
                logger.info("Window '%s' detected but scan already in progress, will retry", window)
                continue

            # Auto-trigger a light scan for this window
            logger.info("Auto-scan triggered for window '%s' at %s", window, et.strftime("%H:%M ET"))
            scanned_windows[today].add(window)
            _run_scan_sync("light")

        except asyncio.CancelledError:
            break
        except Exception:
            logger.exception("Scheduled scan loop error")


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _scheduler_task
    init_db()
    logger.info("SMA Engine started. DB initialized.")

    # Start the scheduled scan loop
    auto_scan = os.environ.get("AUTO_SCAN", "true").lower()
    if auto_scan in ("true", "1", "yes"):
        _scheduler_task = asyncio.create_task(_scheduled_scan_loop())
        logger.info("Scheduled auto-scan loop started (open/midday/close windows)")
    else:
        logger.info("Auto-scan disabled (set AUTO_SCAN=true to enable)")

    yield

    # Cleanup
    if _scheduler_task:
        _scheduler_task.cancel()
        try:
            await _scheduler_task
        except asyncio.CancelledError:
            pass


app = FastAPI(
    title="SMA Outfits Detection Engine",
    version="1.0.0",
    lifespan=lifespan,
    default_response_class=PrettyJSONResponse,
)

# CORS — allow all origins (personal tool, not public API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Scan logic ──────────────────────────────────────────────────────────────

def _run_scan_sync(mode: str):
    """Run scan synchronously (called from background task)."""
    global scan_in_progress, scan_progress, latest_result

    if mode == "tsla":
        tickers = TICKERS_TSLA
        timeframes = list(TIMEFRAMES.keys())  # all timeframes for TSLA deep scan
    elif mode == "light":
        tickers = TICKERS_LIGHT
        timeframes = PRIMARY_TIMEFRAMES
    else:
        tickers = TICKERS
        timeframes = list(TIMEFRAMES.keys())

    def progress_cb(done, total, ticker, tf):
        scan_progress.update(done=done, total=total, ticker=ticker, timeframe=tf)

    reset_data_source_stats()
    logger.info("Starting %s scan: %d tickers × %d timeframes", mode, len(tickers), len(timeframes))

    result = run_scan(tickers, timeframes, progress_callback=progress_cb)
    latest_result = result

    # Compute rankings and persist
    bias = compute_institutional_bias(result)
    outfits = compute_outfit_ranking(result, institutional_bias=bias)
    tickers_ranked = compute_ticker_ranking(result, institutional_bias=bias)
    signals = hits_to_signals(result)
    stats = {
        "tickers_scanned": result.tickers_scanned,
        "combos_checked": result.combos_checked,
        "total_hits": len(result.hits),
        "errors": result.errors[:10],
    }

    save_scan(result.scan_time, mode, bias, outfits, tickers_ranked, signals, stats)

    # Save snapshot for current time window (for momentum tracking)
    window = current_time_window()
    if window:
        try:
            build_scan_snapshot(result, window)
            logger.info("Saved scan snapshot for window: %s", window)
        except Exception:
            logger.exception("Failed to save scan snapshot for window: %s", window)

        # Enrich rankings with momentum (needs 2+ windows to compute)
        try:
            session_date = result.scan_time[:10]
            enriched_outfits = enrich_rankings_with_momentum(outfits, session_date)
            enriched_tickers = enrich_rankings_with_momentum(tickers_ranked, session_date)
            # Re-save with momentum data
            save_scan(result.scan_time, mode, bias, enriched_outfits, enriched_tickers, signals, stats)
            logger.info("Enriched rankings with momentum data for %s", session_date)
        except Exception:
            logger.exception("Failed to enrich rankings with momentum")
    else:
        # Outside market windows — still save as 'full' snapshot for reference
        try:
            build_scan_snapshot(result, "full")
            logger.info("Saved full-day scan snapshot (outside market windows)")
        except Exception:
            logger.exception("Failed to save full scan snapshot")

        # Still try momentum enrichment outside windows (uses 'full' snapshots)
        try:
            session_date = result.scan_time[:10]
            enriched_outfits = enrich_rankings_with_momentum(outfits, session_date)
            enriched_tickers = enrich_rankings_with_momentum(tickers_ranked, session_date)
            save_scan(result.scan_time, mode, bias, enriched_outfits, enriched_tickers, signals, stats)
            logger.info("Enriched rankings with momentum data for %s", session_date)
        except Exception:
            logger.exception("Failed to enrich rankings with momentum")

    # Update active programs lifecycle + magnetized detection
    programs = None
    try:
        programs = update_active_programs(result)
        active_count = sum(1 for p in programs if p["status"] == "active")
        mag_count = sum(1 for p in programs if p.get("is_magnetized"))
        logger.info("Active programs: %d active, %d magnetized", active_count, mag_count)
    except Exception:
        logger.exception("Failed to update active programs")

    # Detect major signals / alerts
    global latest_alerts
    try:
        latest_alerts = detect_alerts(result, programs)
        if latest_alerts:
            critical = sum(1 for a in latest_alerts if a["level"] == "critical")
            high = sum(1 for a in latest_alerts if a["level"] == "high")
            logger.info("ALERTS: %d critical, %d high — %d total major signals detected",
                        critical, high, len(latest_alerts))
            for a in latest_alerts[:5]:
                logger.info("  [%s] %s", a["level"].upper(), a["summary"])
    except Exception:
        logger.exception("Failed to detect alerts")
        latest_alerts = []

    ds_stats = get_data_source_stats()
    logger.info(
        "Scan complete: %d hits from %d tickers, %d combos (Schwab: %d, failed: %d)",
        len(result.hits), result.tickers_scanned, result.combos_checked,
        ds_stats["schwab"], ds_stats["failed"],
    )

    if ds_stats["schwab"] == 0 and ds_stats["failed"] > 0:
        logger.error("ALL fetches failed — Schwab API is not authenticated. Go to /api/schwab/auth to reconnect.")

    scan_in_progress = False


# ── API Routes ──────────────────────────────────────────────────────────────

@app.get("/api/health")
async def health():
    return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}


@app.get("/api/data-status")
async def data_status():
    """
    Shows what scan data is available — when last scan ran, what windows
    have been captured today, and whether momentum data exists.
    """
    data = load_latest_scan()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    snapshots_today = load_scan_snapshots(today)
    windows_today = list(set(s["time_window"] for s in snapshots_today))
    momentum_today = load_momentum_data(today)

    return {
        "has_scan_data": data is not None,
        "last_scan_time": data["scan_time"] if data else None,
        "last_scan_mode": data["mode"] if data else None,
        "today": today,
        "windows_captured_today": sorted(windows_today),
        "has_momentum": len(momentum_today) > 0,
        "momentum_outfits": len(momentum_today),
        "snapshot_count_today": len(snapshots_today),
        "auto_scan_enabled": os.environ.get("AUTO_SCAN", "true").lower() in ("true", "1", "yes"),
    }


@app.post("/api/scan")
async def trigger_scan(
    background_tasks: BackgroundTasks,
    mode: str = Query("light", regex="^(light|full|tsla)$"),
):
    """Trigger a new scan. Runs in background."""
    global scan_in_progress, scan_progress

    if scan_in_progress:
        return JSONResponse(
            status_code=409,
            content={"error": "Scan already in progress", "progress": scan_progress},
        )

    scan_in_progress = True
    scan_progress = {"done": 0, "total": 0, "ticker": "", "timeframe": ""}

    background_tasks.add_task(_run_scan_sync, mode)

    return {"status": "started", "mode": mode}


@app.get("/api/scan/status")
async def scan_status():
    """Get current scan progress."""
    return {
        "in_progress": scan_in_progress,
        "progress": scan_progress,
    }


@app.get("/api/bias")
async def get_bias(window: str = Query("full", regex="^(full|institutional|open|midday|close)$")):
    """
    Overall institutional bias summary.
    ?window=institutional|close returns close-window bias with momentum overlay.
    """
    data = load_latest_scan()
    if data is None:
        return {"overall_bias": "Neutral", "systems": {}, "dominant_outfit": "", "session_date": ""}

    bias = data["bias"]

    if window in ("institutional", "close"):
        session_date = bias.get("session_date", "")
        if session_date:
            momentum = load_momentum_data(session_date)
            # Count how many outfits have falling momentum
            falling = sum(1 for m in momentum.values() if m["momentum"] == "Falling")
            rising = sum(1 for m in momentum.values() if m["momentum"] == "Rising")
            total = len(momentum)
            if total > 0:
                bias["momentum_summary"] = {
                    "falling": falling,
                    "rising": rising,
                    "flat": total - falling - rising,
                    "total": total,
                }
                # Override bias if momentum strongly diverges
                if falling > rising and falling > total / 2:
                    bias["institutional_momentum"] = "Bearish"
                elif rising > falling and rising > total / 2:
                    bias["institutional_momentum"] = "Bullish"
                else:
                    bias["institutional_momentum"] = "Mixed"
            else:
                bias["momentum_summary"] = None
                bias["institutional_momentum"] = "No data"

    return bias


@app.get("/api/outfits")
async def get_outfits(window: str = Query("full", regex="^(full|institutional|open|midday|close)$")):
    """
    Outfit ranking table.
    ?window=institutional returns rankings with momentum data from close vs midday comparison.
    ?window=open|midday|close returns snapshot from that specific window.
    """
    data = load_latest_scan()
    if data is None:
        return []

    outfits = data["outfits"]

    if window in ("institutional", "close"):
        session_date = data.get("bias", {}).get("session_date", "")
        if session_date:
            outfits = enrich_rankings_with_momentum(outfits, session_date)
    elif window in ("open", "midday"):
        # Return snapshot data from that window period
        session_date = data.get("bias", {}).get("session_date", "")
        if session_date:
            snapshots = load_scan_snapshots(session_date, window)
            if snapshots:
                # Merge snapshot L/S ratios into the ranking data
                snap_lookup = {s["outfit_key"]: s for s in snapshots if s["ticker"] is None}
                for outfit in outfits:
                    snap = snap_lookup.get(outfit.get("sequence", ""))
                    if snap:
                        outfit["window_ls_ratio"] = snap["ls_ratio"]
                        outfit["window_long"] = snap["long_count"]
                        outfit["window_short"] = snap["short_count"]
                        outfit["window"] = window

    return outfits


@app.get("/api/tickers")
async def get_tickers(window: str = Query("full", regex="^(full|institutional|open|midday|close)$")):
    """Ticker ranking table with optional momentum enrichment."""
    data = load_latest_scan()
    if data is None:
        return []

    tickers = data["tickers"]

    if window in ("institutional", "close"):
        session_date = data.get("bias", {}).get("session_date", "")
        if session_date:
            # Tickers don't have direct snapshots (those are outfit-level),
            # but we pass through the data for frontend enrichment
            momentum = load_momentum_data(session_date)
            for t in tickers:
                dom = t.get("dominant_outfit", "")
                mom = momentum.get(dom)
                if mom:
                    t["outfit_momentum"] = mom["momentum"]
                    t["outfit_momentum_delta"] = mom["delta"]

    return tickers


@app.get("/api/momentum")
async def get_momentum(date: str = Query(None)):
    """
    Momentum data for a given date (defaults to today).
    Returns per-outfit momentum comparing midday vs close L/S ratios.
    """
    if date is None:
        date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    momentum = load_momentum_data(date)
    if not momentum:
        return {"date": date, "status": "no_data", "outfits": {}}
    return {"date": date, "status": "ok", "outfits": momentum}


@app.get("/api/snapshots")
async def get_snapshots(date: str = Query(None), window: str = Query(None)):
    """
    Raw scan snapshots for a given date and optional window filter.
    Useful for debugging and verifying momentum calculations.
    """
    if date is None:
        date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    snapshots = load_scan_snapshots(date, window)
    return {"date": date, "window": window, "count": len(snapshots), "snapshots": snapshots}


@app.get("/api/snapshots/dates")
async def get_snapshot_dates_api():
    """Return all dates with snapshot data and their available windows."""
    return get_snapshot_dates()


@app.get("/api/scan/schedule")
async def get_scan_schedule():
    """Show the auto-scan schedule and current window status."""
    window = current_time_window()
    return {
        "auto_scan_enabled": os.environ.get("AUTO_SCAN", "true").lower() in ("true", "1", "yes"),
        "current_window": window,
        "windows": {
            "open": "9:30 AM - 10:30 AM ET",
            "midday": "11:30 AM - 1:00 PM ET",
            "close": "3:00 PM - 4:00 PM ET (institutional hour)",
        },
        "scan_interval": "Every 60 seconds (checks if window needs scanning)",
    }


@app.get("/api/signals")
async def get_signals(limit: int = Query(50, ge=1, le=200)):
    """Recent signal feed."""
    data = load_latest_scan()
    if data is None:
        return []
    return data["signals"][:limit]


@app.get("/api/ticker/{symbol}")
async def get_ticker_detail(symbol: str):
    """Ticker detail with all signals."""
    global latest_result
    sym = symbol.upper()

    # If we have in-memory scan results, use them for full detail
    if latest_result is not None:
        return compute_ticker_detail(latest_result, sym)

    # Fallback: reconstruct from DB-stored ticker ranking + signals
    data = load_latest_scan()
    if data is None:
        return {"ticker": sym, "total": 0, "long": 0, "short": 0, "signals": []}

    # Find the ticker in stored ranking
    ticker_entry = None
    for t in data.get("tickers", []):
        if t.get("ticker") == sym:
            ticker_entry = t
            break

    # Filter stored signals for this ticker
    ticker_signals = [
        s for s in data.get("signals", [])
        if s.get("ticker") == sym
    ]

    if ticker_entry:
        return {
            "ticker": sym,
            "total": ticker_entry.get("total", 0),
            "long": ticker_entry.get("long", 0),
            "short": ticker_entry.get("short", 0),
            "ls_ratio": ticker_entry.get("ls_ratio", 0),
            "dominant_outfit": ticker_entry.get("dominant_outfit", ""),
            "signals": ticker_signals[:20],
        }

    return {"ticker": sym, "total": 0, "long": 0, "short": 0, "signals": ticker_signals[:20]}


@app.get("/api/vix")
async def get_vix():
    """Current VIX level."""
    try:
        price = fetch_latest_price("VIX")
        if price is not None:
            # Classify VIX regime
            if price < 15:
                regime = "Low"
            elif price < 20:
                regime = "Normal"
            elif price < 30:
                regime = "Elevated"
            else:
                regime = "Extreme"
            return {"vix": round(price, 2), "regime": regime}
    except Exception:
        pass
    return {"vix": None, "regime": "Unknown"}


@app.get("/api/btc")
async def get_btc():
    """
    Bitcoin dedicated panel — always-on BTC analysis via Coinbase.
    Runs outfit detection across timeframes and returns price, bias, and key levels.
    """
    import numpy as np

    price = fetch_latest_price("BTC")

    # Only scan BTC against confirmed/plausible crypto outfits
    # Confirmed by Raul tweets + other builders: AN(33s), SVIX(211)
    # Plausible (pure math, not ticker-specific): Base 2/NVDA, Waring's Problem
    _BTC_ALLOWED_OUTFITS = {
        "AN (33s)",           # confirmed on BTC 30m (MA666, MA999)
        "SVIX (211)",         # confirmed on BTC 30m (MA844)
        "AN (11s)",           # angel number family — plausible
        "AN (22s)",           # angel number family — plausible
        "Base 2/NVDA",        # pure binary math — plausible on any asset
        "Waring's Problem",   # number theory — plausible on any asset
    }

    # Run BTC through the outfit engine across primary timeframes
    btc_timeframes = ["5m", "15m", "30m", "1h", "2h", "4h", "1D"]
    hits = []
    sma_levels = {}  # track key SMA values

    for tf in btc_timeframes:
        df = fetch_ohlc("BTC", tf)
        if df is None or df.empty:
            continue
        close = df["Close"]
        current_price = float(close.iloc[-1])
        if price is None:
            price = current_price

        for outfit_name, outfit_def in OUTFITS.items():
            if outfit_name not in _BTC_ALLOWED_OUTFITS:
                continue
            periods = outfit_def["periods"]
            for idx, period in enumerate(periods):
                if period >= len(close):
                    continue
                sma_val = float(close.rolling(window=period).mean().iloc[-1])
                if np.isnan(sma_val):
                    continue
                delta = current_price - sma_val
                pct = abs(delta / sma_val) * 100

                # Only count as a "hit" if price is within 0.5% of SMA
                if pct <= 0.5:
                    side = "long" if current_price > sma_val else "short"
                    weight = [1.0, 1.5, 2.0, 4.0, 6.0, 8.0][idx] if len(periods) == 6 else [1.0, 3.0, 8.0][idx]
                    hits.append({
                        "outfit": outfit_name,
                        "timeframe": tf,
                        "period": period,
                        "sma_value": round(sma_val, 2),
                        "delta": round(delta, 2),
                        "pct": round(pct, 3),
                        "side": side,
                        "weight": weight,
                        "position": idx,
                    })
                    key = f"MA{period}"
                    if key not in sma_levels or weight > sma_levels[key]["weight"]:
                        sma_levels[key] = {"value": round(sma_val, 2), "weight": weight, "side": side}

    # Compute bias
    long_weight = sum(h["weight"] for h in hits if h["side"] == "long")
    short_weight = sum(h["weight"] for h in hits if h["side"] == "short")
    total_hits = len(hits)

    if total_hits == 0:
        verdict = "Neutral"
        reason = "No SMA outfit signals detected on BTC"
    elif long_weight > short_weight * 1.5:
        verdict = "Bullish"
        reason = f"{sum(1 for h in hits if h['side'] == 'long')} long signals ({long_weight:.1f}w) vs {sum(1 for h in hits if h['side'] == 'short')} short ({short_weight:.1f}w)"
    elif short_weight > long_weight * 1.5:
        verdict = "Bearish"
        reason = f"{sum(1 for h in hits if h['side'] == 'short')} short signals ({short_weight:.1f}w) vs {sum(1 for h in hits if h['side'] == 'long')} long ({long_weight:.1f}w)"
    else:
        verdict = "Neutral"
        reason = f"Mixed signals — {long_weight:.1f}w long vs {short_weight:.1f}w short"

    # Find dominant outfit
    outfit_weights = {}
    for h in hits:
        outfit_weights[h["outfit"]] = outfit_weights.get(h["outfit"], 0) + h["weight"]
    dominant = max(outfit_weights, key=outfit_weights.get) if outfit_weights else None

    # Top hits sorted by weight
    top_hits = sorted(hits, key=lambda h: h["weight"], reverse=True)[:10]

    return {
        "price": round(price, 2) if price else None,
        "verdict": verdict,
        "reason": reason,
        "total_hits": total_hits,
        "long_weight": round(long_weight, 1),
        "short_weight": round(short_weight, 1),
        "dominant_outfit": dominant,
        "key_levels": dict(sorted(sma_levels.items(), key=lambda x: x[1]["weight"], reverse=True)),
        "top_hits": top_hits,
        "source": "coinbase",
    }


@app.get("/api/alerts")
async def get_alerts():
    """
    Major signal alerts — flags exceptional activity suggesting big positioning.
    Alert types: CONFLUENCE, HIGH_PERIOD_CLUSTER, OUTFIT_SURGE, AFFINITY_LOCK, MAGNETIZED_HIGH.
    Levels: critical (red), high (orange).
    """
    return {
        "count": len(latest_alerts),
        "critical": sum(1 for a in latest_alerts if a["level"] == "critical"),
        "high": sum(1 for a in latest_alerts if a["level"] == "high"),
        "alerts": latest_alerts,
    }


@app.get("/api/programs")
async def get_programs(status: str = Query(None)):
    """Active and recently terminated programs."""
    programs = get_active_programs(status)
    return programs


@app.get("/api/config")
async def get_config():
    """Current configuration."""
    return {
        "outfits": {k: v["periods"] for k, v in OUTFITS.items()},
        "tickers": TICKERS,
        "tickers_light": TICKERS_LIGHT,
        "timeframes": list(TIMEFRAMES.keys()),
        "primary_timeframes": PRIMARY_TIMEFRAMES,
    }


@app.get("/api/sma-table")
async def get_sma_table():
    """
    SMA reference table — which outfits and SMA periods apply to each ticker.
    Like Raul's original GitHub reference.
    """
    from .config import outfits_for_ticker, AFFINITIES

    table = []
    for ticker in sorted(TICKERS):
        allowed = outfits_for_ticker(ticker)
        if allowed is None:
            # No affinity — scans all outfits
            table.append({
                "ticker": ticker,
                "has_affinity": False,
                "outfits": [],
                "all_smas": [],
            })
            continue

        outfit_entries = []
        all_smas = set()
        for outfit_name in sorted(allowed):
            periods = OUTFITS[outfit_name]["periods"]
            all_smas.update(periods)
            outfit_entries.append({
                "outfit": outfit_name,
                "category": OUTFITS[outfit_name]["category"],
                "periods": periods,
            })

        table.append({
            "ticker": ticker,
            "has_affinity": True,
            "outfits": outfit_entries,
            "all_smas": sorted(all_smas),
        })

    return table


# ── Schwab Auth Endpoints ────────────────────────────────────────────────────

@app.get("/api/schwab/status")
async def schwab_status():
    """Check Schwab API authentication status and data source stats."""
    try:
        from .schwab_fetcher import auth_status, is_schwab_available
        status = auth_status()
        status["data_source_stats"] = get_data_source_stats()
        status["schwab_available"] = is_schwab_available()
        return status
    except ImportError:
        return {"authenticated": False, "reason": "schwab_fetcher not available"}


@app.get("/api/schwab/auth")
async def schwab_auth_url():
    """Get the OAuth2 authorization URL. Open this in a browser to log in."""
    try:
        from .schwab_fetcher import get_auth_url
        return {"auth_url": get_auth_url()}
    except ImportError:
        return JSONResponse(status_code=500, content={"error": "schwab_fetcher not available"})


@app.get("/api/schwab/callback")
async def schwab_callback_get(code: str = Query(None), error: str = Query(None)):
    """
    OAuth2 callback — Schwab redirects the browser here after login.
    Automatically exchanges the code for tokens.
    """
    if error:
        return JSONResponse(content={
            "status": "error",
            "error": error,
            "message": "Schwab denied authorization. Check your Schwab developer app settings.",
        })

    if not code:
        return JSONResponse(content={
            "status": "waiting",
            "message": "No authorization code received. Complete the Schwab login flow first.",
            "auth_url_endpoint": "/api/schwab/auth",
        })

    try:
        from .schwab_fetcher import complete_auth
        token = complete_auth(code)
        if token:
            return JSONResponse(content={
                "status": "authenticated",
                "message": "Schwab API connected! You can close this tab and return to the trading tool.",
            })
        return JSONResponse(status_code=400, content={
            "status": "failed",
            "error": "Token exchange failed — Schwab rejected the code. This usually means: "
                     "(1) the code expired (they're single-use and short-lived), "
                     "(2) the callback URL in .env doesn't exactly match Schwab Developer Portal, or "
                     "(3) the App Key/Secret have a character error (watch for l vs I, O vs 0).",
        })
    except ImportError:
        return JSONResponse(status_code=500, content={"error": "schwab_fetcher not available"})


@app.post("/api/schwab/callback")
async def schwab_callback_post(code: str = Query(...)):
    """Manual token exchange — POST /api/schwab/callback?code=<code>"""
    try:
        from .schwab_fetcher import complete_auth
        token = complete_auth(code)
        if token:
            return {"status": "authenticated", "message": "Schwab API connected!"}
        return JSONResponse(status_code=400, content={"error": "Failed to exchange code for token"})
    except ImportError:
        return JSONResponse(status_code=500, content={"error": "schwab_fetcher not available"})
