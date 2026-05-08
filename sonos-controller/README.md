# 🔊 Sonos Multi-Room Controller

Complete control dashboard for all your Sonos speakers from a single web interface.

## Setup

### Installation

```bash
cd /Users/rk/clawd/sonos-controller
npm install
```

### Running Locally

```bash
npm start
# Server will start on http://localhost:8002
```

## Features

✅ **Real-time Speaker Status**
- Play/Pause/Skip controls
- Current track information
- Volume control (0-100%)
- Mute/Unmute

✅ **Multi-Room Management**
- Control all 4 speakers independently
- Group/ungroup speakers (coming soon)
- Quick access to all rooms

✅ **Live Dashboard**
- Auto-refreshes every 2 seconds
- Beautiful, responsive UI
- Works on desktop, tablet, mobile

## Speakers

Your setup:
- **Kitchen** — 192.168.68.57
- **Office 1** — 192.168.68.59
- **Office 2** — 192.168.68.61
- **Office 3** — 192.168.68.63

## Architecture

**Backend** (Node.js + Express)
- `/api/speakers` — Get all speaker states
- `/api/speaker/:name/play` — Play
- `/api/speaker/:name/pause` — Pause
- `/api/speaker/:name/next` — Next track
- `/api/speaker/:name/previous` — Previous track
- `/api/speaker/:name/volume` — Set volume (0-100)
- `/api/speaker/:name/mute` — Mute
- `/api/speaker/:name/unmute` — Unmute

**Frontend** (React + Vanilla JS)
- Single-page app served from `/public`
- Auto-refreshes speaker status every 2 seconds
- Responsive grid layout

## Deployment

### Option 1: Run Locally (Recommended for now)

```bash
npm start
# Access at http://localhost:8002
```

### Option 2: Deploy to Vercel (Future)

Would require:
1. Separating backend to a serverless function or dedicated node server
2. Handling CORS for Sonos API calls
3. Potential network access issues (Sonos on local network)

For now, keep running locally since Sonos devices are on your home network (192.168.x.x range).

## Next Steps

- [ ] Add grouping/ungrouping UI
- [ ] Add favorite playlists
- [ ] Add source switching (Spotify, AirPlay, etc.)
- [ ] Add scheduling
- [ ] Discord bot integration for voice commands
- [ ] Mobile app version

## Troubleshooting

**Speakers not showing up?**
- Make sure all speakers are powered on
- Check they're on the same WiFi network
- Verify IPs are correct in `server.js`

**API errors?**
- Check speaker IP addresses
- Ensure speakers respond to network commands
- Look at server console for detailed errors

## Development

Created: 2026-03-24
Last Updated: 2026-03-24
Author: Rob Kremers
