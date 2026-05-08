# SMA Outfits Detection Engine — Technical Specification

## 1. Overview

This document defines the computation engine for detecting SMA outfit signals across U.S. equity markets. The system ingests OHLC market data, computes Simple Moving Averages for predefined outfit configurations, detects precision alignments and breaches, classifies signal types, and outputs ranked summaries and a real-time event feed.

The logic is derived from the raultrades/SMA-outfits GitHub repository and live trade documentation posted by @rauItrades / @UnfairMarket on X.

---

## 2. Architecture

```
Market Data Source (Polygon / Alpaca / Lightspeed / Webull)
        │
        ▼
  ┌─────────────────┐
  │  Data Ingestion  │  Python service, writes to InfluxDB
  │  (OHLC Fetcher)  │  Handles multiple timeframes
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │    InfluxDB      │  Time-series storage
  │   (OHLC Data)    │  Bucket per timeframe
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │  SMA Compute     │  Calculates all outfit SMAs
  │  Engine          │  Per ticker × timeframe × outfit
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │  Signal Detector │  Alignment/breach/crossover detection
  │  & Classifier    │  Penny-precision matching
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │  Ranking Engine  │  Aggregates signals → outfit & ticker ranks
  │  & Aggregator    │  Computes bias, slope, structural context
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │  FastAPI Server  │  REST + WebSocket API
  │  (Backend)       │  Serves dashboard
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │  React Dashboard │  Outfit ranking, ticker ranking,
  │  (Frontend)      │  signal feed, ticker drill-down
  └─────────────────┘
```

---

## 3. SMA Outfit Configurations

### 3.1 Core Outfits (from GitHub repo)

| Name | SMA Periods | Category | Notes |
|------|------------|----------|-------|
| S&P | 10/50/200 | System | SPX on 30m chart |
| NAS | 20/100/250 | System | IXIC on 20m/30m chart |
| DJI | 30/60/90/300/600/900 | System | DJI on 15m/1h chart |
| Base 2/NVDA | 16/32/64/128/256/512 | Core | Binary progression |
| Waring's Problem | 19/37/73/143/279/548 | Core | Number theory integers |
| Time (144) | 18/36/72/144/288/576 | Core | 144(0) reference |
| Time (365) | 23/46/91/183/365/730 | Core | Calendar year |
| Time (366) | 23/46/92/183/366/732 | Core | Leap year |
| TSLA (420) | 27/53/105/210/420/840 | Core | Tesla / 420 meme |
| SVIX (211) | 26/52/106/211/422/844 | Core | |
| Resource missing (404) | 25/51/101/202/404/808 | Core | HTTP 404 |
| Regression (432) | 27/54/108/216/432/864 | Core | |
| AN (11s) | 11/44/88/111/444/888 | Angel | Angel numbers |
| AN (22s) | 22/55/77/222/555/777 | Angel | Angel numbers |
| AN (33s) | 33/66/99/333/666/999 | Angel | Angel numbers |
| US President (45) | 23/46/92/184/368/736 | Political | |
| US President (47) | 24/47/94/188/376/752 | Political | |
| Speaker House (56) | 28/56/112/224/448/896 | Political | |
| Russia Pres (2000) | 16/31/63/125/250/500 | Political | |
| Turkey Pres (12) | 24/48/96/192/384/768 | Political | |
| REPEATER_9 | 9/18/27/36/45/54 | Core | |

### 3.2 Dual Sequence Outfits (from live trades)

| Name | SMA Periods | Category | Observed On |
|------|------------|----------|-------------|
| Dual Seq (TSLQ) | 39/78/156/311/622/944 | Dual | TSLQ 2H chart |
| Dual Seq (IXIC) | 28/55/111/221/442/884 | Dual | IXIC 2H chart |

### 3.3 Ticker-Outfit Affinity Map

Not all outfits are equal across all tickers. Specific outfits have **primary affinity** to specific tickers based on symbolic, numerical, or structural relationships. When a primary-affinity outfit fires on its associated ticker, the signal weight receives a **2x multiplier**.

