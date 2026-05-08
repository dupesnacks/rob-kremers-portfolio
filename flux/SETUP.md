# 🔐 Flux Setup Guide

## Prerequisites

- Node.js 16+
- Volvo Connected Services subscription (active on your vehicle)
- Access to Volvo Developer Portal

## Step 1: Get Your API Keys

1. Go to **https://developer.volvocars.com**
2. Sign in or create an account
3. Create a new API application
4. You'll get two API keys (Primary + Secondary)
5. Copy both into `.env.local`:

```
VITE_VCC_API_KEY=<primary_key>
VITE_VCC_API_KEY_SECONDARY=<secondary_key>
```

## Step 2: Configure OAuth

OAuth is needed for user authentication (sign in with Volvo ID).

1. In your app settings on developer.volvocars.com:
   - Click **"Edit Application"**
   - Go to **"OAuth"** or **"Authentication"** section

2. Add Redirect URI:
   ```
   http://localhost:5173/auth/callback
   ```

3. Set Required Scopes:
   - `conve:vehicle_relation` (list your vehicles)
   - `conve:vehicles_commands` (control commands like lock/unlock)

4. Copy your **Client ID** and **Client Secret** into `.env.local`:

```
VITE_VOLVO_CLIENT_ID=<your_client_id>
VITE_VOLVO_CLIENT_SECRET=<your_client_secret>
```

## Step 3: Add Your Vehicle VIN

Find your VIN:
- Driver's side door jamb
- Insurance documents
- Volvo's My Car app

Add to `.env.local`:
```
VITE_VEHICLE_VIN=YV4BR0CZ0N1808808
```

## Step 4: Run the App

```bash
npm install
npm run dev
```

Opens at **http://localhost:5173**

## Step 5: Sign In

1. Click **"Sign in with Volvo ID"**
2. You'll be redirected to Volvo's login page
3. Sign in with your Volvo ID (same as My Car app)
4. Approve the requested scopes
5. You'll be redirected back with an access token
6. Dashboard loads with live vehicle data!

---

## Troubleshooting

### "UNAUTHORIZED" error
- **Cause:** Missing or invalid OAuth token
- **Fix:** Sign in again, or manually paste token if OAuth redirect fails

### Commands not working
- **Cause:** Vehicle out of range, or command not supported
- **Fix:** Check `GET /vehicles/{vin}/commands` to see available commands

### Token expired
- The app will automatically refresh tokens when possible
- If stuck, clear localStorage and sign in again

### OAuth redirect not working
- Verify Redirect URI in developer portal matches exactly:
  - `http://localhost:5173/auth/callback` (local dev)
  - `https://yourdomain.com/auth/callback` (production)

---

## .env.local Template

Copy from `.env.example` and fill in your values:

```bash
cp .env.example .env.local
# Edit .env.local with your credentials
```

**Never commit `.env.local` to git!** (It's in `.gitignore`)

---

## Production Deployment

When deploying (Vercel, etc.):

1. Update Redirect URI in developer portal to your production domain
2. Set environment variables in deployment platform:
   - `VITE_VCC_API_KEY`
   - `VITE_VCC_API_KEY_SECONDARY`
   - `VITE_VOLVO_CLIENT_ID`
   - `VITE_VOLVO_CLIENT_SECRET`
   - `VITE_VEHICLE_VIN`

---

## API Reference

### Status Endpoints
- `GET /vehicles` — List your vehicles
- `GET /vehicles/{vin}` — Vehicle details
- `GET /vehicles/{vin}/fuel` — Battery/fuel level
- `GET /vehicles/{vin}/odometer` — Mileage
- `GET /vehicles/{vin}/statistics` — Avg speed, consumption, range
- `GET /vehicles/{vin}/doors` — Lock status
- `GET /vehicles/{vin}/engine-status` — Engine on/off
- `GET /vehicles/{vin}/diagnostics` — Service intervals, warnings

### Command Endpoints
- `POST /vehicles/{vin}/commands/lock` — Lock doors
- `POST /vehicles/{vin}/commands/unlock` — Unlock doors
- `POST /vehicles/{vin}/commands/honk` — Honk horn
- `POST /vehicles/{vin}/commands/flash` — Flash lights
- `POST /vehicles/{vin}/commands/engine-start` — Start engine (0-15 min)
- `POST /vehicles/{vin}/commands/climatization-start` — Start AC/heat

All requests require:
- Header: `vcc-api-key: <your_api_key>`
- Header: `Authorization: Bearer <access_token>`

---

**Built with React + Vite + Axios**
