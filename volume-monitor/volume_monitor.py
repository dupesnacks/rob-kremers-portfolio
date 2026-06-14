#!/usr/bin/env python3
"""
Volume Monitor MVP
Tracks volume anomalies for configured tickers and alerts via Discord webhook.
Detects: SPIKE, ELEVATED, TREND, ACCUMULATION patterns.

ENHANCED: Weekly/monthly volume+price recaps (raw numbers only, no prose).
"""

import os
import json
import requests
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv
import yfinance as yf
import pandas as pd

# Load environment variables
load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')
if not DISCORD_WEBHOOK_URL:
    raise ValueError("DISCORD_WEBHOOK_URL not set in .env")

# ==================== WATCHLIST ====================
# Add/remove tickers here (one per line)
WATCHLIST = [
    'BYND',
    'SABS',
    'GME',
    'AMC',
    'BTC-USD',
    'DOGE-USD',
    'IBM',
    'PLTR',
    'LFVN',
    'IPW',
    'TSLA',
    'TSLL',
    'SPCX',
    'PLCE',
    'INTC',
]
# ===================================================

# Volume thresholds
SPIKE_THRESHOLD = 2.5  # 2.5x 20-day average
ELEVATED_THRESHOLD = 1.5  # 1.5x 20-day average
TREND_THRESHOLD = 0.20  # 20% increase in 7-day rolling avg
ACCUMULATION_DAYS = 3  # 3+ consecutive days above elevated

# Crypto tickers (trade 7 days/week)
CRYPTO_TICKERS = ['BTC-USD', 'DOGE-USD']


def fetch_volume_data(ticker, days=180):
    """Fetch historical OHLCV data for ticker (extended window for weekly/monthly)."""
    try:
        data = yf.download(ticker, period=f'{days}d', progress=False)
        if data.empty:
            return None
        return data[['Open', 'High', 'Low', 'Close', 'Volume']].copy()
    except Exception as e:
        print(f"Error fetching {ticker}: {str(e)}")
        return None


def calculate_volume_metrics(volume_data):
    """Calculate daily volume metrics (SPIKE, ELEVATED, TREND, ACCUMULATION)."""
    if volume_data is None or len(volume_data) < 3:
        return None
    
    today_volume = float(volume_data['Volume'].iloc[-1].item())
    avg_20day = float(volume_data['Volume'].rolling(20).mean().iloc[-1].item())
    
    # 7-day rolling averages
    vol_7day_avg = float(volume_data['Volume'].rolling(7).mean().iloc[-1].item())
    vol_7day_prev_val = volume_data['Volume'].rolling(7).mean().iloc[-8].item()
    vol_7day_prev = float(vol_7day_prev_val) if not (isinstance(vol_7day_prev_val, float) and vol_7day_prev_val != vol_7day_prev_val) else None
    
    # Check accumulation (3+ days above elevated)
    recent_volumes = volume_data['Volume'].tail(7)
    elevated_days = int((recent_volumes > (avg_20day * ELEVATED_THRESHOLD)).sum().item())
    
    return {
        'today': today_volume,
        'avg_20day': avg_20day,
        'vol_7day': vol_7day_avg,
        'vol_7day_prev': vol_7day_prev,
        'elevated_days': elevated_days,
    }


