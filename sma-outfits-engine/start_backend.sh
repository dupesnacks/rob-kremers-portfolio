#!/bin/bash
cd /Users/rk/clawd/sma-outfits-engine
source .env
exec python3 -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
