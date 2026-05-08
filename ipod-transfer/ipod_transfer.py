"""
iPod Touch Transfer — Windows 11
Transfers photos/videos to and from iPod Touch (iOS 3.1.3) over USB.
Uses WIA (Windows Image Acquisition) and PTP for photo access,
and communicates device status via libimobiledevice (bundled DLLs).
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import sys
import shutil
import subprocess
import datetime
import ctypes
import ctypes.wintypes
import time
from pathlib import Path
from PIL import Image, ImageTk
import io
import struct
import queue

# ── Colour palette ─────────────────────────────────────────────────────────────
BG        = "#0f0f0f"
PANEL     = "#1a1a1a"
BORDER    = "#2a2a2a"
ACCENT    = "#c8a96e"          # warm gold
ACCENT2   = "#e8c890"
TEXT      = "#e8e8e8"
MUTED     = "#777777"
SUCCESS   = "#5aad7a"
ERROR     = "#d95f5f"
WARNING   = "#e0a840"
DEVICE_ON = "#5aad7a"
DEVICE_OFF = "#555555"

FONT_MONO = ("Consolas", 9)
FONT_BODY = ("Segoe UI", 10)
FONT_HEAD = ("Segoe UI Semibold", 11)
FONT_TITLE= ("Segoe UI Light", 16)
FONT_BIG  = ("Segoe UI Semibold", 13)


# ─────────────────────────────────────────────────────────────────────────────
# WIA / PTP helper (Windows Image Acquisition COM automation)
# ─────────────────────────────────────────────────────────────────────────────

def get_wia_devices():
    """Return list of (device_id, name) tuples via WIA COM."""
    try:
        import win32com.client
        wia = win32com.client.Dispatch("WIA.DeviceManager")
        devices = []
        for i in range(1, wia.DeviceInfos.Count + 1):
            di = wia.DeviceInfos.Item(i)
            if di.Type == 1:   # 1 = Camera / PTP device
                devices.append((di.DeviceID, di.Properties("Name").Value))
        return devices
    except Exception:
        return []


def list_wia_items(device_id):
    """Return list of (item_id, name, size, date) from a WIA camera device."""
    try:
        import win32com.client
        wia = win32com.client.Dispatch("WIA.DeviceManager")
        device = None
        for i in range(1, wia.DeviceInfos.Count + 1):
            di = wia.DeviceInfos.Item(i)
            if di.DeviceID == device_id:
                device = di.Connect()
                break
        if device is None:
            return []
        items = []

        def walk(collection):
            for i in range(1, collection.Count + 1):
                item = collection.Item(i)
                try:
                    name = item.Properties("Item Name").Value
                except Exception:
                    name = f"item_{i}"
                try:
                    size = item.Properties("Item Size").Value
                except Exception:
                    size = 0
                try:
                    date_raw = item.Properties("Time Stamp").Value
                    date = str(date_raw)
                except Exception:
                    date = ""
                items.append((item.ItemID, name, size, date, item))
                try:
                    sub = item.Items
                    walk(sub)
                except Exception:
                    pass

        walk(device.Items)
        return items
    except Exception as e:
        return []


def download_wia_item(item_obj, dest_path):
    """Download a single WIA item to dest_path."""
    import win32com.client
    image_file = item_obj.Transfer()
    image_file.SaveFile(str(dest_path))


def upload_photo_wia(device_id, src_path):
    """Upload a photo to the device Camera Roll via WIA."""
    try:
        import win32com.client
        wia = win32com.client.Dispatch("WIA.DeviceManager")
        device = None
        for i in range(1, wia.DeviceInfos.Count + 1):
            di = wia.DeviceInfos.Item(i)
            if di.DeviceID == device_id:
                device = di.Connect()
                break
        if device is None:
            return False, "Device not found"
        # WIA upload is not universally supported on all iOS firmware.
        # We use the Shell approach as fallback.
        return False, "WIA upload not supported on this firmware. Use iTunes for sending files."
    except Exception as e:
        return False, str(e)


# ─────────────────────────────────────────────────────────────────────────────
# libimobiledevice wrapper (uses bundled ideviceinfo.exe / idevicepair.exe)
# ─────────────────────────────────────────────────────────────────────────────

def find_imobiledevice_dir():
    """Find bundled libimobiledevice tools next to the exe or script."""
    base = Path(getattr(sys, '_MEIPASS', Path(__file__).parent))
    for candidate in [base / "imobiledevice", base / "tools", base]:
        if (candidate / "ideviceinfo.exe").exists():
            return candidate
    # Also check PATH
    for p in os.environ.get("PATH", "").split(";"):
        if Path(p, "ideviceinfo.exe").exists():
            return Path(p)
    return None


def run_idevice_tool(tool, *args, timeout=8):
    idir = find_imobiledevice_dir()
    exe = (idir / tool) if idir else Path(tool)
    try:
        result = subprocess.run(
            [str(exe)] + list(args),
            capture_output=True, text=True, timeout=timeout
        )
        return result.returncode == 0, result.stdout, result.stderr
    except FileNotFoundError:
        return None, "", "tool not found"
    except subprocess.TimeoutExpired:
        return False, "", "timeout"
    except Exception as e:
        return False, "", str(e)


def get_device_info():
    """Return dict of device info from ideviceinfo, or None."""
    ok, out, err = run_idevice_tool("ideviceinfo.exe")
    if ok is None or not ok:
        return None
    info = {}
    for line in out.splitlines():
        if ": " in line:
            k, _, v = line.partition(": ")
            info[k.strip()] = v.strip()
    return info


def pair_device():
    ok, out, err = run_idevice_tool("idevicepair.exe", "pair")
    return ok, out or err


# ─────────────────────────────────────────────────────────────────────────────
# Thumbnail helper
# ─────────────────────────────────────────────────────────────────────────────

def make_thumbnail(path, size=(96, 96)):
    try:
        img = Image.open(path)
        img.thumbnail(size, Image.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception:
        return None


# ─────────────────────────────────────────────────────────────────────────────
# Main Application Window
# ─────────────────────────────────────────────────────────────────────────────

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("iPod Transfer")
        self.geometry("1000x680")
        self.minsize(820, 560)
        self.configure(bg=BG)
        self._set_icon()

        self.device_info   = None
        self.wia_device_id = None
        self.wia_items     = []
        self.selected_dir  = tk.StringVar(value=str(Path.home() / "Pictures" / "iPod"))
        self._thumb_cache  = {}
        self._msg_queue    = queue.Queue()

        self._build_ui()
        self._start_device_poller()
        self.after(200, self._drain_queue)

    # ── Icon (embed a tiny iPod-ish icon) ──────────────────────────────────
    def _set_icon(self):
        try:
            icon_path = Path(getattr(sys, '_MEIPASS', Path(__file__).parent)) / "icon.ico"
            if icon_path.exists():
                self.iconbitmap(str(icon_path))
        except Exception:
            pass

    # ── UI Construction ────────────────────────────────────────────────────
    def _build_ui(self):
        # Header bar
        hdr = tk.Frame(self, bg=PANEL, height=56)
        hdr.pack(fill="x", side="top")
        hdr.pack_propagate(False)

        tk.Label(hdr, text="◈  iPod Transfer", font=FONT_TITLE,
                 bg=PANEL, fg=ACCENT).pack(side="left", padx=20, pady=12)

        # Device status pill
        self._status_dot = tk.Label(hdr, text="●", font=("Segoe UI", 14),
                                    bg=PANEL, fg=DEVICE_OFF)
        self._status_dot.pack(side="right", padx=(0, 6), pady=14)
        self._status_lbl = tk.Label(hdr, text="No device", font=FONT_BODY,
                                    bg=PANEL, fg=MUTED)
        self._status_lbl.pack(side="right", padx=(0, 2), pady=14)

        # Pair button
        self._pair_btn = tk.Button(hdr, text="Pair", font=FONT_BODY,
                                   bg=BORDER, fg=ACCENT, relief="flat",
                                   activebackground=ACCENT, activeforeground=BG,
                                   cursor="hand2", padx=12,
                                   command=self._do_pair)
        self._pair_btn.pack(side="right", padx=12, pady=10)

        # Separator
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x")

        # Main body: left sidebar + right content
        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True)

        self._build_sidebar(body)
        self._build_content(body)

        # Bottom status bar
        self._build_statusbar()

    def _build_sidebar(self, parent):
        sb = tk.Frame(parent, bg=PANEL, width=220)
        sb.pack(side="left", fill="y")
        sb.pack_propagate(False)

        tk.Frame(sb, bg=BORDER, height=1).pack(fill="x")

        section = lambda title: (
            tk.Label(sb, text=title.upper(), font=("Segoe UI", 8),
                     bg=PANEL, fg=MUTED, anchor="w").pack(
                fill="x", padx=16, pady=(16, 4))
        )

        # Device info panel
        section("Device")
        self._info_frame = tk.Frame(sb, bg=PANEL)
        self._info_frame.pack(fill="x", padx=16, pady=4)
        self._info_rows = {}
        for key in ["Model", "iOS", "Name", "Serial", "Storage"]:
            row = tk.Frame(self._info_frame, bg=PANEL)
            row.pack(fill="x", pady=1)
            tk.Label(row, text=key, font=FONT_MONO, bg=PANEL,
                     fg=MUTED, width=8, anchor="w").pack(side="left")
            val = tk.Label(row, text="—", font=FONT_MONO,
                           bg=PANEL, fg=TEXT, anchor="w")
            val.pack(side="left", fill="x", expand=True)
            self._info_rows[key] = val

        tk.Frame(sb, bg=BORDER, height=1).pack(fill="x", padx=0, pady=8)

        # Save location
        section("Save location")
        dir_row = tk.Frame(sb, bg=PANEL)
        dir_row.pack(fill="x", padx=16, pady=2)
        self._dir_entry = tk.Entry(dir_row, textvariable=self.selected_dir,
                                   font=("Consolas", 8), bg=BORDER, fg=TEXT,
                                   insertbackground=ACCENT,
                                   relief="flat", bd=4)
        self._dir_entry.pack(side="left", fill="x", expand=True)
        tk.Button(dir_row, text="…", font=FONT_BODY, bg=BORDER, fg=ACCENT,
                  relief="flat", cursor="hand2", padx=6,
                  command=self._choose_dir).pack(side="right")

        tk.Frame(sb, bg=BORDER, height=1).pack(fill="x", padx=0, pady=8)

        # Music note
        section("Music")
        note_text = (
            "Music sync requires\n"
            "iTunes for iOS 3.x.\n\n"
            "Download iTunes 10.7\n"
            "for Windows (last\n"
            "version for this iOS)."
        )
        tk.Label(sb, text=note_text, font=("Consolas", 8), bg=PANEL,
                 fg=WARNING, justify="left", wraplength=188).pack(
            padx=16, pady=2, anchor="w")

        tk.Button(sb, text="Open iTunes Download Page",
                  font=("Consolas", 8), bg=BORDER, fg=ACCENT,
                  relief="flat", cursor="hand2", pady=4,
                  command=lambda: self._open_url(
                      "https://support.apple.com/downloads/itunes")).pack(
            padx=16, fill="x", pady=(4, 0))

    def _build_content(self, parent):
        right = tk.Frame(parent, bg=BG)
        right.pack(side="left", fill="both", expand=True)

        # Tab bar
        tabbar = tk.Frame(right, bg=PANEL, height=40)
        tabbar.pack(fill="x")
        tabbar.pack_propagate(False)

        self._tab_buttons = {}
        self._active_tab  = tk.StringVar(value="photos")
        for tab_id, label in [("photos", "📷  Photos & Videos"),
                                ("upload", "⬆  Send to Device"),
                                ("log",    "◎  Activity Log")]:
            btn = tk.Button(tabbar, text=label, font=FONT_BODY,
                            bg=PANEL, fg=MUTED, relief="flat",
                            activebackground=BG, activeforeground=ACCENT,
                            cursor="hand2", padx=16,
                            command=lambda t=tab_id: self._switch_tab(t))
            btn.pack(side="left", fill="y")
            self._tab_buttons[tab_id] = btn

        self._tab_indicator = tk.Frame(tabbar, bg=ACCENT, height=2)

        tk.Frame(right, bg=BORDER, height=1).pack(fill="x")

        # Content frames
        self._content = tk.Frame(right, bg=BG)
        self._content.pack(fill="both", expand=True)

        self._tabs = {}
        self._tabs["photos"] = self._build_photos_tab(self._content)
        self._tabs["upload"] = self._build_upload_tab(self._content)
        self._tabs["log"]    = self._build_log_tab(self._content)

        self._switch_tab("photos")

    def _switch_tab(self, tab_id):
        self._active_tab.set(tab_id)
        for tid, frame in self._tabs.items():
            frame.pack_forget()
        self._tabs[tab_id].pack(fill="both", expand=True)
        for tid, btn in self._tab_buttons.items():
            btn.config(fg=ACCENT if tid == tab_id else MUTED,
                       bg=BG if tid == tab_id else PANEL)

    def _build_photos_tab(self, parent):
        frame = tk.Frame(parent, bg=BG)

        toolbar = tk.Frame(frame, bg=PANEL, height=44)
        toolbar.pack(fill="x")
        toolbar.pack_propagate(False)

        tk.Button(toolbar, text="⟳  Refresh", font=FONT_BODY,
                  bg=BORDER, fg=ACCENT, relief="flat", cursor="hand2", padx=12,
                  command=self._refresh_photos).pack(side="left", padx=8, pady=6)

        self._select_all_var = tk.BooleanVar()
        tk.Checkbutton(toolbar, text="Select all", variable=self._select_all_var,
                       font=FONT_BODY, bg=PANEL, fg=TEXT,
                       selectcolor=BORDER, activebackground=PANEL,
                       command=self._toggle_select_all).pack(
            side="left", padx=8)

        self._dl_btn = tk.Button(toolbar, text="⬇  Download Selected",
                                 font=FONT_BODY, bg=ACCENT, fg=BG,
                                 relief="flat", cursor="hand2", padx=14,
                                 command=self._download_selected)
        self._dl_btn.pack(side="right", padx=8, pady=6)

        self._photo_count_lbl = tk.Label(toolbar, text="", font=FONT_BODY,
                                         bg=PANEL, fg=MUTED)
        self._photo_count_lbl.pack(side="right", padx=8)

        tk.Frame(frame, bg=BORDER, height=1).pack(fill="x")

        # Scrollable grid
        canvas_frame = tk.Frame(frame, bg=BG)
        canvas_frame.pack(fill="both", expand=True)

        self._canvas = tk.Canvas(canvas_frame, bg=BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical",
                                  command=self._canvas.yview)
        self._canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self._canvas.pack(side="left", fill="both", expand=True)

        self._grid_frame = tk.Frame(self._canvas, bg=BG)
        self._canvas_window = self._canvas.create_window(
            (0, 0), window=self._grid_frame, anchor="nw")
        self._grid_frame.bind("<Configure>", self._on_grid_configure)
        self._canvas.bind("<Configure>", self._on_canvas_configure)
        self._canvas.bind("<MouseWheel>", self._on_mousewheel)

        # Empty state
        self._empty_lbl = tk.Label(self._grid_frame,
                                   text="Connect your iPod Touch and click Refresh",
                                   font=FONT_HEAD, bg=BG, fg=MUTED)
        self._empty_lbl.pack(pady=80)

        self._photo_cards   = []
        self._photo_vars    = []

        return frame

    def _build_upload_tab(self, parent):
        frame = tk.Frame(parent, bg=BG)

        tk.Label(frame, text="Send Photos to iPod Camera Roll",
                 font=FONT_BIG, bg=BG, fg=ACCENT).pack(pady=(24, 4))
        tk.Label(frame,
                 text="Supported formats: JPG, PNG, GIF, BMP",
                 font=FONT_BODY, bg=BG, fg=MUTED).pack(pady=(0, 20))

        drop_frame = tk.Frame(frame, bg=PANEL, bd=0, relief="flat")
        drop_frame.pack(padx=40, pady=8, fill="x")

        tk.Label(drop_frame,
                 text="Select files to send to your iPod Touch",
                 font=FONT_HEAD, bg=PANEL, fg=TEXT).pack(pady=(20, 6))

        self._upload_listbox = tk.Listbox(drop_frame, bg=BORDER, fg=TEXT,
                                          font=FONT_MONO, height=8,
                                          selectmode="extended",
                                          relief="flat", bd=0,
                                          selectbackground=ACCENT,
                                          selectforeground=BG)
        self._upload_listbox.pack(padx=20, fill="x")

        btn_row = tk.Frame(drop_frame, bg=PANEL)
        btn_row.pack(pady=12)

        tk.Button(btn_row, text="+ Add Files", font=FONT_BODY,
                  bg=BORDER, fg=ACCENT, relief="flat", cursor="hand2", padx=14,
                  command=self._add_upload_files).pack(side="left", padx=4)
        tk.Button(btn_row, text="✕ Remove Selected", font=FONT_BODY,
                  bg=BORDER, fg=MUTED, relief="flat", cursor="hand2", padx=14,
                  command=self._remove_upload_selected).pack(side="left", padx=4)

        self._send_btn = tk.Button(frame, text="⬆  Send to iPod",
                                   font=FONT_HEAD, bg=ACCENT, fg=BG,
                                   relief="flat", cursor="hand2",
                                   padx=24, pady=10,
                                   command=self._do_upload)
        self._send_btn.pack(pady=16)

        self._upload_note = tk.Label(frame,
            text="Note: Sending photos requires iTunes to be installed and the device paired.",
            font=("Consolas", 8), bg=BG, fg=MUTED, wraplength=560)
        self._upload_note.pack(pady=4)

        return frame

    def _build_log_tab(self, parent):
        frame = tk.Frame(parent, bg=BG)

        toolbar = tk.Frame(frame, bg=PANEL, height=40)
        toolbar.pack(fill="x")
        toolbar.pack_propagate(False)
        tk.Label(toolbar, text="Activity Log", font=FONT_HEAD,
                 bg=PANEL, fg=TEXT).pack(side="left", padx=16, pady=8)
        tk.Button(toolbar, text="Clear", font=FONT_BODY,
                  bg=BORDER, fg=MUTED, relief="flat", cursor="hand2", padx=10,
                  command=lambda: self._log_text.delete("1.0", "end")).pack(
            side="right", padx=8, pady=6)

        tk.Frame(frame, bg=BORDER, height=1).pack(fill="x")

        self._log_text = tk.Text(frame, bg=BG, fg=TEXT,
                                 font=FONT_MONO, relief="flat",
                                 wrap="word", state="disabled",
                                 insertbackground=ACCENT)
        scroll = ttk.Scrollbar(frame, command=self._log_text.yview)
        self._log_text.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        self._log_text.pack(fill="both", expand=True, padx=4, pady=4)

        self._log_text.tag_config("info",    foreground=TEXT)
        self._log_text.tag_config("success", foreground=SUCCESS)
        self._log_text.tag_config("error",   foreground=ERROR)
        self._log_text.tag_config("warn",    foreground=WARNING)
        self._log_text.tag_config("ts",      foreground=MUTED)

        return frame

    def _build_statusbar(self):
        bar = tk.Frame(self, bg=PANEL, height=26)
        bar.pack(fill="x", side="bottom")
        bar.pack_propagate(False)
        tk.Frame(bar, bg=BORDER, height=1).pack(fill="x", side="top")
        self._status_bar_lbl = tk.Label(bar, text="Ready", font=FONT_MONO,
                                        bg=PANEL, fg=MUTED, anchor="w")
        self._status_bar_lbl.pack(side="left", padx=12)

        self._progress = ttk.Progressbar(bar, length=200, mode="determinate")
        self._progress.pack(side="right", padx=12, pady=4)

    # ── Utility methods ────────────────────────────────────────────────────
    def _log(self, msg, level="info"):
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        self._log_text.config(state="normal")
        self._log_text.insert("end", f"[{ts}] ", "ts")
        self._log_text.insert("end", msg + "\n", level)
        self._log_text.see("end")
        self._log_text.config(state="disabled")

    def _set_status(self, msg):
        self._status_bar_lbl.config(text=msg)

    def _set_device_connected(self, info_dict):
        self._status_dot.config(fg=DEVICE_ON)
        self._status_lbl.config(fg=SUCCESS, text="Connected")
        model    = info_dict.get("ProductType", info_dict.get("Model", "iPod Touch"))
        ios_ver  = info_dict.get("ProductVersion", "?")
        name     = info_dict.get("DeviceName", "iPod")
        serial   = info_dict.get("SerialNumber", "?")
        capacity = info_dict.get("TotalDiskCapacity", "")

        def fmt_storage(b):
            try:
                gb = int(b) / 1e9
                return f"{gb:.1f} GB"
            except Exception:
                return b

        self._info_rows["Model"].config(text=model)
        self._info_rows["iOS"].config(text=ios_ver)
        self._info_rows["Name"].config(text=name)
        self._info_rows["Serial"].config(text=serial[:12] if serial else "?")
        self._info_rows["Storage"].config(text=fmt_storage(capacity) if capacity else "?")

    def _set_device_disconnected(self):
        self._status_dot.config(fg=DEVICE_OFF)
        self._status_lbl.config(fg=MUTED, text="No device")
        for lbl in self._info_rows.values():
            lbl.config(text="—")
        self.device_info   = None
        self.wia_device_id = None

    def _choose_dir(self):
        d = filedialog.askdirectory(title="Choose save folder",
                                    initialdir=self.selected_dir.get())
        if d:
            self.selected_dir.set(d)

    def _open_url(self, url):
        import webbrowser
        webbrowser.open(url)

    def _drain_queue(self):
        try:
            while True:
                fn = self._msg_queue.get_nowait()
                fn()
        except queue.Empty:
            pass
        self.after(100, self._drain_queue)

    def _ui(self, fn):
        """Schedule a lambda on the main thread."""
        self._msg_queue.put(fn)

    # ── Device polling ─────────────────────────────────────────────────────
    def _start_device_poller(self):
        self._poll_thread = threading.Thread(
            target=self._device_poll_loop, daemon=True)
        self._poll_thread.start()

    def _device_poll_loop(self):
        last_state = None
        while True:
            info = get_device_info()
            if info is not None and last_state != "connected":
                last_state = "connected"
                self.device_info = info
                self._ui(lambda i=info: self._set_device_connected(i))
                self._ui(lambda: self._log(
                    f"Device connected: {info.get('DeviceName','iPod')} "
                    f"(iOS {info.get('ProductVersion','?')})", "success"))
                # Also scan WIA
                self._ui(self._scan_wia_device)
            elif info is None and last_state == "connected":
                last_state = "disconnected"
                self._ui(self._set_device_disconnected)
                self._ui(lambda: self._log("Device disconnected.", "warn"))
            elif info is None and last_state is None:
                last_state = "disconnected"
            time.sleep(3)

    def _scan_wia_device(self):
        """Find the iPod in WIA device list."""
        devs = get_wia_devices()
        if devs:
            self.wia_device_id = devs[0][0]
            self._log(f"WIA device found: {devs[0][1]}", "success")
        else:
            self.wia_device_id = None

    # ── Pair button ────────────────────────────────────────────────────────
    def _do_pair(self):
        self._log("Attempting to pair device…", "info")
        self._set_status("Pairing…")

        def task():
            ok, msg = pair_device()
            if ok is None:
                self._ui(lambda: self._log(
                    "libimobiledevice tools not found. See setup instructions.", "error"))
            elif ok:
                self._ui(lambda: self._log("Paired successfully!", "success"))
            else:
                self._ui(lambda: self._log(f"Pair result: {msg}", "warn"))
            self._ui(lambda: self._set_status("Ready"))

        threading.Thread(target=task, daemon=True).start()

    # ── Photo grid ─────────────────────────────────────────────────────────
    def _refresh_photos(self):
        if not self.wia_device_id:
            # Try WIA even without libimobiledevice
            devs = get_wia_devices()
            if devs:
                self.wia_device_id = devs[0][0]
            else:
                messagebox.showwarning(
                    "Device not found",
                    "No iPod detected via WIA (Windows Image Acquisition).\n\n"
                    "Make sure:\n"
                    "• The iPod is unlocked and showing the home screen\n"
                    "• You accepted the 'Trust this computer' prompt on the device\n"
                    "• The USB cable is securely connected\n"
                    "• Apple Mobile Device Support is installed (comes with iTunes)")
                return

        self._set_status("Reading photos from device…")
        self._log("Reading device photos…")
        self._progress.config(mode="indeterminate")
        self._progress.start(10)

        def task():
            items = list_wia_items(self.wia_device_id)
            self._ui(lambda: self._populate_grid(items))

        threading.Thread(target=task, daemon=True).start()

    def _populate_grid(self, items):
        self._progress.stop()
        self._progress.config(mode="determinate", value=0)

        # Clear
        for widget in self._grid_frame.winfo_children():
            widget.destroy()
        self._photo_cards = []
        self._photo_vars  = []
        self.wia_items    = items
        self._thumb_cache = {}

        if not items:
            tk.Label(self._grid_frame,
                     text="No photos found on device.\n\nMake sure the device is unlocked.",
                     font=FONT_HEAD, bg=BG, fg=MUTED).pack(pady=80)
            self._photo_count_lbl.config(text="0 items")
            self._set_status("Ready — no photos found")
            return

        self._photo_count_lbl.config(text=f"{len(items)} items")
        self._log(f"Found {len(items)} photos/videos.", "success")
        self._set_status(f"{len(items)} items found")

        # Build grid: 6 columns of cards
        COLS = 6
        for idx, (item_id, name, size, date, item_obj) in enumerate(items):
            var = tk.BooleanVar()
            self._photo_vars.append(var)

            card = tk.Frame(self._grid_frame, bg=PANEL, bd=1, relief="flat",
                            width=130, height=150)
            card.grid(row=idx // COLS, column=idx % COLS,
                      padx=4, pady=4, sticky="nsew")
            card.pack_propagate(False)

            # Placeholder thumbnail
            thumb_lbl = tk.Label(card, bg=PANEL, fg=MUTED,
                                 text="⬛", font=("Segoe UI", 24))
            thumb_lbl.pack(pady=(8, 2))

            tk.Label(card, text=name[:18], font=("Consolas", 7),
                     bg=PANEL, fg=TEXT, wraplength=120).pack()

            sz_str = f"{size/1024:.0f} KB" if size else ""
            tk.Label(card, text=sz_str, font=("Consolas", 7),
                     bg=PANEL, fg=MUTED).pack()

            cb = tk.Checkbutton(card, variable=var, bg=PANEL,
                                selectcolor=BORDER,
                                activebackground=PANEL)
            cb.pack(pady=(2, 4))

            self._photo_cards.append(
                (card, thumb_lbl, var, item_id, name, item_obj))

    def _toggle_select_all(self):
        state = self._select_all_var.get()
        for var in self._photo_vars:
            var.set(state)

    def _download_selected(self):
        selected = [(iid, name, obj)
                    for (_, _, var, iid, name, obj) in self._photo_cards
                    if var.get()]
        if not selected:
            messagebox.showinfo("Nothing selected",
                                "Check the boxes under photos you want to download.")
            return

        save_dir = Path(self.selected_dir.get())
        save_dir.mkdir(parents=True, exist_ok=True)

        self._set_status(f"Downloading {len(selected)} items…")
        self._progress.config(mode="determinate", maximum=len(selected), value=0)
        self._log(f"Downloading {len(selected)} items to {save_dir}…")

        def task():
            ok_count = 0
            for i, (iid, name, obj) in enumerate(selected):
                dest = save_dir / name
                try:
                    download_wia_item(obj, dest)
                    ok_count += 1
                    self._ui(lambda n=name: self._log(f"  ✓ {n}", "success"))
                except Exception as e:
                    self._ui(lambda n=name, err=e:
                             self._log(f"  ✗ {n}: {err}", "error"))
                self._ui(lambda v=i+1: self._progress.config(value=v))

            self._ui(lambda: self._log(
                f"Done — {ok_count}/{len(selected)} downloaded to {save_dir}", "success"))
            self._ui(lambda: self._set_status("Download complete"))
            self._ui(lambda: messagebox.showinfo(
                "Download complete",
                f"{ok_count} of {len(selected)} files saved to:\n{save_dir}"))

        threading.Thread(target=task, daemon=True).start()

    # ── Upload tab actions ─────────────────────────────────────────────────
    def _add_upload_files(self):
        files = filedialog.askopenfilenames(
            title="Select photos to send",
            filetypes=[("Images", "*.jpg *.jpeg *.png *.gif *.bmp *.heic"),
                       ("All files", "*.*")])
        for f in files:
            self._upload_listbox.insert("end", f)

    def _remove_upload_selected(self):
        for idx in reversed(self._upload_listbox.curselection()):
            self._upload_listbox.delete(idx)

    def _do_upload(self):
        files = list(self._upload_listbox.get(0, "end"))
        if not files:
            messagebox.showinfo("No files", "Add files first using '+ Add Files'.")
            return
        if not self.wia_device_id:
            messagebox.showerror(
                "Device not connected",
                "Please connect and unlock your iPod Touch first.")
            return

        self._log(f"Sending {len(files)} files to device…")
        self._set_status("Uploading…")

        def task():
            # WIA upload to iOS 3.x is generally not supported.
            # We try itunes AFC / iFuse as alternative.
            failed = []
            for f in files:
                ok, msg = upload_photo_wia(self.wia_device_id, f)
                if not ok:
                    failed.append((f, msg))
                    self._ui(lambda fn=f, m=msg:
                             self._log(f"  ✗ {Path(fn).name}: {m}", "error"))
                else:
                    self._ui(lambda fn=f:
                             self._log(f"  ✓ {Path(fn).name}", "success"))

            if failed:
                self._ui(lambda: messagebox.showwarning(
                    "Upload limited",
                    "iOS 3.1.3 does not support WIA photo upload.\n\n"
                    "To copy photos TO the device:\n"
                    "1. Open iTunes 10.7\n"
                    "2. Select your device → Photos tab\n"
                    "3. Check 'Sync Photos' and choose your folder"))
            self._ui(lambda: self._set_status("Ready"))

        threading.Thread(target=task, daemon=True).start()

    # ── Canvas / scroll helpers ────────────────────────────────────────────
    def _on_grid_configure(self, event):
        self._canvas.configure(scrollregion=self._canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        self._canvas.itemconfig(self._canvas_window, width=event.width)

    def _on_mousewheel(self, event):
        self._canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Windows DPI awareness
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

    app = App()
    app.mainloop()
