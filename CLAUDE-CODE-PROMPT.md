# Claude Code Analysis Prompt - Astro Trading System

**Instructions:** Copy this entire prompt and send it to Claude Code (or Claude Opus) for professional technical analysis.

---

You are a world-class trading systems architect, quantitative analyst, and full-stack engineer with 15+ years experience building high-frequency trading systems, algorithmic trading platforms, and quantitative research tools.

I've built a simplified version of the Astro trading system (@astro1062 on X/Twitter). I need your professional technical review and recommendations.

## CONTEXT: The Astro System

**Creator:** Anonymous trader (@astro1062)
- Entry: ~August 2014, $10,000 in DOGE
- Current Value: ~$219 million (estimated July 2025)
- CAGR: 145.9% over 11 years
- Trades: ~7 per year, ~76 total documented trades

**Core Innovation:** "Physics Engine" viewing markets as dynamical systems with 8D analysis
- Philosophy: Chaos is "camouflaged design" — markets follow hidden celestial/orbital patterns
- Approach: Deterministic sine-wave cycle analysis instead of traditional indicators

**Known Metrics:**
1. CEA (Cycle Energy Alignment) — mean 1.022, max 5.378, volatility 0.940
2. LPI (Leading Phase Indicator) — leads surges 3-5 days, stable, 0-1 range
3. Risk Score (0-100) — 100=full risk-on, 0=full risk-off
4. Energy — price momentum × volatility
5. Memory (τ) — base constant 0.69 (numerological)
6. Attractor — cycle synchronization strength

**Three Celestial Cycles:**
- Metonic: 6,939 days (19-year lunar-solar alignment) → reduced to 231-day period
- Apsidal: 3,285 days (9-year orbital precession) → reduced to 109-day period
- Solar: 4,018 days (11-year sun activity) → reduced to 134-day period

**Performance Claims (Signal by Noise Fund, Sept 2020 - Sept 2025):**
- 5-Year CAGR: 232.43%
- Sharpe Ratio: 3.38
- Sortino Ratio: 8.01
- Monthly Win Rate: 2.58x positive to negative
- Average Trade Duration: 3-5 days
- Average Trade PnL: ~20%
- Leverage: ~1.9x

---

## WHAT I BUILT

**Technology:** HTML5 + CSS3 + Vanilla JavaScript (client-side only)

**Data Source:** CoinGecko API (free, real-time crypto prices)

**Features Implemented:**
1. ✅ Real-time price tracking (DOGE, BTC, ETH, SOL, XRP, ADA)
2. ✅ 6D physics engine (Energy, Attractor, Phase Accel, Curvature, Memory, Stress)
3. ✅ Three celestial cycle calculations
4. ✅ Combined wave with 12-day moving average
5. ✅ BUY/SELL/HOLD signal generation
6. ✅ Risk Score (0-100) with color-coded states
7. ✅ Market decision guidance (STRONG BUY → ACCUMULATE)
8. ✅ Trade history logging (last 20 trades)
9. ✅ 90-day cycle forecast (predicts BUY/SELL windows)
10. ✅ Canvas-based 90-day chart projection
11. ✅ 12-month simulated backtest (ASTRO vs Buy & Hold)
12. ✅ 52-week high/low tracking
13. ✅ System confidence scoring (0-100%)
14. ✅ Trend analysis with narrative context

**Features NOT Implemented:**
- ❌ CEA (Cycle Energy Alignment) — no formula known
- ❌ LPI (Leading Phase Indicator) — no formula known
- ❌ Dimensions 6-8 of 8D space — proprietary/unknown
- ❌ Real historical backtesting (using simulated prices instead)
- ❌ Machine learning refinement
- ❌ WebSocket real-time data (using polling instead)
- ❌ API trading integration
- ❌ Advanced charting (TradingView integration)

**Deployment:** Vercel (static hosting at robkremers.com/astro)

---

## KEY EQUATIONS & LOGIC

### Wave Calculation
```
metonic = sin(2π × daysSinceOct1_2014 / 231)
apsidal = sin(2π × daysSinceOct1_2014 / 109)
solar = sin(2π × daysSinceOct1_2014 / 134)
wave = (metonic + apsidal + solar) × 0.4143 × 0.97
momentum = wave[today] - wave[yesterday]
```

