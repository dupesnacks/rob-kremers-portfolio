#!/bin/bash
# BACKUP SCRIPT - RUN THIS BEFORE EVERY DEPLOY
# Usage: ./backup-before-deploy.sh

DATE=$(date +%Y-%m-%d)
BACKUP_DIR="/Users/rk/clawd/_BACKUPS/$DATE"

mkdir -p "$BACKUP_DIR"

echo "📦 Creating dated backups for $DATE..."

# Backup all HTML files from key locations
cp /Users/rk/clawd/flavorgalaxy/index.html "$BACKUP_DIR/flavorgalaxy-index.html" 2>/dev/null && echo "✅ flavorgalaxy"
cp /Users/rk/clawd/rob-kremers-portfolio/teslasales/index.html "$BACKUP_DIR/teslasales-index.html" 2>/dev/null && echo "✅ teslasales"
cp /Users/rk/clawd/rork.html "$BACKUP_DIR/rork.html" 2>/dev/null && echo "✅ rork"
cp /Users/rk/clawd/rork2.html "$BACKUP_DIR/rork2.html" 2>/dev/null && echo "✅ rork2"
cp /Users/rk/clawd/tesla.html "$BACKUP_DIR/tesla.html" 2>/dev/null && echo "✅ tesla (root)"

# Add any other important pages here
cp /Users/rk/clawd/aurora.html "$BACKUP_DIR/aurora.html" 2>/dev/null && echo "✅ aurora"
cp /Users/rk/clawd/consulting.html "$BACKUP_DIR/consulting.html" 2>/dev/null && echo "✅ consulting"

echo ""
echo "✅ BACKUP COMPLETE: $BACKUP_DIR"
echo "📍 Google Drive sync will pick this up automatically"
echo ""