| Outfit | Primary Tickers | Reason |
|--------|----------------|--------|
| S&P (10/50/200) | SPX, SPY, UPRO, SPXU | System outfit for S&P 500 |
| NAS (20/100/250) | IXIC, QQQ, TQQQ, SQQQ | System outfit for NASDAQ |
| DJI (30/60/90/300/600/900) | DJI, DIA, UDOW, SDOW | System outfit for Dow Jones |
| Base 2/NVDA (16/32/64/128/256/512) | NVDA, SOXL, SOXS, AMD, INTC | Binary/computing reference |
| TSLA 420 (27/53/105/210/420/840) | TSLA, TSLR, TSLQ, TSLT | 420 meme / Tesla culture |
| AN 33s (33/66/99/333/666/999) | ORCX, and broadly applicable | Angel numbers — confirmed on ORCX live trade |
| AN 11s (11/44/88/111/444/888) | Broadly applicable | Angel numbers |
| AN 22s (22/55/77/222/555/777) | Broadly applicable | Angel numbers |
| SVIX 211 (26/52/106/211/422/844) | SVIX, UVXY, SVXY, UVIX | Volatility instruments |
| Time 365 (23/46/91/183/365/730) | Broadly applicable | Calendar year reference |
| Time 144 (18/36/72/144/288/576) | Broadly applicable | Fibonacci/time reference |
| Dual Seq TSLQ (39/78/156/311/622/944) | TSLQ, TSLR, TSLA | Confirmed on TSLQ live trade |
| Dual Seq IXIC (28/55/111/221/442/884) | IXIC, QQQ, TQQQ | Confirmed on IXIC live trade |

**Important:** All outfits are still computed against all tickers. The affinity map only affects scoring weight, not whether a signal is detected. A Base 2 outfit firing on TSLA is still a valid signal — it just doesn't get the affinity bonus.

The affinity map should be user-configurable. As new live trades are documented, affinities can be added or updated.

### 3.4 Parameter Rules

- All SMA periods are integers between 1 and 999
- Most outfits follow a near-doubling progression (each period ≈ 2× the previous)
- The outfit list is extensible; users should be able to add custom outfits
- The 3 "System" outfits (S&P, NAS, DJI) have only 3 SMAs; all others have 6

---

## 4. Ticker Universe

### 4.1 Primary Tickers

Major indices: SPX, IXIC, DJI
Index ETFs: SPY, QQQ, DIA, IWM
Leveraged/Inverse: TQQQ, SQQQ, UPRO, SDOW, UDOW, SOXL, SOXS, SPXU
Volatility: VIX, UVIX, UVXY, SVIX, SVXY
Mega-caps: AAPL, MSFT, AMZN, GOOG, NVDA, META, TSLA, AMD, NFLX
Financials: JPM, V, XLF
Leveraged single-stock: TSLQ, TSLR, ORCX, AAPU, AAPD, TSLT
Commodities/Bonds: GLD, TLT, TBT, USO, BOIL, DRN, DRIP, GUSH, LABU
Crypto: BITO, BITU, BITI
Other: COIN, QCOM, PYPL, UPST, AI, GME, UNH, ENPH, RBLX, ARM

### 4.2 Notes

- Every SMA outfit applies to every ticker (outfits are not ticker-specific)
- Certain timeframe + outfit combos are "proprietary" to specific indices (S&P → 30m, NAS → 20m/30m, DJI → 15m/1h) but all combos should still be computed

---

## 5. Timeframes

| Code | Period | Use Case |
|------|--------|----------|
| 1m | 1 minute | High-frequency detection |
| 2m | 2 minutes | |
| 5m | 5 minutes | Primary short-term |
| 10m | 10 minutes | |
| 15m | 15 minutes | Primary (DJI system, ORCX trade) |
| 20m | 20 minutes | NAS system alternate |
| 30m | 30 minutes | Primary (S&P system, NAS system) |
| 1h | 1 hour | DJI system alternate |
| 2h | 2 hours | Primary (TSLQ trade, IXIC trade) |
| 4h | 4 hours | Swing context |
| 1D | Daily | Structural bias |
| 1W | Weekly | Long-term context |

