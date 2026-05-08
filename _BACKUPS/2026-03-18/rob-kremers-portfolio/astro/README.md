# Astro Physics Trading Dashboard

A quantum-inspired algorithmic trading dashboard implementing the Astro trading system physics engine.

## Features

### Real-Time Price Data
- Live price tracking from CoinGecko API (no auth required)
- 24h, 7d price changes
- Market cap display
- Token selector (DOGE, BTC, ETH, SOL, XRP, ADA)

### Physics Engine (8D Analysis)
The dashboard calculates six core physics metrics:

1. **Energy** - Price momentum × volatility
2. **Attractor** - Phase convergence strength (cycles in alignment)
3. **Phase Accel** - Solar cycle acceleration indicator
4. **Curvature** - Cycle correlation and path bending
5. **Memory (τ)** - Historical resonance constant (0.69 base)
6. **Stress** - Volatility × stability inverse

### Celestial Cycle Analysis
Three primary cycles based on astronomical periods:

- **Metonic Cycle** (6939d → 231d): 19-year lunar-solar alignment
- **Apsidal Cycle** (3285d → 109d): 9-year orbital precession  
- **Solar Cycle** (4018d → 134d): 11-year sun activity

Combined into a smoothed 12-day moving average wave with momentum tracking.

### Trading Signals
- **BUY**: Wave > -0.2, momentum > 0, energy > 0.3
- **SELL**: Wave > 0.7 or (wave > 0.4 and momentum < -0.05)
- **HOLD**: Default state

Signals include:
- Confidence score (0-100%)
- Signal strength (0-100%)
- Risk assessment

### Risk Management
- **Risk Score** (0-100): Full risk-on (100) to full risk-off (0)
- Based on: Wave value, energy, volatility, confidence
- Risk states: STRONG RISK-OFF → NEUTRAL → HIGH RISK-ON
- Visual progress bar with color gradient

### Trade History
- Logs every signal change with:
  - Timestamp
  - Signal type (BUY/SELL/HOLD)
  - Entry price
  - Confidence level
  - Risk score
- Keeps last 20 trades for analysis

## Architecture

### Data Flow
```
CoinGecko API
    ↓
Price History (last 100 points)
    ↓
Physics Metrics Calculation
    ├─ Volatility
    ├─ Celestial cycles (sin waves)
    ├─ Energy, Attractor, Phase Accel, Curvature, Memory, Stress
    └─ Wave momentum
    ↓
Signal Generation + Risk Score
    ↓
Trade Logging + Display
```

### Calculation Formulas

**Wave Calculation:**
```
t = days since Oct 1, 2014
metonic(t) = sin(2π × t / 231)
apsidal(t) = sin(2π × t / 109)
solar(t) = sin(2π × t / 134)
wave(t) = (metonic + apsidal + solar) × 0.4143 × 0.97
```

**Physics Metrics:**
```
energy = |momentum| × volatility
attractor = 1 + volatility (if cycles align, else 0.5 + volatility)
phaseAccel = |momentum| if |solar| > 0.7, else 0
curvature = 1 + sin(2π × t / 180)
memory = 0.69 × (1 + volatility)
stress = volatility × (1 - cos(wave))
```

**Risk Score:**
```
risk = 50 + (wave × 30) + (energy × 20) - (volatility × 30) + (confidence × 0.2)
clamp(0, 100)
```

## Usage

### Token Selection
Dropdown to switch between DOGE, BTC, ETH, SOL, XRP, ADA. Each has independent price history and calculations.

### Refresh Intervals
Auto-refresh at:
- 30 seconds
- 1 minute (default)
- 5 minutes
- 15 minutes

Or click **REFRESH** for immediate update.

### Dashboard Layout
- **Top row:** Current price, risk assessment, trading signal
- **Middle:** 8D physics metrics in grid
- **Below:** Celestial cycle analysis (raw wave values)
- **Bottom:** Trade history (reverse chronological)

## Data Sources

**Price Data:**
- [CoinGecko API](https://www.coingecko.com/en/api/documentation)
- Free tier: 10-50 calls/min
- No authentication required
- Returns: price, 24h change, 7d change, market cap

**Cycle Calculations:**
- Client-side (100% local)
- Base date: October 1, 2014
- Pure sine/cosine math

**Trade History:**
- Browser localStorage (persistent across sessions)
- Last 20 trades stored
- Clears on token change

## Astro System Reference

This dashboard is inspired by @astro1062's "Signal by Noise" platform, which claims:
- 232.43% 5-year CAGR
- Sharpe ratio 3.38, Sortino 8.01
- Physics-based market analysis avoiding traditional indicators
- Markets viewed as chaotic dynamical systems with hidden structures

## Limitations

- **No live backtesting:** Dashboard shows current/recent signals only
- **No API trading:** Manual copy trading required
- **Limited historical depth:** Only stores last 100 prices
- **No advanced analytics:** CAGR/Sharpe require manual calculation
- **Cycle accuracy:** Simplified model (actual system may be more complex)

## Future Enhancements

- [ ] Historical backtesting over 1y/5y/all-time
- [ ] CAGR/Sharpe/Sortino calculations
- [ ] Multi-token portfolio view
- [ ] Alert system (email/webhook on BUY/SELL)
- [ ] Advanced charting (TradingView.Lightweight)
- [ ] CEA (Cycle Energy Alignment) metric
- [ ] LPI (Leading Phase Indicator) implementation
- [ ] API integration for auto-trading (Kraken, Coinbase, etc.)

## Deployment

**Vercel:**
```bash
vercel deploy --prod
```

Routes to: `https://robkremers.com/astro`

Configured in `vercel.json`:
```json
{ "source": "/astro", "destination": "/rob-kremers-portfolio/astro/index.html" }
```

## Development Notes

### Extending to New Tokens
1. Add token to `tokenMap` in JavaScript
2. Add option to token selector `<select>`
3. Use same token ID as CoinGecko (e.g., `dogecoin`, `bitcoin`)

### Customizing Signals
Edit `generateSignal()` function to adjust:
- Buy/sell thresholds
- Confidence weighting
- Risk score formula

### Adding Metrics
Extend `calculatePhysicsMetrics()` with new features:
- CEA (Cycle Energy Alignment)
- LPI (Leading Phase Indicator)  
- Custom entropy/phase metrics

---

**Created:** March 14, 2026  
**Status:** Beta  
**Last Updated:** $(date)
