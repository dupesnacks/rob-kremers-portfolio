# Schwab OAuth Authentication Troubleshooting Guide

**Last Updated:** April 8, 2026  
**Issue:** Schwab API token expiration and authentication failures  
**Resolution Time:** ~45 minutes

---

## The Problem

Schwab OAuth tokens expire after **exactly 7 days** from the saved timestamp (not calendar weekly, but 7 days from `saved_at`).

**Symptoms:**
- Backend logs show: `WARNING: Schwab API not authenticated — cannot fetch [TICKER]`
- Scan returns only 1 ticker (BTC via Coinbase public API)
- `/api/schwab/status` shows `"authenticated": false, "reason": "refresh_failed"`
- All equity scans fail (240+ combos fail, only Coinbase succeeds)

---

## Root Cause Checklist

### 1. **Expired Token** (Most Common)
- Token was last authenticated 7+ days ago
- Backend tries to refresh, fails with 401 Unauthorized
- **Fix:** Re-authenticate via OAuth flow (see Solution section)

### 2. **Missing Credentials in `.env`** (Common)
- `.env` file doesn't exist or is missing `SCHWAB_APP_KEY` / `SCHWAB_APP_SECRET`
- Auth URL generated with empty `client_id`
- **Fix:** Create/update `.env` file (see `.env` Setup section)

### 3. **Wrong Environment Variable Names** (Caught Once)
- Backend expects `SCHWAB_APP_KEY` and `SCHWAB_APP_SECRET`
- (NOT `SCHWAB_CLIENT_ID` / `SCHWAB_CLIENT_SECRET`)
- **Fix:** Use correct var names in `.env` (see below)

### 4. **Redirect URI Mismatch** (Schwab Dev Console)
- Callback URL in Schwab app settings ≠ URL in backend config
- Schwab rejects redirect, login fails
- **Fix:** Update `SCHWAB_CALLBACK_URL` in `.env` to match Schwab settings

### 5. **ngrok Tunnel Offline** (If Using ngrok)
- ngrok tunnel to local backend is down
- Schwab can't reach callback endpoint
- **Fix:** Restart ngrok with `ngrok http 8001`

---

## Solution: Full Authentication Flow

### Step 1: Create `.env` File

**Location:** `/Users/rk/clawd/sma-outfits-engine/.env`

**Content:**
```
SCHWAB_APP_KEY=<your_app_key>
SCHWAB_APP_SECRET=<your_app_secret>
SCHWAB_CALLBACK_URL=<your_callback_url>
CORS_ORIGINS=http://localhost:3000,http://localhost:5173,https://www.robkremers.com
SMA_DB_PATH=sma_data.db
```

