#!/bin/bash
# TVRN tweet sync & summary (runs every 30 minutes + daily summary at 22:00)

cd /Users/rk/clawd

# Fetch new tweets
python3 fetch_tvrn_incremental.py

# Re-analyze
python3 analyze_tvrn_tweets.py

# Generate daily summary (only runs at 22:00 via cron, but safe to run anytime)
if [ "$1" == "--daily" ]; then
    python3 summarize_tvrn_daily.py
fi

# Commit to git (if called with --daily)
if [ "$1" == "--daily" ]; then
    git add memory/tvrn-tweets.jsonl memory/tvrn-analysis.md memory/tvrn-daily-summary.md
    git commit -m "Daily TVRN sync + summary: $(date +%Y-%m-%d)" || true
    echo "TVRN daily sync + summary complete at $(date)"
else
    echo "TVRN 30-min sync at $(date)"
fi
