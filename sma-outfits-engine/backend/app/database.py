"""
SQLite database layer for persisting scan results, active programs, and hit history.
Stores the latest scan result so the dashboard can load data without re-scanning.
Also tracks algorithm lifecycle (active → terminated) and consecutive-session hits
for magnetized buying algorithm detection.
"""

import json
import sqlite3
import os
from typing import Optional, List, Dict
from datetime import datetime, timezone

DB_PATH = os.environ.get("SMA_DB_PATH", "sma_data.db")


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    """Create tables if they don't exist."""
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS scan_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scan_time TEXT NOT NULL,
            mode TEXT NOT NULL DEFAULT 'light',
            bias_json TEXT,
            outfits_json TEXT,
            tickers_json TEXT,
            signals_json TEXT,
            stats_json TEXT,
            created_at TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_scan_time ON scan_results(scan_time);

        -- Active programs: tracks algorithm lifecycle (active → terminated)
        CREATE TABLE IF NOT EXISTS active_programs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT NOT NULL,
            outfit_key TEXT NOT NULL,
            timeframe TEXT NOT NULL,
            sma_period INTEGER NOT NULL,
            entry_price REAL,
            sma_value REAL,
            protocol TEXT NOT NULL DEFAULT 'penny_breach',
            stop_level REAL,
            status TEXT NOT NULL DEFAULT 'active',
            is_magnetized INTEGER NOT NULL DEFAULT 0,
            activated_at TEXT NOT NULL,
            terminated_at TEXT,
            consecutive_sessions INTEGER NOT NULL DEFAULT 1,
            UNIQUE(ticker, outfit_key, timeframe, sma_period, activated_at)
        );
        CREATE INDEX IF NOT EXISTS idx_active_status ON active_programs(status);
        CREATE INDEX IF NOT EXISTS idx_active_ticker ON active_programs(ticker);

        -- Scan snapshots: per-window L/S ratio snapshots for momentum tracking
        CREATE TABLE IF NOT EXISTS scan_snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_date TEXT NOT NULL,
            time_window TEXT NOT NULL,  -- 'open', 'midday', 'close', 'full'
            outfit_key TEXT NOT NULL,
            ticker TEXT NOT NULL DEFAULT '__ALL__',  -- '__ALL__' = outfit-level aggregate
            long_count INTEGER NOT NULL DEFAULT 0,
            short_count INTEGER NOT NULL DEFAULT 0,
            ls_ratio REAL NOT NULL DEFAULT 0.0,
            total_weight REAL NOT NULL DEFAULT 0.0,
            scanned_at TEXT NOT NULL,
            UNIQUE(session_date, time_window, outfit_key, ticker)
        );
        CREATE INDEX IF NOT EXISTS idx_snapshot_date_window
            ON scan_snapshots(session_date, time_window);
        CREATE INDEX IF NOT EXISTS idx_snapshot_outfit
            ON scan_snapshots(outfit_key, session_date);

        -- Hit history: per-session record of EOT hits for magnetized detection
        CREATE TABLE IF NOT EXISTS hit_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_date TEXT NOT NULL,
            ticker TEXT NOT NULL,
            outfit_key TEXT NOT NULL,
            timeframe TEXT NOT NULL,
            sma_period INTEGER NOT NULL,
            price REAL,
            sma_value REAL,
            side TEXT,
            weight REAL,
            UNIQUE(session_date, ticker, outfit_key, timeframe, sma_period)
        );
        CREATE INDEX IF NOT EXISTS idx_hit_eot ON hit_history(ticker, outfit_key, timeframe, sma_period);
    """)
    conn.commit()

    # Migration: fix NULL ticker values in scan_snapshots and deduplicate
    _migrate_scan_snapshots(conn)

    conn.close()


def _migrate_scan_snapshots(conn):
    """
    One-time migration: convert ticker=NULL to '__ALL__' and deduplicate.
    SQLite treats NULL != NULL so the UNIQUE constraint failed on NULLs.
    """
    try:
        # Check if there are any NULL ticker rows to migrate
        nulls = conn.execute(
            "SELECT COUNT(*) FROM scan_snapshots WHERE ticker IS NULL"
        ).fetchone()[0]
        if nulls == 0:
            return

        # For each (date, window, outfit) group with NULL ticker,
        # keep only the most recent row and convert to __ALL__
        conn.execute("""
            DELETE FROM scan_snapshots
            WHERE ticker IS NULL
              AND id NOT IN (
                SELECT MAX(id)
                FROM scan_snapshots
                WHERE ticker IS NULL
                GROUP BY session_date, time_window, outfit_key
              )
        """)
        conn.execute(
            "UPDATE scan_snapshots SET ticker = '__ALL__' WHERE ticker IS NULL"
        )
        conn.commit()
    except Exception:
        pass  # Table might not exist yet on fresh installs


def save_scan(
    scan_time: str,
    mode: str,
    bias: dict,
    outfits: list,
    tickers: list,
    signals: list,
    stats: dict,
):
    """Persist a scan result."""
    conn = get_db()
    conn.execute(
        """INSERT INTO scan_results
           (scan_time, mode, bias_json, outfits_json, tickers_json, signals_json, stats_json, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            scan_time,
            mode,
            json.dumps(bias),
            json.dumps(outfits),
            json.dumps(tickers),
            json.dumps(signals),
            json.dumps(stats),
            datetime.now(timezone.utc).isoformat(),
        ),
    )
    conn.commit()
    conn.close()


