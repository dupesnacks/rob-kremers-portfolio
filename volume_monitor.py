from typing import Optional

#!/usr/bin/env python3
"""
Volume Monitor — detects unusual volume patterns and alerts via Discord.

── HOW TO ADD A TICKER ──────────────────────────────────────────────────────
Add the ticker symbol to the WATCHLIST below. That's it.
ClawdyMcBotFace: "add XXXX to WATCHLIST in volume_monitor.py"
─────────────────────────────────────────────────────────────────────────────

Setup:
  1. Add DISCORD_WEBHOOK_URL to your .env file
  2. Run manually:  python3 volume_monitor.py
  3. Or schedule:   add to cron after market close (~4:30 PM ET daily)

Requires: requests, python-dotenv (pip install requests python-dotenv)
Uses the same Schwab token as OpenClaw — no separate auth needed.
"""

import base64
import json
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests

# ── WATCHLIST — add tickers here ─────────────────────────────────────────
WATCHLIST = [
    "BYND",
    "SABS",
]
# ─────────────────────────────────────────────────────────────────────────

# ── ALERT THRESHOLDS — adjust if needed ──────────────────────────────────
BASELINE_DAYS       = 20    # rolling window for average volume
SPIKE_THRESHOLD     = 2.5   # today > 2.5× avg  → SPIKE
ELEVATED_THRESHOLD  = 1.5   # today > 1.5× avg  → ELEVATED
TREND_THRESHOLD     = 0.20  # 7-day avg up 20%+ vs prior 7-day avg → TREND
ACCUMULATION_DAYS   = 3     # N consecutive elevated days → ACCUMULATION
# ─────────────────────────────────────────────────────────────────────────

# ── PATHS & ENV ───────────────────────────────────────────────────────────
_SCRIPT_DIR = Path(__file__).resolve().parent

def _load_env():
    env_path = _SCRIPT_DIR / ".env"
    if not env_path.exists():
        # try sma-outfits-engine location
        env_path = _SCRIPT_DIR.parent / "sma-outfits-engine" / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

_load_env()

DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL", "")
_APP_KEY    = os.environ.get("SCHWAB_APP_KEY", "")
_APP_SECRET = os.environ.get("SCHWAB_APP_SECRET", "")

# Token file: same location OpenClaw uses (3 dirs up from backend/app/)
# For standalone use, check common locations
_TOKEN_CANDIDATES = [
    _SCRIPT_DIR / ".schwab_token.json",
    _SCRIPT_DIR / "sma-outfits-engine" / ".schwab_token.json",
    Path.home() / "clawd" / "sma-outfits-engine" / ".schwab_token.json",
    Path.home() / "clawd" / ".schwab_token.json",
]

def _find_token_file():
    for p in _TOKEN_CANDIDATES:
        if p.exists():
            return p
    return None

# ── SCHWAB AUTH ───────────────────────────────────────────────────────────

def _get_access_token() -> Optional[str]:
    token_path = _find_token_file()
    if not token_path:
        print("ERROR: No .schwab_token.json found. Run OpenClaw auth first.")
        return None

    try:
        token = json.loads(token_path.read_text())
    except Exception as e:
        print(f"ERROR: Could not read token file: {e}")
        return None

    saved_at   = token.get("saved_at", 0)
    expires_in = token.get("expires_in", 1800)
    refresh_expires = saved_at + 7 * 86400

    if time.time() > refresh_expires - 3600:
        print("ERROR: Schwab refresh token expired. Re-authenticate via OpenClaw.")
        return None

    # Refresh if access token expired
    if time.time() > saved_at + expires_in - 60:
        credentials = base64.b64encode(f"{_APP_KEY}:{_APP_SECRET}".encode()).decode()
        try:
            resp = requests.post(
                "https://api.schwabapi.com/v1/oauth/token",
                headers={
                    "Authorization": f"Basic {credentials}",
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": token["refresh_token"],
                },
                timeout=30,
            )
            resp.raise_for_status()
            new_token = resp.json()
            new_token.setdefault("refresh_token", token["refresh_token"])
            new_token["saved_at"] = time.time()
            token_path.write_text(json.dumps(new_token, indent=2))
            return new_token["access_token"]
        except Exception as e:
            print(f"ERROR: Token refresh failed: {e}")
            return None

    return token["access_token"]


