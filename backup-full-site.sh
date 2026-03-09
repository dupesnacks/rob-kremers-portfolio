#!/bin/bash
# FULL SITE BACKUP - Complete project with all assets
# Run this daily to back up everything

DATE=$(date +%Y-%m-%d)
BACKUP_DIR="/Users/rk/clawd/_BACKUPS/$DATE"

mkdir -p "$BACKUP_DIR"

echo "📦 Creating complete site backup for $DATE..."
echo ""

# Backup entire directories (with all assets)
echo "📁 Backing up full directories..."

# Flavor Galaxy (HTML + all images)
if [ -d "/Users/rk/clawd/flavorgalaxy" ]; then
    cp -r /Users/rk/clawd/flavorgalaxy "$BACKUP_DIR/flavorgalaxy" 2>/dev/null
    echo "✅ flavorgalaxy/ ($(find "$BACKUP_DIR/flavorgalaxy" -type f | wc -l) files)"
fi

# Rob Kremers Portfolio (entire project structure)
if [ -d "/Users/rk/clawd/rob-kremers-portfolio" ]; then
    cp -r /Users/rk/clawd/rob-kremers-portfolio "$BACKUP_DIR/rob-kremers-portfolio" 2>/dev/null
    echo "✅ rob-kremers-portfolio/ ($(find "$BACKUP_DIR/rob-kremers-portfolio" -type f | wc -l) files)"
fi

# Backup individual root HTML files
echo ""
echo "📄 Backing up root HTML pages..."
mkdir -p "$BACKUP_DIR/root-html"

cp /Users/rk/clawd/index-projects.html "$BACKUP_DIR/root-html/" 2>/dev/null && echo "✅ index-projects.html"
cp /Users/rk/clawd/rork.html "$BACKUP_DIR/root-html/" 2>/dev/null && echo "✅ rork.html"
cp /Users/rk/clawd/rork2.html "$BACKUP_DIR/root-html/" 2>/dev/null && echo "✅ rork2.html"
cp /Users/rk/clawd/tesla.html "$BACKUP_DIR/root-html/" 2>/dev/null && echo "✅ tesla.html"
cp /Users/rk/clawd/aurora.html "$BACKUP_DIR/root-html/" 2>/dev/null && echo "✅ aurora.html"
cp /Users/rk/clawd/consulting.html "$BACKUP_DIR/root-html/" 2>/dev/null && echo "✅ consulting.html"
cp /Users/rk/clawd/kofi.html "$BACKUP_DIR/root-html/" 2>/dev/null && echo "✅ kofi.html"
cp /Users/rk/clawd/dentalapp_webpage.html "$BACKUP_DIR/root-html/" 2>/dev/null && echo "✅ dentalapp_webpage.html"
cp /Users/rk/clawd/tfd_page.html "$BACKUP_DIR/root-html/" 2>/dev/null && echo "✅ tfd_page.html"
cp /Users/rk/clawd/tfd_app_brief.html "$BACKUP_DIR/root-html/" 2>/dev/null && echo "✅ tfd_app_brief.html"
cp /Users/rk/clawd/tfd_consumables.html "$BACKUP_DIR/root-html/" 2>/dev/null && echo "✅ tfd_consumables.html"
cp /Users/rk/clawd/dental_research_strategic_report.html "$BACKUP_DIR/root-html/" 2>/dev/null && echo "✅ dental_research_strategic_report.html"
cp /Users/rk/clawd/marlo-playbook.html "$BACKUP_DIR/root-html/" 2>/dev/null && echo "✅ marlo-playbook.html"
cp /Users/rk/clawd/viral.html "$BACKUP_DIR/root-html/" 2>/dev/null && echo "✅ viral.html"
cp /Users/rk/clawd/actually.html "$BACKUP_DIR/root-html/" 2>/dev/null && echo "✅ actually.html"

echo ""
echo "✅ BACKUP COMPLETE: $BACKUP_DIR"
echo "📊 Total files: $(find "$BACKUP_DIR" -type f | wc -l)"
echo "💾 Total size: $(du -sh "$BACKUP_DIR" | awk '{print $1}')"
echo "📍 Google Drive sync will pick this up automatically"
echo ""
