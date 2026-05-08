# Schwab OAuth Token Refresh (Weekly)

**Trigger:** When Schwab token is >6 days old or expired (check `/Users/rk/clawd/.schwab_token.json` saved_at timestamp)

## Automated Steps I Execute

1. **Start Raul backend** (if not running):
   ```bash
   cd /Users/rk/clawd/raul-trading-system
   python3 -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8001
   ```

2. **Start ngrok tunnel** (if not running):
   ```bash
   ngrok http http://localhost:8001
   ```

3. **Get auth URL from backend**:
   ```bash
   curl -s "http://localhost:8001/api/schwab/auth" | jq -r '.auth_url'
   ```

4. **Provide URL to user** — single message, copyable format

## User Steps

1. Copy & paste the URL into browser
2. Log in with Schwab account
3. Grant permissions (click Allow)
4. Browser auto-redirects to ngrok callback
5. Backend automatically exchanges code for fresh token
6. Token saved to `/Users/rk/clawd/.schwab_token.json` with 7-day lifespan

## Verification

Check token refresh succeeded:
```bash
python3 << 'EOF'
import json
from datetime import datetime, timedelta

with open('/Users/rk/clawd/.schwab_token.json') as f:
    token = json.load(f)

saved_at = token['saved_at']
saved_datetime = datetime.fromtimestamp(saved_at)
expiry = saved_datetime + timedelta(days=7)
days_left = (expiry - datetime.now()).days

print(f"✅ Token fresh: Expires {expiry.strftime('%Y-%m-%d')}")
print(f"   {days_left} days remaining")
EOF
```

---

**IMPORTANT:** Don't ask "what do I do?" — just execute steps 1-4 above automatically when token is stale.