# ── DATA FETCH ────────────────────────────────────────────────────────────

def fetch_daily_ohlcv(ticker: str) -> Optional[list[dict]]:
    """Fetch ~60 days of daily candles from Schwab. Returns [{date, volume, close}]."""
    access_token = _get_access_token()
    if not access_token:
        return None

    start_ms = int((datetime.now(timezone.utc) - timedelta(days=60)).timestamp() * 1000)
    try:
        resp = requests.get(
            "https://api.schwabapi.com/marketdata/v1/pricehistory",
            headers={"Authorization": f"Bearer {access_token}"},
            params={
                "symbol": ticker,
                "periodType": "year",
                "frequencyType": "daily",
                "frequency": 1,
                "startDate": start_ms,
                "needExtendedHoursData": "false",
            },
            timeout=30,
        )
        resp.raise_for_status()
        candles = resp.json().get("candles", [])
        if not candles:
            print(f"  {ticker}: no candles returned")
            return None

        return [
            {
                "date": datetime.fromtimestamp(c["datetime"] / 1000, tz=timezone.utc).strftime("%Y-%m-%d"),
                "volume": int(c.get("volume", 0)),
                "close":  float(c["close"]),
            }
            for c in sorted(candles, key=lambda x: x["datetime"])
        ]
    except Exception as e:
        print(f"  {ticker}: fetch failed — {e}")
        return None


# ── ANALYSIS ──────────────────────────────────────────────────────────────

def analyze(ticker: str, records: list[dict]) -> Optional[dict]:
    if len(records) < BASELINE_DAYS + 8:
        print(f"  {ticker}: insufficient history ({len(records)} days)")
        return None

    records = sorted(records, key=lambda r: r["date"])
    volumes = [r["volume"] for r in records]
    today   = records[-1]

    baseline = volumes[-(BASELINE_DAYS + 1):-1]
    baseline_avg = sum(baseline) / len(baseline) if baseline else 0
    if baseline_avg == 0:
        return None

    rvol = today["volume"] / baseline_avg

    # 7-day trend vs prior 7-day
    recent_7 = volumes[-8:-1]
    prior_7  = volumes[-15:-8]
    trend_pct = None
    if len(recent_7) == 7 and len(prior_7) == 7:
        r_avg = sum(recent_7) / 7
        p_avg = sum(prior_7) / 7
        if p_avg > 0:
            trend_pct = (r_avg - p_avg) / p_avg

    # Consecutive elevated days (before today)
    consecutive = 0
    for v in reversed(volumes[:-1]):
        if v >= baseline_avg * ELEVATED_THRESHOLD:
            consecutive += 1
        else:
            break

    alerts = []

    if rvol >= SPIKE_THRESHOLD:
        alerts.append(f"🚨 SPIKE — {rvol:.1f}× average ({(rvol-1)*100:.0f}% above baseline)")
    elif rvol >= ELEVATED_THRESHOLD:
        alerts.append(f"⚠️ ELEVATED — {rvol:.1f}× average ({(rvol-1)*100:.0f}% above baseline)")

    if trend_pct is not None and trend_pct >= TREND_THRESHOLD:
        alerts.append(f"📈 TREND — 7-day avg volume up {trend_pct*100:.0f}% vs prior 7 days")

    if consecutive >= ACCUMULATION_DAYS:
        alerts.append(f"🔄 ACCUMULATION — {consecutive} consecutive days above 1.5× baseline")

    return {
        "ticker":      ticker,
        "date":        today["date"],
        "close":       today["close"],
        "volume":      today["volume"],
        "baseline":    int(baseline_avg),
        "rvol":        round(rvol, 2),
        "trend_pct":   round(trend_pct * 100, 1) if trend_pct is not None else None,
        "consecutive": consecutive,
        "alerts":      alerts,
    }


# ── DISCORD ───────────────────────────────────────────────────────────────

def _vol(n: int) -> str:
    """Format volume as human-readable (1.2M, 450K)."""
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n/1_000:.0f}K"
    return str(n)


