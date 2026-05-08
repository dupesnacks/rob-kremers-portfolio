#!/usr/bin/env python3
"""
On-demand volume checker — Get volume data for any ticker instantly.
Usage: python3 check_volume.py TSLA
"""

import sys
import yfinance as yf
from datetime import datetime, timedelta

def get_ticker_volume(ticker):
    """Get today's volume and metrics for a ticker."""
    try:
        # Fetch last 30 days of data
        data = yf.download(ticker, period='30d', progress=False)
        
        if data.empty:
            return f"❌ No data found for {ticker}"
        
        # Get metrics
        today_volume = float(data['Volume'].iloc[-1].item())
        avg_20day = float(data['Volume'].rolling(20).mean().iloc[-1].item())
        avg_5day = float(data['Volume'].rolling(5).mean().iloc[-1].item())
        
        # Today's price
        today_close = float(data['Close'].iloc[-1].item())
        price_change = float(data['Close'].iloc[-1].item()) - float(data['Close'].iloc[-2].item())
        price_pct = (price_change / float(data['Close'].iloc[-2].item())) * 100
        
        # Ratios
        ratio_to_20day = today_volume / avg_20day
        ratio_to_5day = today_volume / avg_5day
        
        # Categorize
        if ratio_to_20day > 2.5:
            category = "🔴 SPIKE (>2.5x avg)"
        elif ratio_to_20day > 1.5:
            category = "🟠 ELEVATED (>1.5x avg)"
        else:
            category = "⚪ NORMAL"
        
        # Build response
        result = f"""
╔══════════════════════════════════════════════════════════════════╗
║ {ticker} — Daily Volume Report
╚══════════════════════════════════════════════════════════════════╝

TODAY'S METRICS:
  Price:        ${today_close:.2f} ({price_pct:+.2f}%)
  Volume:       {today_volume:,.0f}
  Category:     {category}

VOLUME COMPARISON:
  vs 20-day avg:  {ratio_to_20day:.2f}x ({today_volume/avg_20day - 1:+.1%})
  vs 5-day avg:   {ratio_to_5day:.2f}x ({today_volume/avg_5day - 1:+.1%})

AVERAGES:
  20-day avg:   {avg_20day:,.0f}
  5-day avg:    {avg_5day:,.0f}

"""
        return result
        
    except Exception as e:
        return f"❌ Error fetching {ticker}: {str(e)}"


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 check_volume.py TICKER")
        print("Example: python3 check_volume.py TSLA")
        sys.exit(1)
    
    ticker = sys.argv[1].upper()
    result = get_ticker_volume(ticker)
    print(result)
