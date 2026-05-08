#!/bin/bash
# Sync both TVRN and @ghostxswings tweets + analyze patterns

set -e

cd /Users/rk/clawd

echo "=== FETCHING TWEETS ==="
python3 fetch_tvrn_incremental.py
python3 fetch_ghostxswings_incremental.py

echo ""
echo "=== ANALYZING PATTERNS ==="
python3 analyze_tvrn_tweets.py
python3 analyze_ghostxswings_tweets.py

echo ""
echo "=== GENERATING DAILY RECAP ==="
python3 recap_ghostxswings_daily.py

echo ""
echo "=== SYNC COMPLETE ==="
