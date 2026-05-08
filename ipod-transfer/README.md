# iPod Transfer — Setup & Usage Guide

A Windows 11 desktop app for transferring photos and videos between your
PC and iPod Touch (iOS 3.1.3 / PA627LL).

---

## What This Does

| Feature                        | Supported? | Notes                                      |
|-------------------------------|------------|--------------------------------------------|
| Download photos from iPod     | ✅ Yes      | Via WIA (Windows Image Acquisition)        |
| Upload photos to iPod         | ⚠️ Limited  | iOS 3.x blocks WIA upload; use iTunes      |
| View photo thumbnails         | ✅ Yes      | Grid view with checkboxes                  |
| Batch download                | ✅ Yes      | Select all or pick individual files        |
| Device info display           | ✅ Yes      | Requires libimobiledevice (optional)       |
| Music sync                    | ❌ No       | iTunes-only on iOS 3.x (see below)         |

---

## Requirements

1. **Windows 11** (also works on Windows 10)
2. **iTunes 10.7** — Required for:
   - Apple Mobile Device Support drivers (USB detection)
   - Music sync
   - Sending photos TO the device
   
   Download: https://support.apple.com/downloads/itunes
   
   > ⚠️ Use iTunes 10.7 specifically — newer iTunes versions dropped
   > support for iOS 3.x devices.

3. **libimobiledevice** (optional, for device name/serial/info panel)
   - Download the Windows build from:
     https://github.com/libimobiledevice-win32/imobiledevice-net/releases
   - Extract and copy these files into an `imobiledevice\` folder next
     to `iPodTransfer.exe`:
     - `ideviceinfo.exe`
     - `idevicepair.exe`
     - All accompanying `.dll` files

---

## Build Instructions

### Step 1 — Install Python
Download Python 3.11+ from https://python.org
During install: ✅ check **"Add Python to PATH"**

### Step 2 — Install iTunes 10.7
This installs the Apple Mobile Device USB drivers needed for WIA.

### Step 3 — Build the .exe
1. Open **Command Prompt** in this folder
2. Run: `build.bat`
3. When complete, find `iPodTransfer.exe` in the `dist\` folder

### Step 4 — (Optional) Add libimobiledevice
Place the tools in `dist\imobiledevice\` for full device info support.

---

## Using the App

### Downloading Photos from your iPod

1. Connect your iPod Touch via USB
2. **Unlock** the device and tap **"Trust"** when prompted
3. Launch `iPodTransfer.exe`
4. Go to **Photos & Videos** tab
5. Click **⟳ Refresh** — your photos will appear as a grid
6. Check the boxes on items you want, then click **⬇ Download Selected**
7. Files save to your chosen folder (default: `Pictures\iPod`)

### Sending Photos to your iPod

Direct photo upload to iOS 3.x is not supported by Windows WIA.

**Use iTunes instead:**
1. Open iTunes 10.7
2. Connect your iPod → click its icon
3. Click the **Photos** tab in the left panel
4. Check **"Sync Photos from"** and choose your folder
5. Click **Sync**

### Pairing / Trust Issues

If the device isn't detected:
1. Click the **Pair** button in the top-right
2. Look at your iPod — tap **"Trust This Computer"**
3. iTunes must be installed for the drivers to work

---

## Music Sync

Music sync on iOS 3.1.3 is handled exclusively by iTunes. There is no
open-source protocol that can write to the iOS media library on this
firmware version.

**iTunes 10.7 music sync:**
1. Open iTunes → connect device
2. Click **Music** tab in device settings
3. Choose **Sync Music** → pick playlists or "Entire library"
4. Click **Apply**

---

## Troubleshooting

| Problem                            | Fix                                                   |
|------------------------------------|-------------------------------------------------------|
| "No device detected"               | Unlock iPod, tap Trust, restart iTunes                |
| Photos tab shows nothing           | Make sure device is unlocked and on home screen       |
| WIA error on refresh               | Restart Apple Mobile Device Service in Services.msc   |
| Build fails with pywin32 error     | Run: `pip install pywin32 --upgrade`                  |
| .exe crashes on launch             | Run from cmd.exe to see error message                 |

---

## Technical Notes

- **Photo access** uses Windows Image Acquisition (WIA) — the same
  protocol Windows uses for scanners and cameras. iOS 3.x devices
  expose a PTP/MTP camera interface over USB when unlocked.
  
- **Device info** (name, iOS version, serial) uses libimobiledevice,
  an open-source library that speaks Apple's proprietary USB protocol.
  
- **Music** uses Apple's AFC (Apple File Conduit) protocol, which is
  only accessible via iTunes or jailbreak tools on iOS 3.x.