### 5.1 Priority Timeframes for Detection

The primary signal-generating timeframes are 5m through 2h. Daily and weekly are used for structural bias context only. Sub-minute timeframes (tick, 1s, 5s, 15s, 30s) exist in the repo spec but are impractical without direct broker feed access.

### 5.2 Institutional Hours Filter

Signals should be flagged as institutional-hours (9:30 AM – 4:00 PM EST) or extended-hours. Institutional-hours signals carry higher weight in the ranking algorithm.

---

## 6. Signal Detection Logic

### 6.0 The EOT Model (Equity + Outfit + Timeframe)

Per Raul's own definitions (March 1, 2026 @UnfairMarket thread):

The fundamental unit of analysis is the **EOT** — a specific combination of:
- **E**quity: A single stock, index, ETF, or commodity (e.g., TSLA, IXIC, GLD)
- **O**utfit: A specific SMA configuration / "key" (e.g., 33/66/99/333/666/999)
- **T**imeframe: A specific candlestick period (e.g., 15m, 2h)

Detection works by scanning every possible EOT combination. Each time an outfit's SMA value **precisely strikes** an equity's OHLC value on a given timeframe, that produces a signal. The ranking is a tabulation of how many strikes each outfit produces across all equities and timeframes.

Key quote: *"Each thread is the product of a tabulation of records that assesses every NYSE/NASDAQ/CBOE listed stock, each outfit or 'key', each time a 'key' precisely strikes an equity's OHLC value, and every relevant Timeframe to produce a signal."*

### 6.1 Core Detection: OHLC Hit Scoring

Per Raul (July 2025): *"A disproportionate amount of OHLC hits operate on a specific outfit/equity/timeframe. All [O/E/T] combinations are ranked — highest frequency of precise OHLC scores is the signal/key."*

Confirming the community-built tool: *"If this is recording OHLC value hits for each outfit and partitioned and then ranked then YES."*

The algorithm is a hit counter:

```
For each new candle (on any timeframe, any ticker):
  For each outfit:
    Compute all SMA values in the outfit for this ticker+timeframe
    For each SMA value in the outfit:
      For each OHLC component (Open, High, Low, Close):
        if OHLC_component precisely hits SMA_value (within threshold):
          → Record HIT: { outfit, ticker, timeframe, sma_period,
                          ohlc_component, price, sma_value, delta,
                          side: price >= sma_value ? "long" : "short" }

Ranking:
  - OUTFIT RANKING: Group hits by outfit → count total/long/short → sort by total desc
  - TICKER RANKING: Group hits by ticker → count total/long/short → sort by total desc
  - For each outfit row: DOM_TKR = ticker with most hits for that outfit
  - For each ticker row: DOM_OUTFIT = outfit with most hits for that ticker
```

**TOTAL** = count of all OHLC hits
**LONG** = count of hits where price is at or above the SMA value (support touch / bullish)
**SHORT** = count of hits where price is below the SMA value (resistance / bearish)
**L/S** = LONG / SHORT ratio

This is a pure frequency count. The outfit or ticker generating the most precise OHLC-to-SMA alignments ranks highest. No complex signal classification needed for the ranking — the ranking itself IS the signal.

### 6.1.1 Primary Detection Timeframes

Per Raul: timeframes range from **30 seconds to 30 minutes** as the primary detection window. Longer timeframes (1h, 2h, 4h, daily) are used for execution context and structural bias, but the core strike detection engine focuses on:

**Primary:** 30s, 1m, 2m, 5m, 10m, 15m, 20m, 30m
**Secondary (context):** 1h, 2h, 4h, 1D, 1W

### 6.2 Crossover Detection — LIMITED USE ONLY

Per Raul (March 4, 2026): *"Virtually none of the work I share has anything to do with Simple Moving Average crossings. It's all absolute selections based on specific SMA selections. Crossing only matter (even then only somewhat) with the S&P500/NASDAQ/Dow/Russel/SVIX systems. Otherwise forgetaboutit."*

