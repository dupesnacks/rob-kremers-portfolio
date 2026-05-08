# Smart Home Dashboard - Setup Guide

## Prerequisites

- Node.js 18+ installed
- npm or yarn
- Alexa, Wyze, and Google Home accounts
- API credentials from each service

## Step 1: Clone & Install

```bash
cd /Users/rk/clawd/smart-home-dashboard

# Install backend dependencies
cd backend && npm install

# Install frontend dependencies
cd ../frontend && npm install
```

## Step 2: Environment Setup

### Backend (.env)

1. Copy the example file:
   ```bash
   cp backend/.env.example backend/.env
   ```

2. Fill in your API credentials:

   **Dashboard Security:**
   - `DASHBOARD_PASSWORD` - Set a strong password for web access

   **Alexa Smart Home API:**
   - Get credentials from [Amazon Developer Console](https://developer.amazon.com/)
   - Create a new app → OAuth credentials
   - `ALEXA_CLIENT_ID`
   - `ALEXA_CLIENT_SECRET`
   - `ALEXA_REFRESH_TOKEN` - Obtain after first OAuth flow

   **Wyze API:**
   - `WYZE_EMAIL` - Your Wyze account email
   - `WYZE_PASSWORD` - Your Wyze account password
   - `WYZE_KEY_ID` - Get from Wyze app settings
   - `WYZE_API_KEY` - Get from Wyze app settings

   **Google Nest API:**
   - Get credentials from [Google Cloud Console](https://console.cloud.google.com/)
   - Create OAuth 2.0 credentials
   - `GOOGLE_CLIENT_ID`
   - `GOOGLE_CLIENT_SECRET`
   - `GOOGLE_REFRESH_TOKEN` - Obtain after first OAuth flow

   **Roborock API:**
   - `ROBOROCK_EMAIL`
   - `ROBOROCK_PASSWORD`

## Step 3: Start Development

### Terminal 1 - Backend
```bash
cd backend
npm run dev
# Server runs on http://localhost:3001
```

### Terminal 2 - Frontend
```bash
cd frontend
npm run dev
# Dashboard runs on http://localhost:3000
```

Visit `http://localhost:3000` and enter your dashboard password.

## Step 4: Get API Credentials

### Alexa Smart Home API

1. Go to [Amazon Developer Console](https://developer.amazon.com/)
2. Create a new app (type: Smart Home)
3. Under "Configuration" → OAuth Credentials
4. Get Client ID & Secret
5. Set redirect URI: `http://localhost:3001/auth/alexa/callback` (development)
6. For production, change to: `https://robkremers.com/smart-home/auth/alexa/callback`

**To get Refresh Token:**
- Backend will guide you through OAuth flow on first run
- Or use this endpoint:
  ```bash
  curl -X GET http://localhost:3001/auth/alexa/login
  ```

### Wyze API

1. Log into your Wyze account
2. Go to Account Settings → API
3. Create an API key pair
4. Copy KEY_ID and API_KEY to `.env`

### Google Nest API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project: "Smart Home Dashboard"
3. Enable these APIs:
   - Smart Device Management API
   - Home Graph API
4. Create OAuth 2.0 Credentials (Desktop app type)
5. Download credentials JSON
6. Follow OAuth flow to get Refresh Token

### Roborock API

For Roborock, you can use:
- Direct API: Requires device token (available in app)
- Cloud API: Use email/password (simpler but rate-limited)

## Step 5: Deploy to Vercel

### 1. Prepare for Production

Backend needs to run somewhere 24/7 for automations. Options:
- **Option A:** Deploy backend to Vercel Functions (serverless) - Limited automation capability
- **Option B:** Deploy backend to Railway/Heroku (always-on) - Full automation support
- **Option C:** Run backend on local Raspberry Pi - Zero cost, full control

For this project, **Option C (Raspberry Pi) is recommended** because:
- Automations run even if dashboard is closed
- Local network access for direct device control
- No cloud dependency for critical operations

### 2. Frontend Deploy to Vercel

```bash
# In /Users/rk/clawd/smart-home-dashboard/frontend
cd frontend
npm run build
vercel deploy --prod --token $VERCEL_TOKEN
```

**Vercel Config:**
- Build Command: `npm run build`
- Output Directory: `dist`
- Environment Variables:
  - `REACT_APP_API_URL` = Your backend URL (e.g., `https://smart-home-backend.railway.app`)

### 3. Backend Deploy Options

#### Option A: Railway (Recommended for Cloud)
```bash
npm install -g railway
railway login
railway init
# Follow prompts
railway up
```

#### Option B: Raspberry Pi (Recommended for Local)
```bash
# On Raspberry Pi
git clone <your-repo>
cd smart-home-dashboard/backend
npm install
npm start
# Keep terminal open or use PM2:
npm install -g pm2
pm2 start index.js --name smart-home
pm2 save
pm2 startup
```

## Step 6: URL Structure

Once deployed:

- **Dashboard:** `https://robkremers.com/smart-home`
- **Backend API:** `https://api.smart-home.example.com` (or local: `http://192.168.1.X:3001`)
- **Siri Shortcuts:** Configure webhook to backend API

## Step 7: Siri Shortcuts

Create shortcuts that call your backend:

Example shortcut to trigger "Movie Time":
```
POST https://robkremers.com/smart-home/api/automations/trigger
Headers: Authorization: Bearer {PASSWORD}
Body: {"automationId": "movie-time"}
```

## Troubleshooting

**"Cannot connect to API"**
- Check if backend is running
- Verify API_URL environment variable
- Check CORS settings in backend

**"Devices not showing up"**
- Verify Alexa credentials
- Check backend logs: `npm run dev` to see errors
- Make sure devices are actually connected in respective apps

**"Camera streams not working"**
- Verify Wyze/Nest credentials
- Check if cameras are online in their apps
- Verify API permissions for video access

## Next Steps

1. **[Build Automations](./AUTOMATIONS.md)** - Set up time-based & conditional automations
2. **[Siri Integration](./SIRI.md)** - Configure Apple Watch voice commands
3. **[iOS App](./iOS.md)** - Build native iOS app (optional)

---

**Questions?** Check the docs/ folder for more detailed guides, or open an issue.
