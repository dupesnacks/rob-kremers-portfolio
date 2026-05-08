# SMA Outfits — How Raul's System Works

## Summary

Raul (@rauItrades / @UnfairMarket) has documented what he claims is the core operational framework of U.S. equity markets: **SMA Outfits**. These are predefined sets of Simple Moving Average periods (all integers 1–999) that institutional trading divisions use as precision triggers for executing trades. His GitHub repo (github.com/raultrades/SMA-outfits) has 842 stars and contains the theoretical framework, outfit definitions, and 40+ real-time documented trade threads.

The central claim: markets are not primarily driven by fundamentals or retail flow, but by algorithmic exploitation of specific SMA configurations. These outfits produce precise OHLC (Open/High/Low/Close) hits that rank which instruments and outfits are most active at any given moment.

---

## The Core Algorithm (Confirmed by Raul)

Raul confirmed the detection method in his own words:

> "A disproportionate amount of OHLC hits operate on a specific outfit/equity/timeframe. All [O/E/T] combinations are ranked — highest frequency of precise OHLC scores is the signal/key."

And validating a follower's tool that replicated his output:

> "If this is recording OHLC value hits for each outfit and partitioned and then ranked then YES"

### How it works:

1. **Define SMA Outfits** — Each outfit is a set of SMA periods (e.g., 16/32/64/128/256/512)
2. **Scan every EOT combination** — EOT = Equity + Outfit + Timeframe. Every stock × every outfit × every timeframe. 60,000+ combinations.
3. **Count OHLC hits** — For each candle, check: does the Open, High, Low, or Close price precisely match any SMA value in any outfit? If yes, that's a "hit."
4. **Rank by frequency** — The outfit with the most hits across all tickers/timeframes = #1. The ticker with the most hits across all outfits/timeframes = #1.
5. **The top-ranked is the signal** — Raul shares the "top ranked" outfit/ticker at any given moment. That's what produces his trade threads.

### What's NOT part of the core ranking:

Raul explicitly stated:

> "Virtually none of the work I share has anything to do with Simple Moving Average crossings. It's all absolute selections based on specific SMA selections. Crossing only matter (even then only somewhat) with the S&P500/NASDAQ/Dow/Russel/SVIX systems. Otherwise forgetaboutit."

Crossovers are only used to determine if the major market systems are "positive" (bullish) or "negative" (bearish). Everything else is pure OHLC-to-SMA hit counting.

---

## The SMA Outfits

### System Outfits (Macro Trend — "The Systems")

These three outfits determine overall market direction. When they're "positive" (short SMA above long SMA), the market trends up. When "negative," it trends down.

| System | Outfit | Chart | Positive Signal |
|--------|--------|-------|-----------------|
| S&P 500 | 10/50/200 | SPX 30-min | MA10 > MA50 |
| NASDAQ | 20/100/250 | IXIC 20-min/30-min | MA20 > MA100 |
| Dow Jones | 30/60/90/300/600/900 | DJI 15-min/1-hour | MA90 > MA300 |

Raul says: when all three systems are negative, crashes happen. No firm steps in before JPM, BlackRock, Citadel, etc.

### Core Outfits

| Name | SMA Periods | Notes |
|------|------------|-------|
| Base 2/NVDA | 16/32/64/128/256/512 | Binary progression. Consistently #1 in rankings. |
| Waring's Problem | 19/37/73/143/279/548 | Number theory (Hilbert's Waring's Problem) |
| Time (144) | 18/36/72/144/288/576 | 1440 minutes in a day |
| Time (365) | 23/46/91/183/365/730 | Calendar year |
| TSLA (420) | 27/53/105/210/420/840 | Tesla / 420 meme culture |
| SVIX (211) | 26/52/106/211/422/844 | Volatility instruments |
| Resource missing (404) | 25/51/101/202/404/808 | HTTP 404 reference |
| Regression (432) | 27/54/108/216/432/864 | |
| Alphabet (100) | 25/50/100/200/400/800 | Google/Alphabet |

### Angel Number Outfits

| Name | SMA Periods |
|------|------------|
| AN (11s) | 11/44/88/111/444/888 |
| AN (22s) | 22/55/77/222/555/777 |
| AN (33s) | 33/66/99/333/666/999 |

### Political Outfits

| Name | SMA Periods | Reference |
|------|------------|-----------|
| US President (45) | 23/46/92/184/368/736 | 45th president |
| US President (47) | 24/47/94/188/376/752 | 47th president |
| Speaker House (56) | 28/56/112/224/448/896 | Speaker seat 56 |
| Russia Pres (2000) | 16/31/63/125/250/500 | Putin year 2000 |
| Turkey Pres (12) | 24/48/96/192/384/768 | Erdogan seat 12 |

### Dual Sequence Outfits (from live trades)

| Name | SMA Periods | Confirmed On |
|------|------------|-------------|
| Dual Seq (TSLQ) | 39/78/156/311/622/944 | TSLQ 2H chart, March 2026 |
| Dual Seq (IXIC) | 28/55/111/221/442/884 | IXIC 2H chart, March 2026 |

---

## Ticker-Outfit Affinities

Specific outfits have primary relationships with specific tickers:

- **TSLA, TSLR, TSLQ** → TSLA (420) outfit — 420 connection
- **NVDA, SOXL, SOXS, AMD** → Base 2/NVDA — binary/computing
- **SPY, SPX** → S&P (10/50/200) — the system outfit
- **QQQ, IXIC** → NAS (20/100/250) — the system outfit
- **ORCX** → AN (33s) — confirmed live trade
- **Volatility (UVIX, SVIX, UVXY)** → SVIX (211)