**Crossovers are NOT part of the hit-counting ranking algorithm.** They are only used to determine the positive/negative state of the 5 system indices:
- S&P: MA10 vs MA50 on SPX 30m
- NASDAQ: MA20 vs MA100 on IXIC 20m/30m  
- DJI: MA90 vs MA300 on DJI 15m/1h
- Russell: (TBD)
- SVIX: (TBD)

For all other outfits and tickers, the detection is purely **OHLC values hitting SMA levels** — no crossover logic.

### 6.4 SMA Period Weighting

Longer-period SMAs generate higher-weight signals. Observed pattern: entries happen at the 4th, 5th, or 6th SMA in a 6-SMA outfit.

| Position in Outfit | Weight | Example (AN 33s) |
|-------------------|--------|-------------------|
| 1st (shortest) | 1x | MA33 |
| 2nd | 1.5x | MA66 |
| 3rd | 2x | MA99 |
| 4th | 4x | MA333 ← ORCX entry |
| 5th | 6x | MA666 |
| 6th (longest) | 8x | MA999 |

For 3-SMA system outfits (S&P, NAS, DJI): 1st = 1x, 2nd = 3x, 3rd = 8x.

**Affinity Multiplier:** If the detected signal is on a primary-affinity ticker-outfit pair (see Section 3.3), apply a 2x multiplier to the weight. Example: TSLA touching MA420 in the TSLA (420) outfit = 6x (position weight) × 2x (affinity) = 12x total weight.

**Institutional Hours Multiplier:** Signals detected during 9:30 AM – 4:00 PM EST receive 1.5x weight. Extended hours signals receive 1x.

**Final signal weight = position_weight × affinity_multiplier × hours_multiplier**

---

## 7. Signal Classification

Based on the detected alignment/breach context:

### 7.1 Precision Buy Algorithm

**Trigger:** Price touches or sits on one of the longer SMAs (positions 4-6) from above, after a drawdown period. The SMA acts as support.

**Evidence:** ORCX bought at MA333 (9.43), IXIC/TQQQ bought at MA884 (21,853.33).

**Output:** `{ type: "precision_buy", ticker, timeframe, outfit, sma_hit, entry_price, sma_value, delta, stop_level: sma_value - 0.01 }`

### 7.2 Automated Short Order

**Trigger:** Price breaches below a key SMA, confirming downward momentum. Or: price touches a key SMA from below (resistance rejection).

**Evidence:** TSLQ shorted at MA622 breach (23.98 vs 24.00, delta = -0.02).

**Output:** `{ type: "auto_short", ticker, timeframe, outfit, sma_hit, entry_price, sma_value, delta, stop_level: sma_value + 0.01 }`

### 7.3 Singular Point Hard Stop

**Trigger:** Price breaks an SMA by exactly $0.01 (one penny). This triggers forced liquidation.

**Output:** `{ type: "hard_stop", ticker, timeframe, outfit, sma_breached, breach_price, sma_value, direction: "above" | "below" }`

### 7.4 Optimized / Magnetized Buy

**Trigger:** During high volatility, price repeatedly gravitates toward an SMA level with disproportionate OHLC entries at that level. Detected by counting the frequency of touches within a rolling window.

**Output:** `{ type: "optimized_buy", ticker, timeframe, outfit, sma_target, touch_count, window_bars }`

### 7.5 SMA Crossover

**Trigger:** A shorter SMA crosses above or below a longer SMA within the same outfit.

**Output:** `{ type: "crossover", ticker, timeframe, outfit, fast_sma, slow_sma, direction: "bullish" | "bearish" }`

---

## 8. Ranking & Aggregation

### 8.0 Scope and Scale

Per Raul: *"It's every single equity, every single timeframe, every single outfit. Each combination of 60k+ ranked for highest hits."*

There is **no time window difference per timeframe** — the system does not look back further on slower timeframes. At any given moment, each active candle on each timeframe has SMA values computed from its full available history. The OHLC hit check is applied to the **current candle** (or most recent closed candle) across all EOT combinations simultaneously.

