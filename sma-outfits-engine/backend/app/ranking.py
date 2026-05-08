"""
Ranking and aggregation logic.
Takes raw hits from the engine and produces outfit rankings, ticker rankings,
overall institutional bias, and active program lifecycle tracking.
"""

from collections import defaultdict
from datetime import datetime, timezone

from .config import (
    OUTFITS,
    SYSTEM_CROSSOVERS,
    DEFAULT_PROTOCOLS,
    PROTOCOL_CANDLE_CLOSE,
)
from .database import (
    save_hit_history,
    get_consecutive_sessions,
    upsert_active_program,
    get_active_programs,
    terminate_stale_programs,
    save_scan_snapshot,
    load_momentum_data,
)
from .engine import Hit, ScanResult
from typing import Optional, List, Dict, Set, Union


def compute_outfit_ranking(result: ScanResult, institutional_bias: Optional[dict] = None) -> List[dict]:
    """
    Aggregate hits by outfit → rank by total weighted hits descending.
    Returns list of dicts ready for the API.
    """
    outfit_data: dict[str, dict] = defaultdict(lambda: {
        "total": 0.0, "long": 0.0, "short": 0.0,
        "hit_count": 0, "long_count": 0, "short_count": 0,
        "ticker_hits": defaultdict(float),
        "sma_hits": defaultdict(float),
    })

    for hit in result.hits:
        od = outfit_data[hit.outfit]
        od["total"] += hit.weight
        od["hit_count"] += 1
        if hit.side == "long":
            od["long"] += hit.weight
            od["long_count"] += 1
        else:
            od["short"] += hit.weight
            od["short_count"] += 1
        od["ticker_hits"][hit.ticker] += hit.weight
        od["sma_hits"][hit.sma_period] += hit.weight

    ranked = []
    for outfit_name, data in outfit_data.items():
        cfg = OUTFITS.get(outfit_name, {})
        hit_count = data["hit_count"]
        long_count = data["long_count"]
        short_count = data["short_count"]
        ls_ratio = round(long_count / short_count, 2) if short_count > 0 else (
            99.0 if long_count > 0 else 0.0
        )

        # Dominant ticker for this outfit
        dom_ticker = max(data["ticker_hits"], key=data["ticker_hits"].get) if data["ticker_hits"] else ""

        # Key SMAs — show all periods from outfit config
        key_smas = "/".join(str(p) for p in cfg.get("periods", []))

        # Determine bias from L/S ratio
        if ls_ratio > 1.5:
            bias = "Bullish"
        elif ls_ratio < 0.67:
            bias = "Bearish"
        else:
            bias = "Neutral"

        # Slope: derived from L/S ratio — more longs = Rising, more shorts = Falling
        if ls_ratio > 1.1:
            slope = "Rising"
        elif ls_ratio < 0.9:
            slope = "Falling"
        else:
            slope = "Flat"

        # Structural bias from institutional (system outfit crossover) analysis
        struct_bias = ""
        if institutional_bias:
            struct_bias = institutional_bias.get("structural_bias", "")

        # Price position: Above if more longs, Below if more shorts, Crossed if close to 1:1
        if 0.9 <= ls_ratio <= 1.1:
            price_position = "Crossed"
        elif ls_ratio > 1.0:
            price_position = "Above"
        else:
            price_position = "Below"

        ranked.append({
            "sequence": outfit_name,
            "category": cfg.get("category", ""),
            "smas": key_smas,
            "total": round(data["total"], 1),
            "long": round(data["long"], 1),
            "short": round(data["short"], 1),
            "total_count": hit_count,
            "long_count": long_count,
            "short_count": short_count,
            "ls_ratio": ls_ratio,
            "slope": slope,
            "level": bias,            # absolute L/S level classification
            "momentum": None,         # populated later by enrich_rankings_with_momentum
            "momentum_delta": None,
            "institutional_bias": None,
            "structural_bias": struct_bias,
            "key_smas": key_smas,
            "price_position": price_position,
            "bias": bias,
            "dominant_ticker": dom_ticker,
        })

    ranked.sort(key=lambda x: -x["total_count"])
    for i, row in enumerate(ranked, 1):
        row["rank"] = i

    return ranked