def load_latest_scan() -> Optional[Dict]:
    """Load the most recent scan result."""
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM scan_results ORDER BY id DESC LIMIT 1"
    ).fetchone()
    conn.close()

    if row is None:
        return None

    return {
        "scan_time": row["scan_time"],
        "mode": row["mode"],
        "bias": json.loads(row["bias_json"]),
        "outfits": json.loads(row["outfits_json"]),
        "tickers": json.loads(row["tickers_json"]),
        "signals": json.loads(row["signals_json"]),
        "stats": json.loads(row["stats_json"]),
    }


# ── Hit History (for magnetized buy detection) ──────────────────────────────

def save_hit_history(session_date: str, hits: list[dict]):
    """
    Save today's hits into hit_history. Each unique (date, ticker, outfit, tf, sma)
    combo is stored once per session. Used to detect consecutive-session hits.
    """
    conn = get_db()
    for h in hits:
        conn.execute(
            """INSERT OR REPLACE INTO hit_history
               (session_date, ticker, outfit_key, timeframe, sma_period, price, sma_value, side, weight)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                session_date, h["ticker"], h["outfit"], h["timeframe"],
                h["sma_period"], h.get("price"), h.get("sma_value"),
                h.get("side"), h.get("weight"),
            ),
        )
    conn.commit()
    conn.close()


def get_consecutive_sessions(ticker: str, outfit_key: str, timeframe: str, sma_period: int) -> int:
    """
    Count how many of the most recent sessions in a row had a hit for this EOT+SMA combo.
    Returns 0 if no history exists.
    """
    conn = get_db()
    rows = conn.execute(
        """SELECT DISTINCT session_date FROM hit_history
           WHERE ticker = ? AND outfit_key = ? AND timeframe = ? AND sma_period = ?
           ORDER BY session_date DESC LIMIT 10""",
        (ticker, outfit_key, timeframe, sma_period),
    ).fetchall()
    conn.close()

    if not rows:
        return 0

    # Count consecutive days from the most recent
    dates = [r["session_date"] for r in rows]
    count = 1
    for i in range(1, len(dates)):
        # Simple check: if dates are on consecutive calendar days
        from datetime import date as dt_date
        try:
            d1 = dt_date.fromisoformat(dates[i - 1])
            d2 = dt_date.fromisoformat(dates[i])
            diff = (d1 - d2).days
            if diff <= 2:  # allow weekends (up to 2-day gap for Fri→Mon)
                count += 1
            else:
                break
        except ValueError:
            break
    return count


# ── Active Programs ─────────────────────────────────────────────────────────

def upsert_active_program(program: dict):
    """Insert or update an active program."""
    conn = get_db()
    conn.execute(
        """INSERT INTO active_programs
           (ticker, outfit_key, timeframe, sma_period, entry_price, sma_value,
            protocol, stop_level, status, is_magnetized, activated_at,
            terminated_at, consecutive_sessions)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
           ON CONFLICT(ticker, outfit_key, timeframe, sma_period, activated_at)
           DO UPDATE SET
             sma_value = excluded.sma_value,
             stop_level = excluded.stop_level,
             status = excluded.status,
             is_magnetized = excluded.is_magnetized,
             terminated_at = excluded.terminated_at,
             consecutive_sessions = excluded.consecutive_sessions""",
        (
            program["ticker"], program["outfit_key"], program["timeframe"],
            program["sma_period"], program.get("entry_price"),
            program.get("sma_value"), program.get("protocol", "penny_breach"),
            program.get("stop_level"), program.get("status", "active"),
            int(program.get("is_magnetized", False)),
            program["activated_at"], program.get("terminated_at"),
            program.get("consecutive_sessions", 1),
        ),
    )
    conn.commit()
    conn.close()


def get_active_programs(status: Optional[str] = None) -> List[Dict]:
    """Load active programs, optionally filtered by status."""
    conn = get_db()
    if status:
        rows = conn.execute(
            "SELECT * FROM active_programs WHERE status = ? ORDER BY activated_at DESC",
            (status,),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM active_programs ORDER BY status ASC, activated_at DESC"
        ).fetchall()
    conn.close()

    return [
        {
            "id": r["id"],
            "ticker": r["ticker"],
            "outfit_key": r["outfit_key"],
            "timeframe": r["timeframe"],
            "sma_period": r["sma_period"],
            "entry_price": r["entry_price"],
            "sma_value": r["sma_value"],
            "protocol": r["protocol"],
            "stop_level": r["stop_level"],
            "status": r["status"],
            "is_magnetized": bool(r["is_magnetized"]),
            "activated_at": r["activated_at"],
            "terminated_at": r["terminated_at"],
            "consecutive_sessions": r["consecutive_sessions"],
        }
        for r in rows
    ]


# ── Scan Snapshots (for momentum tracking) ─────────────────────────────────

def get_snapshot_dates() -> List[Dict]:
    """
    Return all dates that have snapshot data, with their available windows.
    Returns [{date, windows: ['midday', 'close', ...], scan_count}] newest first.
    """
    conn = get_db()
    rows = conn.execute("""
        SELECT session_date, time_window, COUNT(*) as cnt
        FROM scan_snapshots
        GROUP BY session_date, time_window
        ORDER BY session_date DESC, time_window
    """).fetchall()
    conn.close()

    dates: dict[str, dict] = {}
    for r in rows:
        d = r["session_date"]
        if d not in dates:
            dates[d] = {"date": d, "windows": [], "scan_count": 0}
        dates[d]["windows"].append(r["time_window"])
        dates[d]["scan_count"] += r["cnt"]

    return list(dates.values())

def save_scan_snapshot(
    session_date: str,
    time_window: str,
    outfit_snapshots: list[dict],
):
    """
    Save L/S ratio snapshots for a given time window.
    Each entry: {outfit_key, ticker (optional), long_count, short_count, ls_ratio, total_weight}
    """
    conn = get_db()
    scanned_at = datetime.now(timezone.utc).isoformat()
    for snap in outfit_snapshots:
        # Use '__ALL__' sentinel instead of NULL so UNIQUE constraint works
        ticker = snap.get("ticker") or "__ALL__"
        conn.execute(
            """INSERT OR REPLACE INTO scan_snapshots
               (session_date, time_window, outfit_key, ticker,
                long_count, short_count, ls_ratio, total_weight, scanned_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                session_date, time_window, snap["outfit_key"],
                ticker,
                snap.get("long_count", 0), snap.get("short_count", 0),
                snap.get("ls_ratio", 0.0), snap.get("total_weight", 0.0),
                scanned_at,
            ),
        )
    conn.commit()
    conn.close()