**Combinatorics:**
- With 50 curated tickers × 12 timeframes × 22 outfits = ~13,200 EOT combinations
- With full NYSE/NASDAQ/CBOE coverage (thousands of tickers) = 60,000+ EOT combinations
- Each EOT combo checks 4 OHLC values against 3–6 SMA values = 12–24 comparisons per combo
- Total comparisons per candle cycle: 150,000–1,500,000+

The ranking output is a flattened aggregation of all these comparisons, grouped by outfit (outfit ranking) and by ticker (ticker ranking), sorted by total hit count descending.

### 8.1 Two-Tier Signal Architecture

Per Raul: *"The 15m/1h 30/60/90/300/600/900 is a transient system that the DJI uses — just like the S&P 500's SPX is the 30m 10/50. While those are base systems to signal a trend higher or lower [going positive, going negative], precision arbitrage requires ranking every possible stock/timeframe/outfit for a signal."*

**Tier 1 — System Outfits (Macro Trend):**
The three system outfits on their proprietary timeframes determine overall market direction:
- S&P: MA10 vs MA50 on SPX 30m → positive (bullish) or negative (bearish)
- NAS: MA20 vs MA100 on IXIC 20m/30m → positive or negative
- DJI: MA90 vs MA300 on DJI 15m/1h → positive or negative

These set the **Overall Institutional Bias** displayed at the top of the dashboard.

**Tier 2 — Full EOT Ranking (Precision Arbitrage):**
All 60,000+ EOT combinations are scored by OHLC hit frequency and ranked. The top-ranked outfits and tickers represent where the most precise SMA-to-price alignments are occurring RIGHT NOW. This is where the tradeable signals come from.

For each outfit, across all tickers and timeframes:
- **Total:** Count of all detected signals
- **Long:** Count of bullish signals (precision_buy + bullish crossover + optimized_buy)
- **Short:** Count of bearish signals (auto_short + bearish crossover + hard_stop below)
- **L/S Ratio:** Long / Short
- **Slope:** Computed from the trend of the total signal count over a rolling window (Rising if increasing, Falling if decreasing)
- **Structural Bias:** Derived from the system-level outfit states:
  - If S&P system (MA10 > MA50): Bullish
  - If S&P system (MA10 < MA50): Bearish
  - Mixed/unclear: Neutral
- **Price Position:** Is current price above or below the majority of SMAs in the outfit?
  - Above: price > 4+ of 6 SMAs
  - Below: price < 4+ of 6 SMAs
  - Crossed: recently transitioned
- **Bias:** Final call combining struct_bias + slope + price_position + signal balance
- **Dominant Ticker:** Which ticker has the most signals for this outfit?

### 8.2 Ticker Ranking

For each ticker, across all outfits and timeframes:
- Same metrics as outfit ranking
- **Dominant Outfit:** Which outfit has the most signals for this ticker?
- **Active Signals:** Count of signals in the last N minutes

### 8.3 Overall Institutional Bias

Computed from the 3 system outfits:
- S&P positive = MA10 > MA50 on SPX 30m
- NAS positive = MA20 > MA100 on IXIC 20m/30m
- DJI positive = MA90 > MA300 on DJI 15m/1h

If 2+ systems positive → Overall Bullish
If 2+ systems negative → Overall Bearish
Mixed → Neutral

---

## 9. Data Model (InfluxDB)

### 9.1 OHLC Measurement

```
measurement: ohlc
tags: ticker, timeframe
fields: open, high, low, close, volume
timestamp: candle open time
```

### 9.2 SMA Values Measurement

```
measurement: sma_values
tags: ticker, timeframe, outfit_key, sma_period
fields: value
timestamp: computed at candle close time
```

### 9.3 Signals Measurement

```
measurement: signals
tags: ticker, timeframe, outfit_key, signal_type, sma_period
fields: price, sma_value, delta, stop_level, weight
timestamp: detection time
```

---

## 10. API Endpoints

### REST (FastAPI)