def compute_ticker_ranking(result: ScanResult, institutional_bias: Optional[dict] = None) -> List[dict]:
    """
    Aggregate hits by ticker → rank by total hit count descending.

    Deduplicates by (sma_period, date) across outfits — because MA54 of
    a ticker's close produces the same value regardless of which outfit
    defines period 54. From a ticker's perspective, one SMA touch on one
    day = one hit.
    """
    # First pass: collect all hits per ticker, dedup by (sma_period, date)
    ticker_raw: dict[str, list] = defaultdict(list)
    for hit in result.hits:
        ticker_raw[hit.ticker].append(hit)

    ticker_data: dict[str, dict] = {}
    for ticker, hits in ticker_raw.items():
        # Dedup: for each (sma_period, date), keep only the highest-weight hit
        best: dict[tuple, object] = {}
        for hit in hits:
            date_str = hit.timestamp[:10]
            key = (hit.sma_period, date_str)
            if key not in best or hit.weight > best[key].weight:
                best[key] = hit

        deduped_hits = list(best.values())

        td = {
            "total": 0.0, "long": 0.0, "short": 0.0,
            "hit_count": 0, "long_count": 0, "short_count": 0,
            "outfit_hits": defaultdict(float),
            "sma_hits": defaultdict(float),
            "signals": deduped_hits,
        }

        for hit in deduped_hits:
            td["total"] += hit.weight
            td["hit_count"] += 1
            if hit.side == "long":
                td["long"] += hit.weight
                td["long_count"] += 1
            else:
                td["short"] += hit.weight
                td["short_count"] += 1
            td["outfit_hits"][hit.outfit] += hit.weight
            td["sma_hits"][hit.sma_period] += hit.weight

        ticker_data[ticker] = td

    ranked = []
    for ticker, data in ticker_data.items():
        hit_count = data["hit_count"]
        long_count = data["long_count"]
        short_count = data["short_count"]
        ls_ratio = round(long_count / short_count, 2) if short_count > 0 else (
            99.0 if long_count > 0 else 0.0
        )

        dom_outfit = max(data["outfit_hits"], key=data["outfit_hits"].get) if data["outfit_hits"] else ""
        top_smas = sorted(data["sma_hits"].items(), key=lambda x: -x[1])[:5]
        key_smas = ", ".join(f"MA{p}" for p, _ in top_smas)

        if ls_ratio > 1.5:
            bias = "Bullish"
        elif ls_ratio < 0.67:
            bias = "Bearish"
        else:
            bias = "Neutral"

        if ls_ratio > 1.1:
            slope = "Rising"
        elif ls_ratio < 0.9:
            slope = "Falling"
        else:
            slope = "Flat"

        struct_bias = ""
        if institutional_bias:
            struct_bias = institutional_bias.get("structural_bias", "")

        if 0.9 <= ls_ratio <= 1.1:
            price_position = "Crossed"
        elif ls_ratio > 1.0:
            price_position = "Above"
        else:
            price_position = "Below"

        ranked.append({
            "ticker": ticker,
            "total": round(data["total"], 1),
            "long": round(data["long"], 1),
            "short": round(data["short"], 1),
            "total_count": hit_count,
            "long_count": long_count,
            "short_count": short_count,
            "ls_ratio": ls_ratio,
            "dominant_outfit": dom_outfit,
            "slope": slope,
            "level": bias,
            "momentum": None,
            "momentum_delta": None,
            "institutional_bias": None,
            "structural_bias": struct_bias,
            "key_smas": key_smas,
            "price_position": price_position,
            "bias": bias,
            "active_signals": len(data["signals"]),
        })

    ranked.sort(key=lambda x: -x["total_count"])
    for i, row in enumerate(ranked, 1):
        row["rank"] = i

    return ranked


def compute_institutional_bias(result: ScanResult) -> dict:
    """
    Compute overall institutional bias from the 3 system outfit crossovers.
    S&P: MA10 > MA50 on SPX 30m → positive
    NAS: MA20 > MA100 on IXIC 30m → positive
    DJI: MA90 > MA300 on DJI 1h → positive
    2+ positive → Bullish, 2+ negative → Bearish, else Neutral.
    """
    # We approximate from hit data: if system outfit has more long than short → positive
    systems = {}
    for sys_name, cfg in SYSTEM_CROSSOVERS.items():
        sys_hits = [
            h for h in result.hits
            if h.outfit == sys_name and h.ticker == cfg["ticker"]
        ]
        long_w = sum(h.weight for h in sys_hits if h.side == "long")
        short_w = sum(h.weight for h in sys_hits if h.side == "short")
        systems[sys_name] = "positive" if long_w >= short_w else "negative"

    positive_count = sum(1 for v in systems.values() if v == "positive")

    if positive_count >= 2:
        overall = "Bullish"
    elif positive_count <= 1 and len(systems) >= 3:
        overall = "Bearish"
    else:
        overall = "Neutral"

    # Find dominant outfit from all hits
    outfit_totals: dict[str, float] = defaultdict(float)
    for hit in result.hits:
        outfit_totals[hit.outfit] += hit.weight
    dom_outfit = max(outfit_totals, key=outfit_totals.get) if outfit_totals else ""

    return {
        "overall_bias": overall,
        "systems": systems,
        "dominant_outfit": dom_outfit,
        "structural_bias": overall,
        "price_position": "Above" if overall == "Bullish" else "Below",
        "session_date": result.scan_time[:10] if result.scan_time else "",
    }


