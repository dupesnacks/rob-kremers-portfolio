# robkremers.com Deployment Guide

## Overview
- **Repo**: https://github.com/dupesnacks/rob-kremers-portfolio
- **Live Site**: https://robkremers.com
- **Hosting**: Vercel (auto-deploys on push)
- **No build step needed** — static HTML files

## File Structure

```
/Users/rk/clawd/
├── vercel.json          ← Route configuration
├── aurora.html          ← /aurora route
├── consulting.html      ← /consulting route
├── tesla.html           ← /tesla route (Tesla tracker)
├── rork.html            ← /rork route (short pitch)
├── rork2.html           ← /rork2 route (full case study)
└── /rork/               ← Image assets for /rork
    ├── dupe-snacks-1.png
    ├── flavor-galaxy-1.png
    └── ... other images
```

## Publishing Steps

### 1. Edit Files
Make changes directly in `/Users/rk/clawd/`:
- **HTML files**: Edit content, styling, text
- **Images**: Place in appropriate folder (`/rork/`, `/buildsheets/`, etc.)

### 2. Commit Changes
```bash
cd /Users/rk/clawd
git add <filename.html>           # or specific files
git add -A                        # or all changes
git commit -m "Description of changes"
```

### 3. Push to GitHub
```bash
git push origin main
```

**That's it.** Vercel auto-deploys in 30-60 seconds.

## Creating New Pages

### Step 1: Create HTML file
Save as `/Users/rk/clawd/yourpage.html` with full HTML structure.

### Step 2: Add route in vercel.json
```json
{
  "source": "/yourpage",
  "destination": "/yourpage.html"
}
```

### Step 3: Commit and push
```bash
git add yourpage.html vercel.json
git commit -m "Add /yourpage route"
git push origin main
```

**Live at**: `https://robkremers.com/yourpage`

## Common Tasks

### Update Tesla Tracker
1. Edit `tesla.html` → find `const orders = [`
2. Add new order before closing `]`:
```javascript
{ id: 30, date: '2026-03-08T12:00:00Z', model: 'Model Y', trim: 'RWD', msrp: 45000, fsd: 'None', orderType: 'Custom' }
```
3. Update date range in header: `Jan 11 – Mar 8`
4. Update footer: `Data current as of Mar 8, 2026`
5. Commit and push

### Update /rork Page
1. Edit `rork.html` directly in your text editor
2. Change any text, styling, or structure
3. Commit with `git commit -m "Update /rork: [description]"`
4. Push with `git push origin main`

### Add Images
1. Place images in correct folder (`/rork/`, `/buildsheets/`, etc.)
2. Reference in HTML as: `<img src="/rork/image-name.png">`
3. Commit and push

## Important Rules

### Date Formatting (Critical!)
**Always use this format for dates in data:**
```javascript
date: '2026-03-07T12:00:00Z'  ✅ Correct
date: '2026-03-07'            ❌ Wrong (timezone shifts date back 1 day)
```

The `T12:00:00Z` is **required** to display dates correctly.

### Image Paths
**Always use absolute paths starting with `/`:**
```html
<img src="/rork/image.png">      ✅ Correct
<img src="rork/image.png">       ❌ Wrong
<img src="./rork/image.png">     ❌ Wrong
```

### vercel.json Syntax
Keep it clean:
```json
{
  "buildCommand": "echo 'Static site - no build needed'",
  "outputDirectory": ".",
  "rewrites": [
    { "source": "/routename", "destination": "/routename.html" }
  ],
  "trailingSlash": false
}
```

## Troubleshooting

### Page shows 404
1. Check `vercel.json` has the route defined
2. Verify HTML file exists at root (`/Users/rk/clawd/pagename.html`)
3. Hard refresh browser: `Cmd+Shift+R`
4. Force redeploy: `git commit --allow-empty -m "Force redeploy"` → `git push`

### Images not loading
1. Check image path starts with `/` (absolute path)
2. Verify file exists in correct folder
3. Commit and push (images need to be in git)

### Date shows wrong day
1. Ensure date format is `YYYY-MM-DDTHH:MM:SSZ`
2. Never use just `YYYY-MM-DD` (causes timezone shift)

### Changes not live yet
1. Vercel takes 30-60 seconds to deploy
2. Hard refresh: `Cmd+Shift+R`
3. Check GitHub shows your commit: https://github.com/dupesnacks/rob-kremers-portfolio/commits/main

## Git Cheat Sheet

```bash
# View status
git status

# Add specific file
git add filename.html

# Add all changes
git add -A

# Commit
git commit -m "Your message here"

# Push to GitHub (auto-deploys)
git push origin main

# View recent commits
git log --oneline -5

# Force redeploy (empty commit)
git commit --allow-empty -m "Force redeploy"
git push origin main
```

## Quick Reference

| Task | Command |
|------|---------|
| Edit page | Open `.html` file in editor |
| Add new page | Create `.html` + add route to `vercel.json` |
| Commit changes | `git add <files>` → `git commit -m "msg"` |
| Deploy | `git push origin main` |
| Check deployment | `robkremers.com/yourpage` (wait 60s) |
| Force redeploy | Empty commit + push |

---

**Need help?** Ask in Discord with the page name and what you're trying to change.