```
GET  /api/bias              → Overall institutional bias summary
GET  /api/outfits            → Outfit ranking table
GET  /api/tickers            → Ticker ranking table
GET  /api/signals?limit=50   → Recent signal feed
GET  /api/ticker/{symbol}    → Ticker detail (all outfits, SMA levels, signals)
GET  /api/outfit/{key}       → Outfit detail (all tickers, signals)
POST /api/outfits            → Add custom outfit
GET  /api/config             → Current configuration (thresholds, timeframes, etc.)
PUT  /api/config             → Update configuration
```

### WebSocket

```
WS /ws/feed → Real-time signal stream
WS /ws/bias → Real-time bias updates
```

---

## 11. Frontend Views

### 11.1 Main Dashboard

- Overall institutional bias banner (S&P/NAS/DJI system states)
- Tab: Outfit Ranking table (sortable, filterable)
- Tab: Ticker Ranking table (sortable, filterable, clickable for detail)
- Signal feed sidebar (real-time event stream, toggleable)

### 11.2 Ticker Detail Modal

- Stats: total/long/short/L/S ratio
- Dominant outfit and SMA level display (with above/below/touching status)
- Recent signals for this ticker
- Future: Candlestick chart with SMA overlay

### 11.3 Future: Chart View

- Candlestick chart for selected ticker + timeframe
- Overlay selected outfit's SMA lines
- Mark detected signals on chart
- Show stop levels

---

## 12. Live Trade Pattern Reference

These are the observed real-time trades that define the detection logic:

### Trade 1: TSLQ → Short (= Long TSLA)

- **Ticker:** TSLQ (2x Short Tesla ETF)
- **Timeframe:** 2H
- **Outfit:** 39/78/156/311/622/944 (Dual Seq)
- **SMA Hit:** MA622 = 24.00
- **Entry:** 23.98 (Short TSLQ at -$0.02 from MA622)
- **Signal Type:** Auto Short (breach below)
- **Direction:** Short TSLQ = Long TSLA (bought TSLR)
- **Stop:** Penny above MA622

### Trade 2: IXIC → Long (via TQQQ)

- **Ticker:** IXIC (NASDAQ Composite)
- **Timeframe:** 2H
- **Outfit:** 28/55/111/221/442/884 (Dual Seq)
- **SMA Hit:** MA884 = 21,853.33
- **Entry:** 21,853
- **Signal Type:** Precision Buy (touch on longest SMA)
- **Direction:** Long (bought TQQQ)
- **Stop:** Penny below MA884 (21,853.32)

### Trade 3: ORCX → Long

- **Ticker:** ORCX (2x Long Oracle ETF)
- **Timeframe:** 15M
- **Outfit:** 33/66/99/333/666/999 (AN 33s)
- **SMA Hit:** MA333 = 9.43
- **Entry:** 9.43 (exact touch)
- **Signal Type:** Precision Buy (touch on 4th SMA)
- **Direction:** Long
- **Stop:** Penny below 9.43 (9.42)

### Key Pattern

All three entries target the **4th, 5th, or 6th SMA** in a 6-SMA outfit. Entries are at penny-level precision. Stops are always a single penny breach of the entry SMA.

---

## 13. Implementation Phases

### Phase 1: Data Pipeline
- Set up InfluxDB
- Build OHLC data ingestion from free API (Polygon.io or Alpaca)
- Compute and store SMA values for all outfit × ticker × timeframe combos

### Phase 2: Signal Detection
- Implement alignment detection (threshold-based)
- Implement breach and crossover detection
- Signal classification (precision buy, auto short, hard stop, etc.)
- SMA period weighting

### Phase 3: Ranking & API
- Build aggregation logic (outfit ranking, ticker ranking)
- Overall institutional bias computation
- FastAPI server with REST + WebSocket endpoints

### Phase 4: Frontend Integration
- Replace mock data with API calls
- WebSocket for real-time signal feed
- Add chart view with SMA overlays

### Phase 5: Enhancements
- Custom outfit management
- Alert system (email/push for high-weight signals)
- Historical backtesting view
- Dark pool volume proxy detection
