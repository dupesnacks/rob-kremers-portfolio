# Astro Physics Trading Dashboard - Interpretation Guide

A practical guide to understanding what the metrics mean and how to trade on the signals.

---

## Risk Score (0-100)

The **Risk Score** is your primary decision metric. It represents how risk-on or risk-off the market condition is.

### Risk Score Ranges

| Score | State | Interpretation | Action |
|-------|-------|-----------------|--------|
| **0-20** | 🔴 STRONG RISK-OFF | Market is highly unstable, choppy, no clear direction. Volatility is high. | **AVOID ENTRIES** — Wait for stabilization. Don't FOMO. |
| **20-35** | 🟠 MODERATE RISK-OFF | Market is cautious. Cycles are misaligned. Momentum is weak. | **HOLD or SMALL POSITIONS** — Not a good entry time. |
| **35-50** | 🟡 NEUTRAL | Market is balanced. Could go either way. Wait for confirmation. | **WAIT** — Requires additional signal strength. Don't trade on this alone. |
| **50-70** | 🟢 MODERATE RISK-ON | Market has positive momentum. Cycles are aligning. Good entry conditions. | **BUY SMALL** — Decent setup. Moderate confidence. |
| **70-100** | 🟢🟢 HIGH RISK-ON | Market is hot. Strong directional bias. Cycles are highly aligned. | **AGGRESSIVE ENTRY** — Best conditions. Full position size. |

### Formula Breakdown

```
Risk Score = 50 + (wave×30) + (energy×20) - (volatility×30) + (confidence×0.2)
```

**What Each Component Does:**

- **Wave value (+30):** Positive wave = bulls winning, cycles moving up
- **Energy (+20):** High momentum in the direction of the trend
- **Volatility (-30):** High volatility = more risk, lower score (choppiness)
- **Confidence (+0.2):** When the signal is very sure, risk score rises

**Example:**
- Wave: +0.8 (very bullish) = +24
- Energy: 0.7 (high momentum) = +14
- Volatility: 0.3 (low, calm market) = -9
- Confidence: 85% = +17
- **Total: 50 + 24 + 14 - 9 + 17 = 96 (VERY HOT)**

---

## Physics Metrics (8D Analysis)

### Energy (0.0 - 2.0+)

**What it measures:** Price momentum × market volatility. How much "force" is driving the market right now.

| Level | Meaning | Signal |
|-------|---------|--------|
| **0.0-0.2** | Dead market, no movement | HOLD or WAIT |
| **0.2-0.5** | Moderate movement, building | Watch for BUY signal |
| **0.5-0.8** | Strong momentum | BUY conditions forming |
| **0.8+** | Very high momentum | Strong BUY (or SELL if wave is negative) |

**Example:** Energy 1.3 means the market has 1.3x strong directional force. Combined with a positive wave, this is excellent for entries.

---

### Attractor (0.5 - 2.0)

**What it measures:** How well the three celestial cycles are aligned (resonating together). High attractor = cycles "pulling" in the same direction.

| Level | Meaning |
|-------|---------|
| **0.5-1.0** | Cycles misaligned or chaotic | Low confidence |
| **1.0-1.5** | Cycles starting to align | Increasing confidence |
| **1.5-2.0+** | Cycles highly aligned | Strongest conditions |

**Interpretation:** When Attractor is high, the three cycles (Metonic, Apsidal, Solar) are synchronizing. This is when major moves happen. This was Astro's key insight: watch for **cycle resonance**.

---

### Phase Accel (0.0 - 1.0)

**What it measures:** Acceleration of the Solar Cycle (11-year pattern). Shows if market is shifting into a new phase.

| Level | Meaning |
|-------|---------|
| **0.0-0.1** | No phase acceleration | Steady state |
| **0.1-0.3** | Mild acceleration | Market transitioning |
| **0.3-0.5** | Strong acceleration | Phase shift in progress |
| **0.5+** | Extreme acceleration | Major regime change |

**Trading note:** Phase Accel > 0.2 combined with Energy > 0.5 = very strong reversal setup.

---

### Curvature (0.5 - 2.5)

**What it measures:** The "bend" of the price path through the cycles. How much the market is turning/curving.

| Level | Meaning |
|-------|---------|
| **0.5-1.0** | Linear movement, no curvature | Straight move (could be strong trend) |
| **1.0-1.5** | Moderate turn | Standard market behavior |
| **1.5-2.0** | High curvature | Strong turning point |
| **2.0+** | Very high curvature | Potential reversal or climax |

**Interpretation:** Curvature near 2.0 often signals a top or bottom. Use with Risk Score to time exits.

---

### Memory (τ) (0.6 - 1.0)