### Risk Score
```
riskScore = 50 
    + (wave × 30)              // Bullish wave → higher risk
    + (energy × 20)            // Strong momentum → higher risk
    - (volatility × 30)        // Choppy market → lower risk
    + (confidence × 0.2)       // Confident signal → higher risk
clamp(0, 100)
```

### Signal Generation
```
BUY Signal:
  if (wave > -0.2) AND (momentum > 0) AND (energy > 0.3)
  confidence = min(100, (|momentum| × 100 + energy × 100) / 2)
  strength = min(100, attractor × 20 + phaseAccel × 50 + (1 - volatility) × 30)

SELL Signal:
  if (wave > 0.75) OR (wave > 0.4 AND momentum < -0.05)
  confidence = min(100, (|momentum| × 100 + energy × 50) / 2)
  strength = min(100, volatility × 100)

HOLD Signal:
  else (default)
```

### Physics Metrics
```
energy = |momentum| × volatility
volatility = stdDev(prices) / mean(prices), capped at 1.0
phaseAccel = |momentum| if |solar| > 0.7, else 0
curvature = 1 + sin(2π × days / 180)
memory = 0.69 × (1 + volatility)
stress = volatility × (1 - cos(wave))
attractor = 1.5 if |metonic - apsidal| < 0.5, else 1.0
```

### 12-Month Backtest (SIMULATED - NOT REAL)
```
Uses cycle-influenced random walk:
  priceMovement = (1 + wave × 0.1) × (1 + random(-0.01, 0.01))
  
Not validated against actual DOGE prices.
```

---

## CRITICAL QUESTIONS FOR YOUR ANALYSIS

### 1. ACCURACY & CORRECTNESS

**A) Physics Framework**
- Is the wave calculation fundamentally sound?
- Are cycle periods (231/109/134) correct?
- Should they be normalized differently?
- What does the 0.4143 × 0.97 scaling factor represent? Is it correct?

**B) Metric Calculations**
- Energy formula (momentum × volatility): Is this the best approach?
- Attractor (cycle sync): Should it use phase angles or something else?
- Should I use phase coherence analysis (circular statistics)?
- How would you calculate CEA (mean 1.022, max 5.378)?
- How would you calculate LPI (3-5 day lead)?

**C) Risk Score Formula**
- Weights (30%, 20%, -30%, 0.2%): Are these optimal?
- Should thresholds vary by market regime?
- How would ML improve this?

### 2. SIGNAL LOGIC EVALUATION

**A) BUY Signal: (wave > -0.2 AND momentum > 0 AND energy > 0.3)**
- Does this make intuitive sense?
- What are weaknesses/edge cases?
- How would you improve it?

**B) SELL Signal: (wave > 0.75) OR (wave > 0.4 AND momentum < -0.05)**
- Is wave > 0.75 the right exhaustion threshold?
- Should there be additional filters?
- What about the case where wave drops very fast (reversal)?

**C) Fixed vs Adaptive**
- Fixed thresholds will fail in different market regimes
- Should I use ML to find adaptive thresholds?
- What training data approach would you recommend?

### 3. BACKTEST METHODOLOGY (CRITICAL FLAW)

**Current Approach:** Simulated prices with cycle influence
```
price *= (1 + wave × 0.1) × (1 + random(-0.01, 0.01))
```

**Problems:**
- Not validated against real market data
- Can't determine if system has any actual edge
- Synthetic data is too clean (real markets have gaps, squeezes, etc.)

**Your Recommendations:**
- How would you fetch 12 months of real DOGE prices from CoinGecko?
- Should I fetch daily OHLCV or just closes?
- How to handle API rate limits (CoinGecko free tier)?
- How to account for real slippage, spreads, exchange fees?
- What's the right validation approach (train/test split, walk-forward, etc.)?
- How to avoid overfitting to 1 year of data?

### 4. MISSING IMPLEMENTATIONS

