#!/bin/bash
# Update volume_data.json and deploy to robkremers.com via Vercel

set -e

# Generate fresh volume data
cd /Users/rk/clawd/raul-trading-system
python3 volume_monitor.py

# Copy to robkremers.com repository
cp volume_data.json /Users/rk/clawd/volume_data.json

# Deploy via git push (Vercel auto-deploys)
cd /Users/rk/clawd
git add volume_data.json
git commit -m "Daily volume update — $(date '+%Y-%m-%d %H:%M')"
git push origin main

echo "✅ Volume dashboard updated and deployed"