def calculate_weekly_metrics(data, ticker):
    """
    Calculate weekly volume and price metrics.
    For crypto: use last 7 calendar days.
    For stocks: use last 5 trading days (Mon-Fri).
    """
    if data is None or len(data) < 5:
        return {'has_data': False, 'reason': 'insufficient_history'}
    
    try:
        # Determine number of days for "this week"
        if ticker in CRYPTO_TICKERS:
            # Crypto trades 7 days — use last 7 calendar days
            this_week_data = data.tail(7)
            weeks_back_for_avg = 28  # 4 weeks × 7 days
        else:
            # Stock trading — use last 5 trading days
            this_week_data = data.tail(5)
            weeks_back_for_avg = 20  # 4 weeks × 5 trading days
        
        if len(this_week_data) < 5:
            return {'has_data': False, 'reason': 'insufficient_history'}
        
        # This week's metrics
        volume_this_week = float(this_week_data['Volume'].sum().item())
        price_start = float(this_week_data['Open'].iloc[0].item())
        price_end = float(this_week_data['Close'].iloc[-1].item())
        price_change_pct = ((price_end - price_start) / price_start) * 100 if price_start != 0 else 0
        
        # 4-week average baseline
        baseline_data = data.iloc[-(weeks_back_for_avg + len(this_week_data)):-len(this_week_data)]
        if len(baseline_data) < weeks_back_for_avg:
            return {'has_data': False, 'reason': 'insufficient_history'}
        
        volume_4week_avg = float(baseline_data['Volume'].sum().item() / 4)  # Average of 4 weeks
        volume_change_pct = ((volume_this_week - volume_4week_avg) / volume_4week_avg) * 100 if volume_4week_avg != 0 else 0
        
        return {
            'has_data': True,
            'volume_this_week': round(volume_this_week),
            'volume_4week_avg': round(volume_4week_avg),
            'volume_change_pct': round(volume_change_pct, 2),
            'price_start': round(price_start, 2),
            'price_end': round(price_end, 2),
            'price_change_pct': round(price_change_pct, 2),
        }
    except Exception as e:
        return {'has_data': False, 'reason': f'error: {str(e)}'}


def calculate_monthly_metrics(data, ticker):
    """
    Calculate monthly volume and price metrics.
    Uses calendar month boundaries.
    """
    if data is None or len(data) < 20:
        return {'has_data': False, 'reason': 'insufficient_history'}
    
    try:
        # Get current month boundaries
        today = data.index[-1]
        month_start = pd.Timestamp(year=today.year, month=today.month, day=1)
        
        # This month's data
        this_month_data = data[data.index >= month_start]
        if len(this_month_data) < 1:
            return {'has_data': False, 'reason': 'insufficient_history'}
        
        volume_this_month = float(this_month_data['Volume'].sum().item())
        price_start = float(this_month_data['Open'].iloc[0].item())
        price_end = float(this_month_data['Close'].iloc[-1].item())
        price_change_pct = ((price_end - price_start) / price_start) * 100 if price_start != 0 else 0
        
        # 3-month average baseline (previous 3 months)
        three_months_ago = month_start - pd.DateOffset(months=3)
        baseline_data = data[(data.index >= three_months_ago) & (data.index < month_start)]
        
        if len(baseline_data) < 40:  # At least ~40 trading days
            return {'has_data': False, 'reason': 'insufficient_history'}
        
        volume_3month_avg = float(baseline_data['Volume'].sum().item() / 3)  # Average of 3 months
        volume_change_pct = ((volume_this_month - volume_3month_avg) / volume_3month_avg) * 100 if volume_3month_avg != 0 else 0
        
        return {
            'has_data': True,
            'volume_this_month': round(volume_this_month),
            'volume_3month_avg': round(volume_3month_avg),
            'volume_change_pct': round(volume_change_pct, 2),
            'price_start': round(price_start, 2),
            'price_end': round(price_end, 2),
            'price_change_pct': round(price_change_pct, 2),
        }
    except Exception as e:
        return {'has_data': False, 'reason': f'error: {str(e)}'}


def detect_signals(ticker, metrics):
    """Detect volume signals."""
    if metrics is None:
        return []
    
    signals = []
    today = metrics['today']
    avg_20 = metrics['avg_20day']
    vol_7_curr = metrics['vol_7day']
    vol_7_prev = metrics['vol_7day_prev']
    elevated_days = metrics['elevated_days']
    
    # SPIKE
    if today > (avg_20 * SPIKE_THRESHOLD):
        ratio = today / avg_20
        signals.append({
            'type': 'SPIKE',
            'severity': '🔴',
            'message': f"{ticker}: {ratio:.2f}x volume spike (today: {today:,.0f}, 20d avg: {avg_20:,.0f})",
        })
    
    # ELEVATED
    elif today > (avg_20 * ELEVATED_THRESHOLD):
        ratio = today / avg_20
        signals.append({
            'type': 'ELEVATED',
            'severity': '🟠',
            'message': f"{ticker}: {ratio:.2f}x elevated volume (today: {today:,.0f}, 20d avg: {avg_20:,.0f})",
        })
    
    # TREND (7-day accumulation trend)
    if vol_7_prev and vol_7_prev > 0:
        trend_pct = ((vol_7_curr - vol_7_prev) / vol_7_prev) * 100
        if trend_pct >= (TREND_THRESHOLD * 100):
            signals.append({
                'type': 'TREND',
                'severity': '🟡',
                'message': f"{ticker}: {trend_pct:.1f}% volume trend increase over 7 days",
            })
    
    # ACCUMULATION (3+ consecutive elevated days)
    if elevated_days >= ACCUMULATION_DAYS:
        signals.append({
            'type': 'ACCUMULATION',
            'severity': '🟢',
            'message': f"{ticker}: {elevated_days} consecutive days of elevated volume",
        })
    
    return signals


