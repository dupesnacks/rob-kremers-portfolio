# Volume Monitor — MVP

Tracks volume anomalies for configured tickers and sends Discord alerts when thresholds are breached.

## Setup

### 1. Configure Discord Webhook

1. Open your Discord server
2. Navigate to the channel where you want alerts
3. Click the settings icon (⚙️) → **Edit Channel**
4. Go to **Integrations** → **Webhooks**
5. Click **New Webhook**
6. Name it "Volume Monitor"
7. Copy the webhook URL
8. Paste into `.env`:

```bash
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_WEBHOOK_TOKEN
```

### 2. Run Manually

```bash
cd /Users/rk/clawd/volume-monitor
python3 volume_monitor.py
```

### 3. Schedule Daily (After Market Close)

Add to crontab:

```bash
crontab -e
```

Add this line (runs at 4:30 PM PDT on weekdays):

```
30 16 * * 1-5 cd /Users/rk/clawd/volume-monitor && python3 volume_monitor.py
```

For different timezone, adjust hours:
- 16:30 PDT = 19:30 EDT = 23:30 UTC

## Watchlist Management

Edit the `WATCHLIST` at line 35 in `volume_monitor.py`:

```python
WATCHLIST = [
    'TSLA',
    'BYND',
    'GME',
    'NVDA',
    'AAPL',
    'BTC-USD',
    'DOGE-USD',
]
```

Or just tell me: "Add GME to the WATCHLIST" and I'll handle it.

## Signal Types

- **SPIKE** 🔴 — Volume > 2.5× 20-day average (critical)
- **ELEVATED** 🟠 — Volume > 1.5× 20-day average
- **TREND** 🟡 — 7-day rolling avg up 20%+ vs prior 7 days (accumulation pattern)
- **ACCUMULATION** 🟢 — 3+ consecutive days above elevated threshold

## Dependencies

```bash
pip install yfinance python-dotenv requests
```

## Data Sources

- **Stocks (TSLA, GME, NVDA, etc.):** Yahoo Finance via yfinance
- **Crypto (BTC-USD, DOGE-USD):** Yahoo Finance via yfinance
