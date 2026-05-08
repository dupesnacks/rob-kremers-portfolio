#!/usr/bin/env python3
"""
Volume Monitor Pulse — Intraday scanning (every 3 hours during market hours)
Same signals as daily, but labeled as "PULSE" for real-time tracking.
"""

import os
import json
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import yfinance as yf

# Load environment variables
load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')
if not DISCORD_WEBHOOK_URL:
    raise ValueError("DISCORD_WEBHOOK_URL not set in .env")

# ==================== WATCHLIST ====================
WATCHLIST = [
    'BYND',
    'SABS',
    'GME',
    'AMC',
    'BTC-USD',
    'DOGE-USD',
]
# ===================================================

# Volume thresholds (same as daily)
SPIKE_THRESHOLD = 2.5
ELEVATED_THRESHOLD = 1.5
TREND_THRESHOLD = 0.20
ACCUMULATION_DAYS = 3


def fetch_volume_data(ticker, days=30):
    """Fetch historical volume data for ticker."""
    try:
        data = yf.download(ticker, period=f'{days}d', progress=False)
        if data.empty:
            return None
        return data[['Volume']].copy()
    except Exception as e:
        print(f"Error fetching {ticker}: {str(e)}")
        return None


def calculate_volume_metrics(volume_data):
    """Calculate volume metrics."""
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


def send_discord_alert(signals_by_ticker, pulse_type='PULSE'):
    """Send consolidated alert to Discord webhook."""
    if not signals_by_ticker:
        return
    
    # Build embed
    embed = {
        'title': f'📊 Volume {pulse_type}',
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
        'username': f'Volume Monitor — {pulse_type}',
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
    """Run volume monitor pulse."""
    now = datetime.now()
    print(f"\n{'='*70}")
    print(f"Volume Monitor Pulse — {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*70}\n")
    
    signals_by_ticker = {}
    
    for ticker in WATCHLIST:
        print(f"Scanning {ticker}...", end=' ')
        volume_data = fetch_volume_data(ticker, days=30)
        
        if volume_data is None:
            print("❌ No data")
            continue
        
        metrics = calculate_volume_metrics(volume_data)
        if metrics is None:
            print("❌ Insufficient data")
            continue
        
        signals = detect_signals(ticker, metrics)
        
        if signals:
            print(f"✅ {len(signals)} signal(s)")
            signals_by_ticker[ticker] = signals
            for sig in signals:
                print(f"   {sig['severity']} {sig['type']}: {sig['message']}")
        else:
            print("—")
    
    print(f"\n{'='*70}\n")
    
    # Send alerts
    if signals_by_ticker:
        send_discord_alert(signals_by_ticker, pulse_type='PULSE')
    else:
        print("No signals detected across watchlist.")


if __name__ == '__main__':
    main()