def build_scan_snapshot(result: ScanResult, time_window: str) -> List[dict]:
    """
    Build per-outfit L/S ratio snapshots from scan results for a given time window.
    Saves them to the DB and returns the snapshot list.
    """
    outfit_agg: dict[str, dict] = defaultdict(lambda: {
        "long_count": 0, "short_count": 0, "total_weight": 0.0,
    })

    for hit in result.hits:
        od = outfit_agg[hit.outfit]
        od["total_weight"] += hit.weight
        if hit.side == "long":
            od["long_count"] += 1
        else:
            od["short_count"] += 1

    session_date = result.scan_time[:10] if result.scan_time else datetime.now(timezone.utc).strftime("%Y-%m-%d")

    snapshots = []
    for outfit_key, data in outfit_agg.items():
        lc, sc = data["long_count"], data["short_count"]
        ls_ratio = round(lc / sc, 2) if sc > 0 else (99.0 if lc > 0 else 0.0)
        snapshots.append({
            "outfit_key": outfit_key,
            "ticker": None,  # outfit-level aggregate
            "long_count": lc,
            "short_count": sc,
            "ls_ratio": ls_ratio,
            "total_weight": round(data["total_weight"], 1),
        })

    save_scan_snapshot(session_date, time_window, snapshots)
    return snapshots


def enrich_rankings_with_momentum(rankings: list[dict], session_date: str) -> List[dict]:
    """
    Add momentum data to outfit rankings by comparing two time windows.
    Adds 'momentum', 'momentum_delta', 'level' fields.
    """
    momentum_data = load_momentum_data(session_date)

    for row in rankings:
        outfit_key = row.get("sequence", "")
        mom = momentum_data.get(outfit_key)
        if mom:
            row["momentum"] = mom["momentum"]
            row["momentum_delta"] = mom["delta"]
            row["level"] = _level_label(row.get("ls_ratio", 0))
            # Institutional bias: if momentum is Falling, bias shifts bearish
            if mom["momentum"] == "Falling" and row.get("bias") != "Bearish":
                row["institutional_bias"] = "Bearish"
            elif mom["momentum"] == "Rising" and row.get("bias") != "Bullish":
                row["institutional_bias"] = "Bullish"
            else:
                row["institutional_bias"] = row.get("bias", "Neutral")
        else:
            row["momentum"] = None
            row["momentum_delta"] = None
            row["level"] = _level_label(row.get("ls_ratio", 0))
            row["institutional_bias"] = row.get("bias", "Neutral")

    return rankings


def _level_label(ls_ratio: float) -> str:
    """Classify absolute L/S ratio into a level label."""
    if ls_ratio > 1.5:
        return "Bullish"
    elif ls_ratio < 0.67:
        return "Bearish"
    else:
        return "Neutral"


def hits_to_signals(result: ScanResult, per_ticker: int = 20) -> List[dict]:
    """
    Convert raw hits into signal feed entries for the frontend.

    Stores up to `per_ticker` top signals for each ticker, ensuring the
    ticker detail drilldown has data even after server restart (when
    in-memory latest_result is lost).
    """
    # Group by ticker, take top N per ticker by weight
    ticker_hits: dict[str, list] = defaultdict(list)
    for hit in result.hits:
        ticker_hits[hit.ticker].append(hit)

    signals = []
    for ticker, hits in ticker_hits.items():
        hits_sorted = sorted(hits, key=lambda h: -h.weight)[:per_ticker]
        for hit in hits_sorted:
            sig_type = "precision_buy" if hit.side == "long" else "auto_short"
            signals.append({
                "type": sig_type,
                "ticker": hit.ticker,
                "timeframe": hit.timeframe,
                "outfit": hit.outfit,
                "sma_period": hit.sma_period,
                "ohlc": hit.ohlc_component,
                "price": hit.price,
                "sma_value": hit.sma_value,
                "delta": hit.delta,
                "side": hit.side,
                "weight": hit.weight,
                "timestamp": hit.timestamp,
            })

    # Sort overall by weight descending
    signals.sort(key=lambda s: -s["weight"])
    return signals


