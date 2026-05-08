# Commit 6def48c Diagnostic Report — April 8, 2026

## What We Fixed This Morning (OAuth)

### Initial Problem
- Schwab token expired after 7 days (April 1 → April 8)
- Backend couldn't authenticate: "no_token" / 401 Unauthorized
- Only BTC returning (Coinbase public API), equity data failing

### Root Cause
1. **Missing `.env` file** — Credentials not loaded
2. **Wrong variable names** — Backend expects `SCHWAB_APP_KEY`, not `CLIENT_ID`
3. **Callback URL mismatch** — Localhost doesn't work for Schwab OAuth; needs ngrok
4. **Token path confusion** — Different code versions look in different places

### Solution Applied
1. Created `/Users/rk/clawd/sma-outfits-engine/.env` with:
   ```
   SCHWAB_APP_KEY=zQHTzMc4K194G0ILXKaT3rOLK81lwSrrOTvSom2VadACpK7A
   SCHWAB_APP_SECRET=CFAmNLQ5LKv4cdHuetL6skkYvXvVw98H5RTFzH8kCYwoEoo0aO1gZplA29Svk7Zm
   SCHWAB_CALLBACK_URL=https://hypermodest-gennie-unoppressed.ngrok-free.dev/api/schwab/callback
   ```
2. Restarted ngrok tunnel (kept same URL)
3. User completed OAuth login
4. Token auto-saved to `.schwab_token.json`
5. Schwab authentication working ✅

---

## What Broke With Commit 6def48c

### When We Tried It
- Pulled `6def48c` from `https://github.com/rkremers123/raul-trading-system`
- Updated 5 files: `alerts.py`, `config.py`, `engine.py`, `ranking.py`, `App.jsx`
- Switched backend to `/Users/rk/clawd/raul-trading-system/`

### Issue 1: Token Path Changed
**Old Code (sma-outfits-engine):**
```python
_TOKEN_PATH = Path(__file__).resolve().parent.parent.parent / ".schwab_token.json"
# Resolves to: /Users/rk/clawd/.schwab_token.json
```

**New Code (6def48c):**
```python
_TOKEN_PATH = Path(__file__).resolve().parent.parent.parent / ".schwab_token.json"
# Resolves to: /Users/rk/clawd/raul-trading-system/.schwab_token.json
```

**Fix Applied:** Copied token file:
```bash
cp /Users/rk/clawd/.schwab_token.json /Users/rk/clawd/raul-trading-system/.schwab_token.json
```

**Status:** ✅ Token was found and refreshed

---

### Issue 2: Schwab API 400 Bad Request Errors

**Error Pattern:**
```
WARNING:backend.app.schwab_fetcher:Schwab API error for TSLL: 400 Client Error: Bad Request for url: 
https://api.schwabapi.com/marketdata/v1/pricehistory?symbol=TSLL&periodType=month&period=6&frequencyType=minute&frequency=15
```

**Analysis:**
- `periodType=month` is invalid for `frequencyType=minute`
- Schwab requires: minute candles use `periodType=day` (10-35 days history)
- Old code had this fixed in timeframe config
- New code reverted to broken parameters OR changed config structure

**Key Change in Commit 6def48c:**
- `config.py` got +91 lines
- Likely rewrote SCHWAB_TIMEFRAMES or fetch logic
- Parameter validation either missing or changed

**Files to Check:**
1. `/backend/app/config.py` — SCHWAB_TIMEFRAMES definition (line ~?)
2. `/backend/app/schwab_fetcher.py` — _fetch_ohlc() call signature
3. `/backend/app/engine.py` — How it passes timeframes to fetcher

---

## Current Status

**Working Backend:** `/Users/rk/clawd/sma-outfits-engine/` (commit 3e684aa)
- ✅ 27 tickers returning
- ✅ Schwab authenticated
- ✅ TSLA data complete

**Broken Backend:** `/Users/rk/clawd/raul-trading-system/` (commit 6def48c)
- ❌ Only BTC returning
- ✅ Schwab authenticated (token refreshes)
- ❌ 400 errors on all equity requests (TSLL, etc.)
- ❌ Rate limit throttling (35s+ sleeps)

---

## Action Items for Claude Code

**Goal:** Debug 6def48c, fix Schwab API parameters, get raul-trading-system working

**Questions to Investigate:**
1. What changed in `config.py` SCHWAB_TIMEFRAMES? (Old vs new)
2. Why are minute-level requests using `periodType=month`?
3. Did `schwab_fetcher.py` signature change? How is it called from engine/engine.py?
4. Are there new validations that are too strict or backwards?

**Test Approach:**
1. Compare working config (sma-outfits-engine) vs broken (6def48c)
2. Run single ticker test: `curl -X POST 'http://localhost:8001/api/scan?mode=light&ticker=TSLA'`
3. Check `/tmp/backend.log` for exact API call parameters
4. Fix parameter mapping in config.py or schwab_fetcher.py
5. Re-test scan

**Timeline:**
- This morning (Apr 8): OAuth fixed ✅
- Now: Identify 6def48c parameter bug
- Goal: Get raul-trading-system running so Claude Code pushes work properly

---

## Important Files

| File | Location | Purpose |
|------|----------|---------|
| **.env** | `/Users/rk/clawd/raul-trading-system/.env` | Schwab credentials (APP_KEY, APP_SECRET, CALLBACK_URL) |
| **Token** | `/Users/rk/clawd/raul-trading-system/.schwab_token.json` | Auto-generated after OAuth |
| **Config** | `/Users/rk/clawd/raul-trading-system/backend/app/config.py` | LIKELY CULPRIT — timeframe parameters |
| **Fetcher** | `/Users/rk/clawd/raul-trading-system/backend/app/schwab_fetcher.py` | Makes Schwab API calls |
| **Working Ref** | `/Users/rk/clawd/sma-outfits-engine/backend/app/config.py` | Gold standard — compare against this |

---

## One-Liner Comparison

To see what changed in config.py:
```bash
diff -u /Users/rk/clawd/sma-outfits-engine/backend/app/config.py \
       /Users/rk/clawd/raul-trading-system/backend/app/config.py | grep -A5 -B5 "SCHWAB_TIMEFRAMES\|periodType\|frequencyType"
```

Good luck! 🚀