def load_scan_snapshots(session_date: str, time_window: Optional[str] = None) -> List[Dict]:
    """
    Load snapshots for a given date, optionally filtered by time_window.
    Returns list of dicts with all snapshot fields.
    """
    conn = get_db()
    if time_window:
        rows = conn.execute(
            """SELECT * FROM scan_snapshots
               WHERE session_date = ? AND time_window = ?
               ORDER BY outfit_key""",
            (session_date, time_window),
        ).fetchall()
    else:
        rows = conn.execute(
            """SELECT * FROM scan_snapshots
               WHERE session_date = ?
               ORDER BY time_window, outfit_key""",
            (session_date,),
        ).fetchall()
    conn.close()
    return [
        {
            "outfit_key": r["outfit_key"],
            "ticker": None if r["ticker"] == "__ALL__" else r["ticker"],
            "time_window": r["time_window"],
            "long_count": r["long_count"],
            "short_count": r["short_count"],
            "ls_ratio": r["ls_ratio"],
            "total_weight": r["total_weight"],
            "scanned_at": r["scanned_at"],
        }
        for r in rows
    ]


def load_momentum_data(session_date: str) -> dict:
    """
    Load snapshots for a date and compute momentum per outfit.
    Compares the two most recent windows available (any combination of
    open→midday, midday→close, open→close, or full).
    Returns {outfit_key: {earlier_ls, later_ls, earlier_window, later_window, momentum, delta}}.
    """
    conn = get_db()
    rows = conn.execute(
        """SELECT time_window, outfit_key, ls_ratio
           FROM scan_snapshots
           WHERE session_date = ? AND ticker = '__ALL__'
           ORDER BY outfit_key""",
        (session_date,),
    ).fetchall()
    conn.close()

    # Window ordering: earlier → later
    window_order = {"open": 0, "midday": 1, "close": 2, "full": 3}

    # Build lookup: {outfit_key: {window: ls_ratio}}
    data: dict[str, dict] = {}
    for r in rows:
        ok = r["outfit_key"]
        if ok not in data:
            data[ok] = {}
        data[ok][r["time_window"]] = r["ls_ratio"]

    # Compute momentum using the two most recent windows
    momentum = {}
    for outfit_key, windows in data.items():
        # Sort available windows by time order
        sorted_windows = sorted(windows.keys(), key=lambda w: window_order.get(w, 99))
        if len(sorted_windows) < 2:
            continue

        # Use the two most recent windows
        earlier = sorted_windows[-2]
        later = sorted_windows[-1]
        earlier_ls = windows[earlier]
        later_ls = windows[later]

        delta = round(later_ls - earlier_ls, 2)
        if delta < -0.1:
            direction = "Falling"
        elif delta > 0.1:
            direction = "Rising"
        else:
            direction = "Flat"
        momentum[outfit_key] = {
            "earlier_window": earlier,
            "later_window": later,
            "earlier_ls": earlier_ls,
            "later_ls": later_ls,
            "momentum": direction,
            "delta": delta,
        }
    return momentum


def terminate_stale_programs(current_eot_keys: set[str], terminated_at: str):
    """
    Mark programs as terminated if they are 'active' but their EOT key
    (ticker:outfit:tf:sma) is no longer producing hits.
    """
    conn = get_db()
    active = conn.execute(
        "SELECT id, ticker, outfit_key, timeframe, sma_period FROM active_programs WHERE status = 'active'"
    ).fetchall()

    for row in active:
        key = f"{row['ticker']}:{row['outfit_key']}:{row['timeframe']}:{row['sma_period']}"
        if key not in current_eot_keys:
            conn.execute(
                "UPDATE active_programs SET status = 'terminated', terminated_at = ? WHERE id = ?",
                (terminated_at, row["id"]),
            )

    conn.commit()
    conn.close()