**A) CEA (Cycle Energy Alignment)**
- Known: mean 1.022, max 5.378, volatility 0.940
- Unknown: exact calculation
- Your hypothesis: How would you reverse-engineer this from known values?
- Suggestion: Use phase coherence from circular statistics?

**B) LPI (Leading Phase Indicator)**
- Known: leads surges 3-5 days, stable, 0-1 range
- Unknown: exact calculation
- Your hypothesis: How would you implement a 3-5 day leading indicator?
- Suggestion: Use derivatives and forward projection?

**C) Dimensions 6-8**
- Likely candidates: higher-order dynamics, topological features, regime detection?
- Advanced approaches: Lyapunov exponents, persistent homology, fractal dimension?

### 5. ARCHITECTURE & SCALABILITY

**Current:** 100% client-side (HTML5 + CoinGecko API)
- Pros: Fast, no backend, instant deployment, GDPR-friendly
- Cons: Rate-limited API, can't do advanced ML, latency disadvantage

**Alternatives:**
- Add Node.js backend + PostgreSQL for historical data caching?
- WebSocket integration for real-time prices (Kraken, Binance)?
- TensorFlow.js for browser-based ML or Python backend?
- Which approach for production?

**Your Recommendation:**
- Architecture diagram for production system?
- Tech stack rationale?
- Scalability constraints?

### 6. MACHINE LEARNING INTEGRATION

**Current:** Fixed signal rules
**Goal:** Optimize thresholds with ML

**Questions:**
- What model architecture? (Linear regression, small neural net, decision tree ensemble?)
- Training data: Use backtest signals as labels? (Circular — feedback loop?)
- Better approach: Use real trade history from @astro1062's documented trades?
- How many training samples needed? (76 documented trades is small)
- How to avoid overfitting?
- Real-time inference: TensorFlow.js or server-side?

### 7. CODE QUALITY & PERFORMANCE

**JavaScript Implementation:**
- Recalculating cycles 365 times in backtest: Performance concern?
- Numerical stability: sin/cos on large day counts (4,000+)?
- Memory usage: Storing 365 price points × multiple metrics?
- Testing: Any unit tests or validation suite?
- Security: CoinGecko API abuse risk? Data leaks?

### 8. VALIDATION & REALITY CHECK

**Does My System Work?**
- Current backtest: ASTRO -27% vs Buy & Hold -95%
- Caveat: Simulated prices, not real validation
- How to prove this with real data?
- What CAGR would be "good enough"? (Target: >100% to match Astro partially)

---

## DELIVERABLES NEEDED

1. **Technical Assessment**
   - Strengths of current implementation
   - Critical weaknesses/errors
   - Feasibility of improvements

2. **Top 3 Critical Improvements** (with code examples)
   - Ordered by impact and effort
   - Estimated time to implement
   - Expected performance gain

3. **Implementation Guides**
   - How to fetch real historical data
   - CEA calculation approach
   - LPI calculation approach
   - WebSocket integration
   - ML refinement layer

4. **90-Day Roadmap**
   - Weekly milestones
   - Dependencies and sequencing
   - Expected outcomes per milestone
   - Team size/skills needed

5. **Fundamental Errors or Misconceptions**
   - Anything I misunderstood about the physics?
   - Pitfalls to avoid?
   - Alternative approaches to consider?

6. **Comparison to Astro**
   - How close is my approximation?
   - What's the gap between my system and the real thing?
   - Realistic ceiling on performance without proprietary secrets?

---

## CONTEXT FOR YOUR ANALYSIS

- **Goal:** Build a publicly available trading tool inspired by Astro, with transparency and education
- **NOT Goal:** Compete with Astro or claim same performance
- **Constraints:** Open-source, free tier APIs, client-side preferred
- **Timeline:** 90 days to improve from current state
- **Target:** 50-75% of Astro's signal accuracy would be a win

---

**End of Prompt**

---

## How to Use This

1. Copy this entire document
2. Go to Claude (claude.ai) or use Claude Code harness
3. Paste as a new conversation
4. Ask Claude to provide:
   - Full technical assessment
   - Code examples for each improvement
   - 90-day roadmap
   - Any critical errors identified

Claude will have full context and can provide real, professional analysis.