def compute_ticker_detail(result: ScanResult, symbol: str) -> dict:
    """Get detailed info for a single ticker."""
    ticker_hits = [h for h in result.hits if h.ticker == symbol]

    total = sum(h.weight for h in ticker_hits)
    long_w = sum(h.weight for h in ticker_hits if h.side == "long")
    short_w = sum(h.weight for h in ticker_hits if h.side == "short")

    outfit_totals: dict[str, float] = defaultdict(float)
    for h in ticker_hits:
        outfit_totals[h.outfit] += h.weight
    dom_outfit = max(outfit_totals, key=outfit_totals.get) if outfit_totals else ""

    signals = []
    for h in sorted(ticker_hits, key=lambda x: -x.weight)[:20]:
        signals.append({
            "type": "precision_buy" if h.side == "long" else "auto_short",
            "outfit": h.outfit,
            "timeframe": h.timeframe,
            "sma_period": h.sma_period,
            "ohlc": h.ohlc_component,
            "price": h.price,
            "sma_value": h.sma_value,
            "delta": h.delta,
            "weight": h.weight,
            "timestamp": h.timestamp,
            "side": h.side,
        })

    return {
        "ticker": symbol,
        "total": round(total, 1),
        "long": round(long_w, 1),
        "short": round(short_w, 1),
        "ls_ratio": round(long_w / short_w, 2) if short_w > 0 else 99.0,
        "dominant_outfit": dom_outfit,
        "signals": signals,
    }


# ── Active Programs + Magnetized Detection ──────────────────────────────────

def _sma_position_index(outfit_name: str, sma_period: int) -> int:
    """Get the position index (0-5) of an SMA within its outfit."""
    periods = OUTFITS.get(outfit_name, {}).get("periods", [])
    try:
        return periods.index(sma_period)
    except ValueError:
        return 0


def update_active_programs(result: ScanResult) -> List[dict]:
    """
    Process scan results to update active program lifecycle:
    1. Record hit history for today's session
    2. Detect magnetized buys (consecutive-session hits)
    3. Create/update active programs
    4. Terminate programs that are no longer producing hits
    Returns the updated list of all programs.
    """
    now_str = datetime.now(timezone.utc).isoformat()
    session_date = now_str[:10]

    # 1. Build hit records for history
    hit_records = []
    seen_eot = set()
    current_eot_keys = set()

    for hit in result.hits:
        eot_key = f"{hit.ticker}:{hit.outfit}:{hit.timeframe}:{hit.sma_period}"
        current_eot_keys.add(eot_key)

        if eot_key not in seen_eot:
            seen_eot.add(eot_key)
            hit_records.append({
                "ticker": hit.ticker,
                "outfit": hit.outfit,
                "timeframe": hit.timeframe,
                "sma_period": hit.sma_period,
                "price": hit.price,
                "sma_value": hit.sma_value,
                "side": hit.side,
                "weight": hit.weight,
            })

    # 2. Save today's hits to history
    save_hit_history(session_date, hit_records)

    # 3. For each unique EOT combo in current scan, create/update active program
    for rec in hit_records:
        consec = get_consecutive_sessions(
            rec["ticker"], rec["outfit"], rec["timeframe"], rec["sma_period"]
        )
        is_magnetized = consec >= 2

        # Determine protocol
        pos_idx = _sma_position_index(rec["outfit"], rec["sma_period"])
        protocol = DEFAULT_PROTOCOLS.get(pos_idx, "penny_breach")

        # Magnetized → upgrade to candle_close
        if is_magnetized:
            protocol = PROTOCOL_CANDLE_CLOSE

        # Compute stop level based on protocol
        sma_val = rec.get("sma_value", 0) or 0
        if protocol == "penny_breach":
            stop_level = round(sma_val - 0.01, 2)
        elif protocol == "point_break":
            stop_level = round(sma_val - 1.0, 2)
        else:  # candle_close
            stop_level = round(sma_val, 2)

        upsert_active_program({
            "ticker": rec["ticker"],
            "outfit_key": rec["outfit"],
            "timeframe": rec["timeframe"],
            "sma_period": rec["sma_period"],
            "entry_price": rec.get("price"),
            "sma_value": sma_val,
            "protocol": protocol,
            "stop_level": stop_level,
            "status": "active",
            "is_magnetized": is_magnetized,
            "activated_at": session_date,
            "terminated_at": None,
            "consecutive_sessions": consec,
        })

    # 4. Terminate programs no longer producing hits
    terminate_stale_programs(current_eot_keys, now_str)

    return get_active_programs()
