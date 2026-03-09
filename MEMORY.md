# MEMORY.md - Critical Procedures & Context

## 🚨 CRITICAL: BACKUP BEFORE EVERY DEPLOY

**THIS IS NON-NEGOTIABLE.** Before deploying ANYTHING to Vercel:

1. Run: `bash /Users/rk/clawd/backup-before-deploy.sh`
2. Wait for ✅ confirmation
3. THEN run vercel deploy

**Why:** March 8, 2026 - Flavor Galaxy site was completely lost due to deployment error. No backup existed. This nearly destroyed the entire project.

**The System:**
- `/Users/rk/clawd/_BACKUPS/[YYYY-MM-DD]/` = Daily dated copies of ALL HTML files
- Google Drive syncs this automatically (immutable, off-site)
- Git history = additional layer (can revert commits)
- Three independent layers = never lose work again

**Pages to always backup:**
- flavorgalaxy/index.html
- rob-kremers-portfolio/teslasales/index.html
- rork.html, rork2.html
- tesla.html (root)
- aurora.html, consulting.html
- Any other custom HTML pages

---

## Website Pages & Endpoints

**Live Sites:**
- `https://robkremers.com/flavorgalaxy` - Flavor Galaxy Adventure (planets + explorers app)
- `https://robkremers.com/teslasales` - Tesla sales tracker (30+ orders, $1.3M revenue)
- `https://robkremers.com/rork` - Rork pitch page (short version, 409 lines)
- `https://robkremers.com/rork2` - Rork full case study (608 lines)
- `https://robkremers.com/tesla` - Tesla tracker (root HTML)
- `https://robkremers.com/aurora` - Aurora page
- `https://robkremers.com/consulting` - Consulting page

**Flavor Galaxy Details:**
- 8 interactive planets (Base Camp, Sensory Grove, Texture Trails, Aroma Airship, Flavor Mountains, Taste Ocean, Taste Jungle, Galaxy's Heart)
- 4 explorers with bios:
  - **Nova** = Speed Explorer ("Loves discovering fast & trying new things!")
  - **Cosmo** = Science Explorer ("Curious about flavors & tastes!")
  - **Star** = Brave Explorer ("Not afraid to try new things!")
  - **Orbit** = Adventurous Explorer ("Loves collecting & exploring!")
- Colors: Dark background #0a0a1e, cyan/gold/purple gradients, gradient text
- Pricing: Monthly $3.99, Annual $24.99

**Tesla Tracker:**
- 30 orders as of March 9, 2026
- Total revenue: $1,310,065+
- Last entry: Order #30, Model 3 Premium RWD, FSD Subscription, March 9, 2026, $44,130

---

## Deployment Notes

**Vercel API Token:** (stored securely, not in git - see .env or local config)

**Deploy Command:** `cd /Users/rk/clawd && vercel deploy --prod --token [TOKEN] --yes`

**GitHub:** https://github.com/dupesnacks/rob-kremers-portfolio

**Important Files:**
- `/Users/rk/clawd/vercel.json` - Vercel routing config (static site, no build needed)
- `/Users/rk/clawd/flavorgalaxy/` - All Flavor Galaxy assets
- `/Users/rk/clawd/rob-kremers-portfolio/` - Main project folder
- `/Users/rk/clawd/_BACKUPS/` - Daily backup folder (synced to Google Drive)

---

## What NOT to Do

- ❌ Never edit root `.html` files directly without backing up first
- ❌ Never deploy without running backup script first
- ❌ Never assume git history is enough (it can be lost too)
- ❌ Never trust a single deployment method (use layered backups)

---

**Last Updated:** March 9, 2026 (Backup system implemented)
