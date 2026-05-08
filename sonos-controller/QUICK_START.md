# 🔊 Quick Start — Sonos Controller

## Start the Server

```bash
cd /Users/rk/clawd/sonos-controller
npm start
```

Server will run on: **http://localhost:8002**

## Open the Dashboard

```
http://localhost:8002
```

You'll see 4 speaker cards:
- **Kitchen** (192.168.68.57)
- **Office 1** (192.168.68.59)
- **Office 2** (192.168.68.61)
- **Office 3** (192.168.68.63)

## Control Your Speakers

Each speaker card has:
- **Play/Pause button** — Start/stop playback
- **Skip buttons** — Previous/Next track
- **Volume slider** — 0-100% with live feedback
- **Mute button** — Quick mute/unmute
- **Track display** — Current song name
- **Status badge** — Playing/Paused/Error

## Dashboard Features

✅ Real-time updates (every 2 seconds)
✅ Works on phone, tablet, desktop
✅ One-click controls
✅ No configuration needed
✅ Beautiful gradient UI

## API Reference

### Get All Speakers

```bash
curl http://localhost:8002/api/speakers
```

Response:
```json
{
  "kitchen": {
    "name": "Kitchen",
    "ip": "192.168.68.57",
    "state": "playing",
    "track": { "title": "Song Name" },
    "volume": 50,
    "mute": false,
    "playing": true
  },
  ...
}
```

### Play a Speaker

```bash
curl -X POST http://localhost:8002/api/speaker/kitchen/play
```

### Pause a Speaker

```bash
curl -X POST http://localhost:8002/api/speaker/kitchen/pause
```

### Skip Next Track

```bash
curl -X POST http://localhost:8002/api/speaker/kitchen/next
```

### Skip Previous Track

```bash
curl -X POST http://localhost:8002/api/speaker/kitchen/previous
```

### Set Volume (0-100)

```bash
curl -X POST http://localhost:8002/api/speaker/kitchen/volume \
  -H "Content-Type: application/json" \
  -d '{"volume": 50}'
```

### Mute

```bash
curl -X POST http://localhost:8002/api/speaker/kitchen/mute
```

### Unmute

```bash
curl -X POST http://localhost:8002/api/speaker/kitchen/unmute
```

## Speaker Names for API

Use these in API calls:
- `kitchen` — Kitchen speaker
- `office1` — Office speaker 1
- `office2` — Office speaker 2
- `office3` — Office speaker 3

## Troubleshooting

**Speakers not showing up?**
- Make sure they're powered on
- Check they're connected to WiFi
- Verify IPs haven't changed (static is best)

**Volume/playback not responding?**
- Check speaker is online
- Try refreshing the page
- Look at server logs for errors

**Dashboard looks broken?**
- Hard refresh (Cmd+Shift+R on Mac)
- Clear browser cache
- Check console for JS errors

## Future Features

Coming soon:
- Group/ungroup speakers
- Favorite playlists
- Source switching (Spotify, AirPlay, etc.)
- Scheduling & automation
- Discord bot commands
- Mobile app

## Architecture

```
Frontend (React @ localhost:8002)
    ↓ (REST API calls)
Backend (Node.js @ localhost:8002)
    ↓ (UPnP/SOAP)
Sonos Speakers (local network)
```

---

**Created:** March 24, 2026
**Status:** ✅ Live & Working
**Support:** Check README.md for detailed setup