All outfits CAN fire on any ticker. The affinity just means those pairings have historically higher relevance.

---

## How Raul Trades It (Observed Pattern)

From 4 confirmed live trades in March 2026:

### Trade Pattern:
1. Identify the top-ranked outfit + ticker from the EOT scan
2. Look at the **longer-period SMAs** (positions 4–6 in a 6-SMA outfit)
3. Enter when price **precisely touches** one of those long SMAs (penny-level precision)
4. Stop loss = **one penny breach** of the SMA level

### Confirmed Trades:

| Trade | Ticker | Timeframe | Outfit | SMA Hit | Entry | Stop |
|-------|--------|-----------|--------|---------|-------|------|
| Short TSLQ (=long TSLA) | TSLQ | 2H | 39/78/156/311/622/944 | MA622=24.00 | 23.98 [-$0.02] | Penny above |
| Long via TQQQ | IXIC | 2H | 28/55/111/221/442/884 | MA884=21,853.33 | 21,853 | Penny below |
| Long ORCX | ORCX | 15M | 33/66/99/333/666/999 | MA333=9.43 | 9.43 [exact] | 9.42 |
| Long SPXU | SPXU | 20M | 180 outfit | MA720 | 48.78 | Penny breach |

### Key Observations:
- Entries always target the **4th, 5th, or 6th SMA** in an outfit (the longer periods)
- Precision is penny-level ($0.00 to $0.02 from the SMA value)
- Stop is ALWAYS a single penny breach — no wider stops
- Inverse ETFs are used directionally (short TSLQ = long TSLA)

---

## The Ranking Output

The confirmed-correct output (validated by Raul) looks like two ranked tables:

### Outfit Ranking — "Top 20 Outfits Bias Summary"
Shows which SMA outfits are producing the most OHLC hits right now:
- **Rank, Sequence (outfit name), Total hits, Long, Short, L/S ratio, Slope, Structural Bias, Key SMAs, Price Position, Bias, Dominant Ticker**

### Ticker Ranking — "Ticker Ranking (SMA 1-999)"
Shows which stocks have the most OHLC hits right now:
- **Rank, Ticker, Total hits, Long, Short, L/S ratio, Dominant Outfit, Slope, Structural Bias, Key SMAs, Price Position, Bias**

### Overall Institutional Bias
A header showing: Overall Bias (Bearish/Bullish/Neutral), Dominant Outfit, Structural Bias, Key SMAs, Price Position. Derived from the three system outfits.

On a confirmed bearish day (March 17, 2026):
- Base 2/NVDA was #1 outfit with 1,615 hits
- UVIX was #1 ticker with 1,733 hits (heavily short-skewed at 0.16 L/S)
- Overall bias: Bearish

---

## The Symbolic/Cryptographic Layer

Raul claims outfit selection has an intentional symbolic dimension:

- **420** for Tesla (meme culture)
- **512** for NVDA (binary/computing)
- **911** used on September 11th (WTC homage)
- **Presidential numbers** tied to current political figures
- **Dual sequence outfits** used when two "dual-serving" heads of state meet (e.g., Trump 45/47 meeting Japan's leader who also served twice)
- **840** — the Cybertruck bombing on New Year's 2025, first police call at 8:40 AM. Raul believes this was intentional: "Someone clearly set off those fireworks at that time since Elon Musk's banker buddies use the number 840 to manipulate equities/stocks."

The pattern: **signals come first, news comes after to justify the move.** The outfits are selected in advance based on symbolic context, then executed with precision.

---

## Signal Types (from Raul's repo)

- **Precision Buying Algorithm** — Price touches a long-period SMA from above after a drawdown. The SMA acts as support. Entry at the touch, stop at penny breach.
- **Automated Short Order** — Price breaches below a key SMA. Short entry at the breach point.
- **Singular Point Hard Stop Order** — Price breaks an SMA by exactly one penny. Triggers forced liquidation. Creates large volume candles (often via dark pools).
- **Magnetized Buying Algorithm** — SMA level "cradles" price. Price gravitates to and bounces off the SMA repeatedly. The SMA becomes a floor. Becomes a buy-and-hold if overnight session confirms with a new SMA parameter.

---

## What We're Building

A real-time detection engine and dashboard that replicates the confirmed-correct ranking output:

### Backend (Python/FastAPI)
- Fetches OHLC data from Polygon.io across all tickers × timeframes
- Computes SMA values for all 22+ outfits
- Counts OHLC-to-SMA hits across all 60,000+ EOT combinations
- Ranks outfits and tickers by hit frequency
- Serves via REST API + WebSocket

### Frontend (React)
- Outfit ranking table (sortable, filterable)
- Ticker ranking table (clickable for detail)
- Overall institutional bias banner
- Real-time signal feed sidebar
- Manual scan trigger (conserves API calls)

### Key Design Decisions
- **Manual refresh** — Polygon free tier has 5 calls/minute. Full scan uses ~660 calls. Light scan uses 15.
- **No crossover logic in ranking** — per Raul's explicit statement
- **Penny-level precision threshold** — configurable, default 0.02% of price
- **Affinity weighting** — known ticker-outfit pairs get 2x weight boost

---

## Sources

- GitHub: github.com/raultrades/SMA-outfits (842 stars, Apache 2.0 license)
- Twitter/X: @rauItrades, @UnfairMarket
- Confirmed output: Community-built tool validated by Raul on March 17, 2026
- Live trades: March 2026 documented threads (TSLQ, IXIC/TQQQ, ORCX, SPXU)
- Raul's glossary thread: March 1, 2026 @UnfairMarket

---

*This document was compiled from Raul's public GitHub repository, public tweets, and publicly shared screenshots from his followers. All information referenced is publicly available.*
