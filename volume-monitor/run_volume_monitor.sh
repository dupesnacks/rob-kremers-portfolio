#!/bin/bash
# Volume Monitor Cron Wrapper
cd /Users/rk/clawd/volume-monitor
python3 volume_monitor.py >> /tmp/volume_monitor.log 2>&1
