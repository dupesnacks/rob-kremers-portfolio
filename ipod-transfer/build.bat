@echo off
setlocal enabledelayedexpansion

echo ============================================================
echo  iPod Transfer — Build Script
echo  Builds a standalone Windows .exe
echo ============================================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Download from https://python.org
    echo         Make sure to check "Add Python to PATH" during install.
    pause
    exit /b 1
)

echo [1/4] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] pip install failed.
    pause
    exit /b 1
)

echo.
echo [2/4] Downloading libimobiledevice tools (for device detection)...
echo       These are optional but enable device info display.
echo       Skipping auto-download — place ideviceinfo.exe and idevicepair.exe
echo       in an "imobiledevice" subfolder next to the .exe if desired.
echo       Download from: https://github.com/libimobiledevice-win32/imobiledevice-net/releases
echo.

echo [3/4] Building .exe with PyInstaller...

:: Check for icon
set ICON_OPT=
if exist icon.ico (
    set ICON_OPT=--icon=icon.ico
)

python -m pyinstaller ^
    --onefile ^
    --windowed ^
    --name "iPodTransfer" ^
    --add-data "imobiledevice;imobiledevice" ^
    %ICON_OPT% ^
    --hidden-import "win32api" ^
    --hidden-import "win32com.client" ^
    --hidden-import "pywintypes" ^
    --hidden-import "PIL._tkinter_finder" ^
    ipod_transfer.py

if errorlevel 1 (
    echo.
    echo [ERROR] PyInstaller build failed.
    echo         Try running: pip install --upgrade pyinstaller pywin32
    pause
    exit /b 1
)

echo.
echo [4/4] Done!
echo.
echo ============================================================
echo  Your executable is at:
echo    dist\iPodTransfer.exe
echo ============================================================
echo.
echo  Optional: copy the "imobiledevice" folder next to the .exe
echo  for full device info and pairing support.
echo.
pause