def send_discord_alert(signals_by_ticker):
    """Send consolidated alert to Discord webhook."""
    if not signals_by_ticker:
        return
    
    # Build embed
    embed = {
        'title': '📊 Volume Monitor — Daily Summary',
        'color': 0xFF6B6B,  # Red
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'fields': [],
    }
    
    for ticker, signals in signals_by_ticker.items():
        for signal in signals:
            embed['fields'].append({
                'name': f"{signal['severity']} {signal['type']}",
                'value': signal['message'],
                'inline': False,
            })
    
    payload = {
        'username': 'Volume Monitor — Daily Summary',
        'avatar_url': 'https://cdn-icons-png.flaticon.com/512/3050/3050159.png',
        'embeds': [embed],
    }
    
    try:
        resp = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
        resp.raise_for_status()
        print(f"✅ Discord alert sent ({len(signals_by_ticker)} tickers)")
    except Exception as e:
        print(f"❌ Discord alert failed: {str(e)}")


def main():
    """Run volume monitor scan."""
    print(f"\n{'='*70}")
    print(f"Volume Monitor Scan — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*70}\n")
    
    signals_by_ticker = {}
    volume_data_output = []
    
    for ticker in WATCHLIST:
        print(f"Scanning {ticker}...", end=' ', flush=True)
        
        # Fetch 180 days of data
        ohlcv_data = fetch_volume_data(ticker, days=180)
        
        if ohlcv_data is None:
            print("❌ No data")
            volume_data_output.append({'ticker': ticker, 'error': 'no_data'})
            continue
        
        # Daily metrics
        metrics = calculate_volume_metrics(ohlcv_data)
        if metrics is None:
            print("❌ Insufficient data")
            volume_data_output.append({'ticker': ticker, 'error': 'insufficient_data'})
            continue
        
        # Detect daily signals
        signals = detect_signals(ticker, metrics)
        
        # Weekly metrics
        weekly = calculate_weekly_metrics(ohlcv_data, ticker)
        
        # Monthly metrics
        monthly = calculate_monthly_metrics(ohlcv_data, ticker)
        
        # Build ticker data block
        ticker_block = {
            'ticker': ticker,
            'daily': {
                'today_volume': round(metrics['today']),
                'avg_20day': round(metrics['avg_20day']),
            },
            'weekly': weekly,
            'monthly': monthly,
        }
        volume_data_output.append(ticker_block)
        
        if signals:
            print(f"✅ {len(signals)} signal(s) + weekly/monthly")
            signals_by_ticker[ticker] = signals
            for sig in signals:
                print(f"   {sig['severity']} {sig['type']}: {sig['message']}")
        else:
            print("✅ weekly/monthly logged")
    
    print(f"\n{'='*70}\n")
    
    # Write volume_data.json
    json_path = Path(__file__).parent / 'volume_data.json'
    with open(json_path, 'w') as f:
        json.dump(volume_data_output, f, indent=2)
    print(f"✅ Wrote {len(volume_data_output)} tickers to volume_data.json")
    
    # Send alerts
    if signals_by_ticker:
        send_discord_alert(signals_by_ticker)
    else:
        print("No signals detected across watchlist.")


if __name__ == '__main__':
    main()
