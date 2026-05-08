#!/usr/bin/env python3
"""
Quick scan for BYND and SABS — aggregated summary
Usage: python3 quick_scan.py [BYND|SABS|both]
"""

import sys
from datetime import datetime
from collections import defaultdict
from backend.app.schwab_fetcher import fetch_ohlc_schwab
from backend.app.engine import detect_hits_for_ticker
from backend.app.config import OUTFITS, AFFINITIES

def quick_scan_ticker(ticker):
    """Scan a single ticker and return aggregated summary."""
    print(f"\n{'='*70}")
    print(f"{ticker} — {datetime.now().strftime('%H:%M:%S PDT')}")
    print(f"{'='*70}\n")
    
    # Get outfits for this ticker
    outfits_for_ticker = {outfit: tickers for outfit, tickers in AFFINITIES.items() if ticker in tickers}
    
    if not outfits_for_ticker:
        print(f"⚠️  {ticker} not mapped to any outfit")
        return {}
    
    print(f"Outfits: {', '.join(outfits_for_ticker.keys())}\n")
    
    # Aggregate hits by outfit
    hits_by_outfit = defaultdict(lambda: {'long': 0, 'short': 0, 'total_weight': 0, 'timeframes': set()})
    
    timeframes = ['1m', '5m', '15m', '30m', '1h', '2h', '4h', '1D']
    
    for tf in timeframes:
        ohlc = fetch_ohlc_schwab(ticker, tf)
        if ohlc is None or ohlc.empty:
            continue
        
        # Detect hits
        hits = detect_hits_for_ticker(ticker, tf, ohlc, OUTFITS)
        
        if hits:
            for hit in hits:
                outfit = hit.outfit
                hits_by_outfit[outfit]['timeframes'].add(hit.timeframe)
                hits_by_outfit[outfit]['total_weight'] += hit.weight
                if hit.side == 'long':
                    hits_by_outfit[outfit]['long'] += 1
                else:
                    hits_by_outfit[outfit]['short'] += 1
    
    if not hits_by_outfit:
        print(f"  (no signals)")
        return {}
    
    # Print summary
    for outfit in sorted(hits_by_outfit.keys()):
        data = hits_by_outfit[outfit]
        total = data['long'] + data['short']
        ratio = data['long'] / data['short'] if data['short'] > 0 else 999
        timeframes_str = ', '.join(sorted(data['timeframes']))
        
        print(f"  {outfit:20} | Hits: {total:4} (L:{data['long']:3} S:{data['short']:3}) | Weight: {data['total_weight']:7.1f} | L/S: {ratio:.2f}x | TF: {timeframes_str}")
    
    return hits_by_outfit

def main():
    tickers = ['BYND', 'SABS']
    
    if len(sys.argv) > 1:
        arg = sys.argv[1].upper()
        if arg in ['BYND', 'SABS']:
            tickers = [arg]
    
    summary = {}
    for ticker in tickers:
        summary[ticker] = quick_scan_ticker(ticker)
    
    print(f"\n{'='*70}\n")

if __name__ == '__main__':
    main()
