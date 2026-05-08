# Deployment Checklist - ALWAYS FOLLOW THIS

## Before Every Deploy

**Step 1: Verify routing is correct**
```bash
bash /Users/rk/clawd/verify-deploy.sh
```

If this fails, **DO NOT DEPLOY**. Fix the issue first (see troubleshooting below).

**Step 2: Back up the site**
```bash
bash /Users/rk/clawd/backup-full-site.sh
```

**Step 3: Deploy to production**
```bash
cd /Users/rk/clawd && vercel deploy --prod --token $VERCEL_TOKEN --yes
```

---

## Canonical File Locations (NEVER EDIT ROOT VERSIONS)

| URL | Canonical File | Notes |
|-----|----------------|-------|
| `/teslasales` | `/rob-kremers-portfolio/teslasales/index.html` | ✅ Edit this one |
| `/r2` | `/rob-kremers-portfolio/r2/index.html` | ✅ Edit this one |
| `/rork` | `/rork.html` | Root level |
| `/rork2` | `/rork2.html` | Root level |
| `/flavorgalaxy` | `/flavorgalaxy/index.html` | Root level |

---

## If verification fails:

**Check 1: File exists?**
```bash
ls -la /Users/rk/clawd/rob-kremers-portfolio/teslasales/index.html
```

**Check 2: vercel.json routing correct?**
```bash
grep "teslasales" /Users/rk/clawd/vercel.json
```

Should show:
```json
{ "source": "/teslasales", "destination": "/rob-kremers-portfolio/teslasales/index.html" }
```

**Check 3: Hard refresh your browser**
```
Cmd+Shift+R (Mac)
```

---

## Why this matters

The routing mismatch caused teslasales to serve stale content from a root-level file that wasn't being updated. By verifying before every deploy, we catch this immediately instead of deploying silently-broken code.

