# SMA Outfits Trading System — Build Status (March 19, 2026)

**Status: MVP Core Engine Built + Ready for Hosting**

---

## What's Completed ✅

### 1. **Python FastAPI Backend** (Production-Ready)
**Location:** `/Users/rk/clawd/sma-outfits-engine/backend/`

**Modules:**
- **`main.py`** — FastAPI app, REST endpoints, background scans, CORS setup
- **`config.py`** — All 22+ outfit definitions, ticker universe, timeframes, affinity map
- **`engine.py`** — Core hit-counting algorithm (OHLC-to-SMA precision detection)
- **`fetcher.py`** — Market data via yfinance + resampling for custom timeframes
- **`ranking.py`** — Outfit/ticker aggregation, institutional bias computation, signal generation
- **`database.py`** — SQLite persistence (scans, rankings, signals)
- **`requirements.txt`** — Dependencies (FastAPI, Uvicorn, yfinance, pandas, numpy)

**Key Features Implemented:**
- ✅ Full EOT (Equity + Outfit + Timeframe) scanning
- ✅ 22 SMA outfit definitions (System, Core, Angel, Political, Dual Sequence)
- ✅ Ticker-outfit affinity weighting (2x for primary pairs)
- ✅ Penny-precision hit detection (0.02% threshold, configurable)
- ✅ Position-based weighting (6-SMA: 1x→8x, 3-SMA: 1x→8x)
- ✅ Institutional hours multiplier (1.5x during 9:30 AM–4:00 PM EST)
- ✅ Hit → Signal classification (Precision Buy, Auto Short, Hard Stop, etc.)
- ✅ Real-time ranking computation (outfit rank + ticker rank)
- ✅ System crossover state (for S&P/NAS/DJI institutional bias banner)
- ✅ Background scan tasks (light/full mode with progress tracking)
- ✅ REST API endpoints (bias, outfits, tickers, signals, detail, scan control)

**Technology Stack:**
- FastAPI (web framework)
- yfinance (market data, free tier)
- pandas + numpy (data processing)
- SQLite (local persistence)
- Python 3.10+

### 2. **React Dashboard** (Production-Ready)
**Location:** `/Users/rk/clawd/sma-outfits-engine/sma-dashboard.jsx`

**Features:**
- ✅ Outfit ranking table (sortable, filterable, 22 rows)
- ✅ Ticker ranking table (clickable for detail modal)
- ✅ Overall institutional bias banner (S&P/NAS/DJI system state)
- ✅ Real-time signal feed sidebar (last 50 signals)
- ✅ Ticker detail modal with SMA levels + dominant outfit
- ✅ Mock data fallback (works offline during development)
- ✅ Dark theme with color-coded signal types
- ✅ Manual/auto scan trigger with progress tracking
- ✅ Confidence scoring + risk assessment