**What it measures:** Historical "echo" or momentum inertia. 0.69 is the base constant (numerology from Astro).

| Level | Meaning |
|-------|---------|
| **0.69** | Base resonance constant | Normal state |
| **0.69-0.80** | Weak memory, market forgetting the past | Whipsaw risk |
| **0.80-1.0** | Strong memory, trend continuing | Good for momentum trades |

**Note:** Memory rarely moves much. It's more of a long-term constant representing the 0.69 ratio Astro discovered.

---

### Stress (0.0 - 1.0)

**What it measures:** Market friction and instability. High stress = turbulent conditions.

| Level | Meaning | Action |
|-------|---------|--------|
| **0.0-0.2** | Calm, stable market | BEST for entries |
| **0.2-0.5** | Moderate tension | Good conditions |
| **0.5-0.8** | High stress, choppy | Be careful with size |
| **0.8+** | Extreme stress, chaos | AVOID or take profits |

**Example:** If Stress is 0.15 and Risk Score is 75, that's IDEAL — high risk-on in a calm market. Best setup.

---

## Celestial Cycles

The three main cycles that drive the system:

### Metonic Cycle (231 days)

**Period:** 19 years (ancient lunar-solar alignment)

**What to watch:**
- When **Metonic crosses zero** (goes from negative to positive): Start of a new lunar-solar alignment phase
- Ranges from **-1.0 to +1.0**
- **+0.5 to +1.0** = bullish phase
- **-0.5 to -1.0** = bearish phase

---

### Apsidal Cycle (109 days)

**Period:** 9 years (orbital precession)

**What to watch:**
- Fastest of the three cycles (shortest period)
- Represents **short-term directional bias**
- **+0.7 to +1.0** = strong uptrend
- **-0.7 to -1.0** = strong downtrend

---

### Solar Cycle (134 days)

**Period:** 11 years (sun activity)

**What to watch:**
- **Medium-term cycle** (between Metonic and Apsidal)
- Often the "deciding vote" when other cycles conflict
- **Extreme values (+/- 0.9+)** = Phase Accel spike (reversal coming)

---

### Combined Wave (the key metric)

The three cycles combined and smoothed to a 12-day moving average.

**Wave Values & Trading:**

| Wave Value | State | Signal |
|------------|-------|--------|
| **< -0.5** | Deep bearish | SELL or HOLD SHORT |
| **-0.5 to -0.2** | Bearish | HOLD (no entry) |
| **-0.2 to +0.2** | Neutral zone | WAIT for signal |
| **+0.2 to +0.5** | Bullish building | Start looking for BUY |
| **+0.5 to +0.7** | Strong bull | BUY |
| **> +0.7** | Extreme bull (potential top) | SELL or TAKE PROFITS |

**The Critical Rule:**
- Wave **crosses from negative to positive** = **PRIME BUY ZONE**
- Wave **crosses from positive to negative** = **PRIME SELL ZONE**
- Watch for **Wave Momentum** (derivative) to confirm

---

## Trading Signal Reference

### BUY Signal

**Conditions (all must be true):**
1. Wave > -0.2 (not in deep bearish territory)
2. Momentum > 0 (wave is moving upward)
3. Energy > 0.3 (enough force behind it)

**Best conditions:**
- Wave > +0.2 (clearly bullish)
- Momentum > +0.1 (strong upward acceleration)
- Energy > 0.7 (tons of momentum)
- Attractor > 1.4 (cycles aligned)
- Stress < 0.3 (calm market)
- **Risk Score > 65**

**Confidence High when:**
- All physics metrics are positive
- Multiple cycles at +0.6 or higher
- Stress is low
- Signal strength > 60%

---

### SELL Signal

**Conditions (either one):**
1. Wave > +0.7 (potential exhaustion/top)
2. Wave > +0.4 AND Momentum < -0.05 (rolling over from uptrend)

**Best conditions:**
- Wave exactly at +0.7 to +0.9 (exhaustion zone)
- Momentum has turned sharply negative
- Curvature > 1.8 (strong turning point)
- Stress rising (instability)
- **Risk Score < 40** (flipping to risk-off)

**Confidence High when:**
- Wave is at +0.8+ (extreme overbought)
- All momentum indicators rolling over
- Attractor dropping fast (cycles desynchronizing)
- Signal strength > 70%

---

### HOLD Signal (Default)

**Conditions:**
- Wave is in neutral zone (-0.2 to +0.2), OR
- Energy is too low to trade on, OR
- Risk Score is 35-50 (undefined direction)

**What to do:**
- Sit in cash
- Set alerts for BUY/SELL conditions
- Don't FOMO enter
- Wait for clear signal