**Where to find credentials:**
- **App Key + Secret:** Schwab Developer Platform (https://developer.schwab.com) → Your App → View Details
- **Callback URL:** Schwab Developer Platform → Your App → OAuth Settings (see Step 2)

### Step 2: Determine Callback URL

You have two options:

**Option A: Using ngrok (for development)**
```bash
# In a terminal:
ngrok http 8001

# Copy the ngrok URL (e.g., https://xxxx-xxxx-xxxx.ngrok-free.dev)
# In Schwab Developer Console, set:
#   Callback URL = https://xxxx-xxxx-xxxx.ngrok-free.dev/api/schwab/callback
# In .env:
#   SCHWAB_CALLBACK_URL=https://xxxx-xxxx-xxxx.ngrok-free.dev/api/schwab/callback
```

**Option B: Direct localhost (if Schwab allows)**
```
SCHWAB_CALLBACK_URL=http://localhost:8001/api/schwab/callback
```

### Step 3: Restart Backend

```bash
pkill -9 -f "uvicorn.*8001"
sleep 2
cd /Users/rk/clawd/sma-outfits-engine/backend
/opt/homebrew/bin/uvicorn app.main:app --port 8001 --log-level error > /tmp/backend.log 2>&1 &
sleep 5
```

### Step 4: Get Auth URL

```bash
curl -s 'http://localhost:8001/api/schwab/auth' | jq -r '.auth_url'
```

### Step 5: Login & Authenticate

1. Copy the auth URL from Step 4
2. Paste in browser
3. Log in with Schwab credentials
4. Browser redirects to callback (will show success message)
5. Token is automatically saved to `/Users/rk/clawd/.schwab_token.json`

### Step 6: Verify Authentication

```bash
curl -s 'http://localhost:8001/api/schwab/status' | jq '.'
```

Expected output:
```json
{
  "authenticated": true,
  "reason": "active",
  ...
}
```

---

## Key Files & Paths

| File | Purpose |
|------|---------|
| `/Users/rk/clawd/sma-outfits-engine/.env` | Credentials (create if missing) |
| `/Users/rk/clawd/.schwab_token.json` | OAuth token (auto-created after login) |
| `/Users/rk/clawd/sma-outfits-engine/backend/app/schwab_fetcher.py` | Token refresh logic |
| `/tmp/backend.log` | Debug logs (check if auth fails) |

---

## Debug Commands

**Check current auth status:**
```bash
curl -s 'http://localhost:8001/api/schwab/status' | jq '.'
```

**View backend logs:**
```bash
tail -50 /tmp/backend.log | grep -i "schwab\|error\|auth"
```

**Check if token file exists:**
```bash
ls -la /Users/rk/clawd/.schwab_token.json
cat /Users/rk/clawd/.schwab_token.json | jq '{saved_at, access_token_expires_at}'
```

**Check .env is loaded:**
```bash
cat /Users/rk/clawd/sma-outfits-engine/.env
```

**Manually force re-auth (delete old token):**
```bash
rm /Users/rk/clawd/.schwab_token.json
# Then go through Step 5 again
```

---

## Token Lifecycle

- **Created:** When you complete OAuth login
- **Access Token:** 30 minutes (auto-refreshed by backend)
- **Refresh Token:** 7 days from `saved_at` timestamp
- **After 7 days:** Manual re-authentication required (repeat Steps 3-5)

---

## Permanent Solution (To Implement Later)

**Option 1: Cron Job for Weekly Re-Auth**
- Schedule a cron job to prompt for re-auth on day 6 of the 7-day cycle
- Set via `/api/schwab/auth` → browser → callback

**Option 2: Long-Lived Tokens**
- Investigate Schwab API for "offline_access" scope
- May allow refresh tokens to last longer

**Option 3: Environment-Specific Config**
- Production: Use service account or API key (if Schwab offers)
- Development: Current OAuth flow (manual re-auth)

---

## Testing After Fix

```bash
# Run fresh light scan
curl -s -X POST 'http://localhost:8001/api/scan?mode=light' && sleep 180

# Check results
curl -s 'http://localhost:8001/api/tickers' | jq '.[] | {rank, ticker, total}' | head -20
```

**Expected:** All 31 tickers returned, not just BTC

---

## Quick Reference Card

```bash
# If scans stop working:
1. Check status:
   curl -s 'http://localhost:8001/api/schwab/status' | jq '.'

2. If not authenticated, restart ngrok:
   pkill -f ngrok
   ngrok http 8001

3. Get new auth URL:
   curl -s 'http://localhost:8001/api/schwab/auth' | jq -r '.auth_url'

4. Click the URL in browser, login, wait for success message

5. Restart backend:
   pkill -9 -f "uvicorn.*8001"
   cd /Users/rk/clawd/sma-outfits-engine/backend
   /opt/homebrew/bin/uvicorn app.main:app --port 8001 --log-level error > /tmp/backend.log 2>&1 &

6. Test:
   curl -s -X POST 'http://localhost:8001/api/scan?mode=light' && sleep 180
   curl -s 'http://localhost:8001/api/tickers' | jq 'length'
```

---

## April 8, 2026 Resolution Example

**Problem:** Token expired (April 1 → April 8 = 7 days)

**Steps Taken:**
1. Discovered missing credentials in `.env`
2. Updated `.env` with `SCHWAB_APP_KEY` / `SCHWAB_APP_SECRET` (not CLIENT_ID)
3. Updated `SCHWAB_CALLBACK_URL` to ngrok endpoint
4. Restarted backend (forced `.env` reload)
5. Got auth URL with correct client_id
6. Completed OAuth login via ngrok callback
7. Token saved automatically
8. Ran fresh scan: ✅ All 31 tickers returned

**Time to fix:** ~45 minutes (mostly waiting for OAuth + scan completion)

---

**Remember:** Tokens expire every 7 days. Set a calendar reminder for day 6 to re-authenticate, or the next scan will fail.
