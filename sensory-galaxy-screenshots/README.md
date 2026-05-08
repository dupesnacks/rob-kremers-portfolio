# Sensory Galaxy Screenshots Tool

Frames and captions app screenshots for website display.

## Setup

```bash
npm install
npm run dev
```

Open http://localhost:3000

## Features

- **iPhone Mockup Frame**: All 6 screenshots displayed in iPhone frame
- **Text Overlays**: Edit headlines and subheadings for each screenshot
- **Multiple Layouts**: View as single column, pairs (2x3), or triplets (2 columns)
- **Export**: Download all 6 at once or individually at 1125x2436px (6.1" iPhone)

## Usage

1. Open the dev server
2. Edit headlines and subheadings for each screenshot
3. Choose layout (singles, pairs, triplets)
4. Click "Export All" to download framed screenshots
5. (Optional) Use individual "Export" buttons for selective exports

## Screenshots Included

- 0_firstimage.png
- 0_goal.png
- 1_journey.png
- 2_xp.png
- 3_dashboard.png
- 4_bridge.png

## Export Size

All exports: **1125x2436px** (6.1" iPhone size for website use, not App Store)

## Next Steps

Once exported, add images to website as follows:
- **Pairs layout**: 2 images side-by-side per row
- **Triplets layout**: 3 images per row
- **Singles layout**: Full width, stacked vertically

## Files

- `src/app/page.tsx` - Main screenshot framing app
- `public/mockup.png` - iPhone frame template
- `public/screenshots/` - App screenshots (6 total)