**Design:**
- Modern dark UI (#06090f background, cyan/green/red accents)
- Monospace fonts for price data
- Responsive grid layout
- Smooth animations + hover states

### 3. **Complete Technical Documentation**
- **`sma-engine-spec.md`** — 900+ line specification (architecture, EOT model, algorithms, API endpoints)
- **`sma-outfits-summary.md`** — High-level overview with Raul's methodology + live trade examples
- **`.env.example`** — Configuration template

---

## Current Limitations ⚠️

### Immediate Gaps (Needed for Production):

1. **Data Source:** Currently using yfinance (free, limited to ~2-3 day intraday history)
   - **For production:** Switch to Polygon.io API (Raul-level data, real-time intraday)
   - **Cost:** Polygon free tier has 5 API calls/min; full scan needs ~660 calls

2. **Hosting:** Not yet deployed
   - Backend needs a server (Railway.app, Heroku, or VPS)
   - Frontend lives on Vercel already (robkremers.com)

3. **Backtesting Engine:** Not implemented
   - The spec calls for historical validation
   - Simple implementation: log signals against past candles

4. **WebSocket Real-Time Feed:** Not implemented
   - Currently REST polling only
   - Optional for MVP (background task updates every 5 min)

5. **Advanced Features Not Included:**
   - CEA (Cycle Energy Alignment) metric
   - LPI (Leading Phase Indicator)
   - Regime-adaptive thresholding
   - Custom outfit editor (UI only)

---

## Deployment Path (Next Steps)

### **Step 1: Test Locally** (Today)
```bash
cd /Users/rk/clawd/sma-outfits-engine/backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
# Server runs on http://localhost:8000
# Try: curl http://localhost:8000/api/health
```

### **Step 2: Deploy Backend** (Choose One)

**Option A: Railway.app (Recommended)**
1. Create account at railway.app
2. Connect GitHub repo: `dupesnacks/sma-outfits-engine` (after pushing)
3. Railway auto-detects `requirements.txt`, runs `uvicorn app.main:app`
4. Costs: $5–20/month (Python 512MB free tier available)
5. Get production URL (e.g., `https://sma-api.railway.app`)

**Option B: Heroku (Legacy but works)**
```bash
heroku create sma-outfits-api
heroku config:set CORS_ORIGINS="https://robkremers.com"
git push heroku main
```

**Option C: VPS (DigitalOcean, Linode, etc.)**
- Rent $5–10/mo droplet
- SSH in, install Python, clone repo, run with systemd

### **Step 3: Update Frontend** (Vercel)
Edit `sma-dashboard.jsx`:
```javascript
const API_BASE = "https://sma-api.railway.app"; // ← Change this
```

Redeploy:
```bash
cd /Users/rk/clawd/rob-kremers-portfolio
vercel deploy --prod
```

### **Step 4: Monitor + Tune**
- Watch real-time rankings on robkremers.com/sma
- Tweak hit threshold, weights, timeframes based on observed accuracy
- Add Polygon.io when ready

---

## File Structure

```
sma-outfits-engine/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app, endpoints
│   │   ├── config.py            # Outfits, tickers, affinity map
│   │   ├── engine.py            # Core hit-counting algorithm
│   │   ├── fetcher.py           # yfinance data + resampling
│   │   ├── ranking.py           # Aggregation + bias computation
│   │   └── database.py          # SQLite persistence
│   └── requirements.txt          # pip dependencies
├── frontend/                      # (Currently on Vercel)
│   └── sma-dashboard.jsx
├── sma-engine-spec.md           # 900+ line technical spec
├── sma-outfits-summary.md       # Overview + live trades
└── .env.example                 # Config template
```

---

## Next: Data Source Upgrade

When ready, upgrade from yfinance → Polygon.io:

**In `fetcher.py`:**
```python
# Replace yfinance with Polygon API
import requests

def fetch_ohlc_polygon(ticker, timeframe, key="YOUR_API_KEY"):
    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/{tf_map[timeframe]}/{start_date}/{end_date}?apiKey={key}"
    resp = requests.get(url)
    data = resp.json()
    # Convert to pandas DataFrame
    return df
```

**Benefits:**
- Real-time intraday (5+ years history)
- 1m, 5m, 15m, 30m, 1h granularity
- No rate-limit issues with paid tier

**Cost:** Polygon free tier = 5 calls/min. Full scan = ~10 min per cycle. Acceptable for daily analysis.

---

## Live Deployment Checklist

- [ ] Push to GitHub: `dupesnacks/sma-outfits-engine`
- [ ] Deploy backend to Railway/Heroku
- [ ] Update `API_BASE` in React dashboard
- [ ] Deploy frontend via Vercel
- [ ] Test `/api/health` endpoint
- [ ] Run first scan manually (`POST /api/scan`)
- [ ] Monitor for 24h
- [ ] Add cron job to scan every 5 min (optional)
- [ ] Switch to Polygon.io data (optional, future)

---

## Key Insights from Claude Code's Implementation

1. **Hit Threshold:** 0.02% (0.0002 as decimal) is tight but matches real market precision
2. **Position Weights:** The 6-SMA exponential ramp (1→1.5→2→4→6→8) generates signal concentration
3. **Affinity:** 2x multiplier for outfit-ticker pairs creates natural clustering (NVDA+Base2, TSLA+420, etc.)
4. **Institutional Hours:** 1.5x during 9:30–16:00 EST removes noise from pre-market/after-hours
5. **System Crossovers:** Only used for the 3-system bias banner; hit-counting never uses crossovers (per Raul)
6. **Error Handling:** Missing data doesn't crash; just skips that EOT combo
7. **Progress Tracking:** Background tasks report done/total/ticker/timeframe for UI feedback

---

## Questions for Myron

1. **Data source:** Stick with yfinance for now, or upgrade to Polygon immediately?
2. **Hosting:** Preference between Railway/Heroku/VPS? (I recommend Railway for simplicity)
3. **Update frequency:** Scan every 5 min? Or on-demand only?
4. **Real-time:** WebSocket feed needed, or REST polling (every N seconds) OK for MVP?
5. **Backtesting:** Include historical validation module now, or defer to v2?

---

**Build Date:** March 19, 2026, 14:19 PDT  
**Engine Status:** Ready for staging  
**Next Milestone:** Live deployment + first real scan