def build_message(results: list[dict]) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    triggered = [r for r in results if r["alerts"]]
    clean     = [r for r in results if not r["alerts"]]

    lines = [f"**📊 Volume Monitor** — {now}"]

    if triggered:
        lines.append("")
        for r in triggered:
            lines.append(f"**${r['ticker']}** @ ${r['close']:.2f}  |  Vol: {_vol(r['volume'])} vs {_vol(r['baseline'])} avg")
            for alert in r["alerts"]:
                lines.append(f"  {alert}")

    if clean:
        lines.append("")
        normal = "  ".join(f"${r['ticker']} {r['rvol']:.1f}×" for r in clean)
        lines.append(f"✅ Normal: {normal}")

    if not triggered and not clean:
        lines.append("No data retrieved.")

    return "\n".join(lines)


def send_discord(message: str):
    if not DISCORD_WEBHOOK_URL:
        print("\n── Discord message (no webhook configured) ──")
        print(message)
        return
    try:
        resp = requests.post(
            DISCORD_WEBHOOK_URL,
            json={"content": message},
            timeout=10,
        )
        if resp.status_code not in (200, 204):
            print(f"Discord error: {resp.status_code} — {resp.text}")
        else:
            print("Discord alert sent.")
    except Exception as e:
        print(f"Discord send failed: {e}")
        print(message)


# ── JSON DATA FILE ────────────────────────────────────────────────────────

# Written alongside this script; the dashboard reads it via fetch().
_DATA_PATH = _SCRIPT_DIR / "volume_data.json"
_HISTORY_LIMIT = 60   # days kept per ticker


def _load_existing() -> dict:
    if _DATA_PATH.exists():
        try:
            return json.loads(_DATA_PATH.read_text())
        except Exception:
            pass
    return {"tickers": {}, "alert_log": []}


def _upsert_history(history: list[dict], entry: dict) -> list[dict]:
    """Replace same-date entry or append, then cap at _HISTORY_LIMIT."""
    history = [h for h in history if h["date"] != entry["date"]]
    history.append(entry)
    history.sort(key=lambda h: h["date"])
    return history[-_HISTORY_LIMIT:]


def _upsert_alert_log(log: list[dict], result: dict) -> list[dict]:
    """Add alert log entry for today if there are alerts; one entry per (date, ticker)."""
    if not result["alerts"]:
        return log
    key_date = result["date"]
    key_ticker = result["ticker"]
    log = [e for e in log if not (e["date"] == key_date and e["ticker"] == key_ticker)]
    log.append({
        "date":    key_date,
        "ticker":  key_ticker,
        "alerts":  result["alerts"],
        "rvol":    result["rvol"],
        "close":   result["close"],
    })
    log.sort(key=lambda e: (e["date"], e["ticker"]), reverse=True)
    return log[:200]   # keep last 200 alert events


def update_json(results: list[dict]):
    data = _load_existing()
    data.setdefault("tickers", {})
    data.setdefault("alert_log", [])

    for result in results:
        ticker = result["ticker"]
        history_entry = {
            "date":     result["date"],
            "volume":   result["volume"],
            "close":    result["close"],
            "baseline": result["baseline"],
            "rvol":     result["rvol"],
            "alerts":   result["alerts"],
        }
        ticker_block = data["tickers"].setdefault(ticker, {"latest": {}, "history": []})
        ticker_block["latest"]  = {k: result[k] for k in
            ("date", "close", "volume", "baseline", "rvol", "trend_pct", "consecutive", "alerts")}
        ticker_block["history"] = _upsert_history(ticker_block["history"], history_entry)
        data["alert_log"] = _upsert_alert_log(data["alert_log"], result)

    data["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M ET")
    _DATA_PATH.write_text(json.dumps(data, indent=2))
    print(f"Data written → {_DATA_PATH}")


# ── MAIN ──────────────────────────────────────────────────────────────────

def run():
    print(f"Volume Monitor — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Watching: {', '.join(WATCHLIST)}\n")

    results = []
    for ticker in WATCHLIST:
        print(f"Fetching {ticker}...")
        records = fetch_daily_ohlcv(ticker)
        if not records:
            continue
        result = analyze(ticker, records)
        if not result:
            continue
        results.append(result)
        status = result["alerts"] if result["alerts"] else [f"normal ({result['rvol']:.2f}×)"]
        print(f"  → {' | '.join(status)}")

    print()
    update_json(results)
    message = build_message(results)
    send_discord(message)


if __name__ == "__main__":
    run()
