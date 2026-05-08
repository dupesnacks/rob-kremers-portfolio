# ⚡ Flux - Volvo Vehicle Control Dashboard

Real-time Volvo vehicle monitoring and control dashboard.

## Features

- 🔋 **Live Battery/Fuel Status** — Monitor charge level in real-time
- 🗺️ **Range Tracking** — Know your remaining distance
- 📊 **Vehicle Stats** — Odometer, average speed, consumption
- 🔒 **Quick Controls**:
  - Lock/Unlock doors
  - Honk horn
  - Flash lights
  - Start/Stop engine
  - Climatization control

## Setup

### Prerequisites
- Node.js 16+ 
- Volvo Connected Vehicle API credentials (API keys)
- Your vehicle VIN

### Installation

```bash
cd flux
npm install
```

### Configuration

Environment variables are configured in `.env.local`:

```
VITE_VCC_API_KEY=your_primary_api_key
VITE_VCC_API_KEY_SECONDARY=your_secondary_api_key
VITE_VEHICLE_VIN=your_vehicle_vin
VITE_VCC_API_BASE=https://api.volvocars.com/connected-vehicle/v2
```

The `.env.local` file is already configured with your credentials.

### Running the App

```bash
npm run dev
```

Opens at `http://localhost:5173`

## API Integration

The app uses the Volvo Connected Vehicle v2 API with:
- **Authentication:** VCC API Key (in headers) + OAuth bearer token (optional)
- **Base URL:** `https://api.volvocars.com/connected-vehicle/v2`
- **Endpoints:** Vehicle info, status, diagnostics, and commands

See `src/api/volvoClient.js` for all available API methods.

## Commands Available

- `lock` / `unlock` — Control door locks
- `honk` / `flash` — Audio/visual signals
- `honkFlash` — Combined honk & flash
- `engineStart` / `engineStop` — Engine control
- `climatizationStart` / `climatizationStop` — Climate control
- All status endpoints for monitoring

## Architecture

```
src/
├── api/
│   └── volvoClient.js      # Volvo API wrapper
├── components/
│   └── Dashboard.jsx       # Main dashboard UI
├── styles/
│   └── Dashboard.css       # Styled component
└── App.jsx                 # App root
```

## Status Polling

The dashboard automatically refreshes vehicle data every 30 seconds. Use the "Refresh Now" button for immediate updates.

## Notes

- Requires active Volvo Connected Services subscription
- Some commands may require vehicle to be in specific states (e.g., parked for lock/unlock)
- API rate limits apply — excessive polling may be throttled
- All control actions are logged to browser console

## Next Steps

- [ ] OAuth2 Volvo ID login flow
- [ ] Historical data charts
- [ ] Multi-vehicle support
- [ ] Push notifications for status changes
- [ ] Mobile app version

---

Built with React + Vite + Axios