---

## Trading Strategy Examples

### Example 1: Perfect Buy Setup (Risk Score 78)

```
Wave: +0.35 (bullish)
Momentum: +0.08 (rising)
Energy: 0.72 (strong)
Attractor: 1.6 (cycles aligned)
Stress: 0.12 (very calm)
Risk Score: 78

Signal: BUY ✅
Action: ENTER with full position size
Stop Loss: Below previous local low
Take Profit: Hold for 3-5 days or until Wave > +0.7
```

### Example 2: Questionable Setup (Risk Score 38)

```
Wave: +0.15 (slightly bullish but weak)
Momentum: +0.02 (barely moving up)
Energy: 0.25 (low momentum)
Attractor: 1.1 (barely aligned)
Stress: 0.6 (choppy)
Risk Score: 38

Signal: HOLD (possibly weak BUY)
Action: WAIT — Not enough confluenc. Only enter if you want to scalp small
Reason: Too much uncertainty, risk score still low
```

### Example 3: Perfect Sell Setup (Risk Score 25)

```
Wave: +0.82 (overbought)
Momentum: -0.12 (rolling over hard)
Energy: 0.15 (momentum dying)
Attractor: 0.9 (cycles desynchronizing)
Stress: 0.78 (market getting choppy)
Risk Score: 25

Signal: SELL ✅
Action: EXIT long positions or ENTER short
Stop Loss: Above wave peak at +0.9
Take Profit: Target wave -0.2 or lower
Hold Time: 1-3 days typical
```

---

## Quick Reference Checklist

### ✅ STRONG BUY CONDITIONS
- [ ] Risk Score > 70
- [ ] Wave > +0.2 and rising
- [ ] Energy > 0.6
- [ ] Attractor > 1.5
- [ ] Stress < 0.3
- [ ] Signal Strength > 60%

### ✅ STRONG SELL CONDITIONS
- [ ] Risk Score < 30
- [ ] Wave > +0.7 or turning negative
- [ ] Momentum < -0.05
- [ ] Curvature > 1.7
- [ ] Stress > 0.5
- [ ] Signal Strength > 70%

### ⚠️ CAUTION (Don't Trade)
- [ ] Risk Score 35-50 (neutral)
- [ ] Energy < 0.3 (no momentum)
- [ ] Stress > 0.8 (too chaotic)
- [ ] Attractor < 1.0 (cycles misaligned)
- [ ] Signal Strength < 40% (low confidence)

---

## Common Mistakes to Avoid

1. **Trading on HOLD signals** — Risk Score 35-50 is dangerous. Wait.
2. **Ignoring Stress** — High stress (>0.7) makes all signals unreliable.
3. **Not watching Wave Momentum** — Wave value alone isn't enough; momentum confirms.
4. **Over-trading at Wave extremes** — Wave +0.9 or -0.9 is reversal risk, not continuation.
5. **Treating Risk Score as gospel** — It's one metric. Check all 6 physics metrics.
6. **Ignoring cycle desynchronization** — When Attractor drops, get out. Cycles are about to realign.

---

## Historical Astro Performance

For context, the actual Astro/Signal by Noise system claims:
- **232.43% 5-year CAGR** (Sept 2020 - Sept 2025)
- **Sharpe Ratio: 3.38** (excellent)
- **Sortino Ratio: 8.01** (very few bad trades)
- **Monthly win rate: 2.58x positive to negative**
- **Average trade duration: 3-5 days** (short-term)

This dashboard is a simplified model, so results will differ. Use it for education and as a **confirmation tool**, not as a guaranteed trading system.

---

## Tips for Best Results

1. **Start small** — Trade 1-2% of portfolio per signal
2. **Track your trades** — Log entry/exit and compare to risk score
3. **Look for confluence** — Best trades have 5+ of the 6 metrics in agreement
4. **Watch cycle crossovers** — Metonic/Apsidal/Solar crossing zero = major moves
5. **Use Stress as a filter** — Skip trades when Stress > 0.6
6. **Trade the direction of the highest cycle** — Metonic sets long-term bias
7. **Short holds, take profits early** — This is a 3-5 day system, not a hodl strategy

---

## Dashboard Update Frequency

By default, the dashboard refreshes every **1 minute** (configurable):
- 30 seconds (very active, lots of noise)
- 1 minute (balanced)
- 5 minutes (calmer, less whipsaw)
- 15 minutes (very conservative)

For swing trading (3-5 day holds), **5-minute refresh is best**. Reduces false signals.

---

**Last Updated:** March 14, 2026  
**Dashboard Version:** Beta 1.0  
**Data Source:** CoinGecko API (real-time)
