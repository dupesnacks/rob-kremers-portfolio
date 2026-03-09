# Asset Manifest - Flavor Galaxy / Sensory Explorer

**Purpose:** Track all visual assets and ensure they're committed to version control.

## Asset Locations

### Primary (version controlled in GitHub)
```
/Users/rk/clawd/rob-kremers-portfolio/
├── public/flavorgalaxy/          ← VERCEL DEPLOYMENT SOURCE
│   ├── index.html                ✅ Landing page
│   ├── planet-01-base-camp.png   ✅ 1.3MB
│   ├── planet-02-sensory-grove.png  ✅ 1.5MB
│   ├── planet-03-texture-trails.png ✅ 1.8MB
│   ├── planet-04-aroma-airship.png  ✅ 1.6MB
│   ├── planet-05-flavor-mountains.png ✅ 1.6MB
│   ├── planet-06-taste-ocean.png    ✅ 1.2MB
│   ├── planet-07-taste-jungle.png   ✅ 1.7MB
│   ├── planet-08-galaxys-heart.png  ✅ 1.2MB
│   ├── explorer-nova.jpg         ✅ 148KB (portrait)
│   ├── explorer-nova.png         ✅ 287KB (full-body, transparent)
│   ├── explorer-cosmo.jpg        ✅ 58KB (portrait)
│   ├── explorer-cosmo.png        ✅ 238KB (full-body, transparent)
│   ├── explorer-star.jpg         ✅ 73KB (portrait)
│   ├── explorer-star.png         ✅ 353KB (full-body, transparent)
│   ├── explorer-orbit.jpg        ✅ 67KB (portrait)
│   └── explorer-orbit.png        ✅ 231KB (full-body, transparent)
│
└── flavorgalaxy/                 ← Source (mirrors public/)
    └── (same structure as above)
```

### Backup (local drive)
```
/Users/rk/clawd/
├── flavor-galaxy-1.png  ✅ (backup copy)
├── flavor-galaxy-2.png  ✅
├── flavor-galaxy-3.png  ✅
└── flavor-galaxy-4.png  ✅
```

## Git Status

**All files committed:**
```bash
git ls-files public/flavorgalaxy/
git ls-files rob-kremers-portfolio/flavorgalaxy/
```

**Verify before deployment:**
```bash
cd /Users/rk/clawd/rob-kremers-portfolio
git status  # Should show nothing or only non-asset changes
git log --oneline -5  # Check recent commits
```

## Deployment Checklist

- [ ] All assets in `/public/flavorgalaxy/` 
- [ ] `vercel.json` has `"outputDirectory": "public"`
- [ ] All files committed to git (`git status` clean)
- [ ] Latest commits pushed to origin (`git push origin main`)
- [ ] Vercel rebuild triggered (wait 30-60 seconds)
- [ ] Test: `curl https://www.robkremers.com/flavorgalaxy/planet-01-base-camp.png`
- [ ] Verify HTML loads: `https://www.robkremers.com/flavorgalaxy/`

## Vercel Configuration

**File:** `/Users/rk/clawd/rob-kremers-portfolio/vercel.json`

```json
{
  "buildCommand": "echo 'Static site'",
  "outputDirectory": "public",  ← CRITICAL
  "framework": null,
  "cleanUrls": true,
  "trailingSlash": false,
  "routes": [
    {
      "src": "/flavorgalaxy/(.*)",
      "dest": "/flavorgalaxy/$1"
    },
    {
      "src": "/teslasales/(.*)",
      "dest": "/teslasales/$1"
    }
  ]
}
```

**If Vercel doesn't auto-deploy:**
1. Go to https://vercel.com/dashboard
2. Select `rob-kremers-portfolio` project
3. Click **"Deployments"** tab
4. Click **"Redeploy"** on latest commit
5. Or check **"Build Logs"** for errors

## Asset Specifications

| Asset Type | Count | Format | Size | Location |
|-----------|-------|--------|------|----------|
| Planet Images | 8 | PNG | 1.2-1.8 MB ea | `planet-0[1-8]-*.png` |
| Explorer Portraits | 4 | JPG | 58-148 KB ea | `explorer-{nova,cosmo,star,orbit}.jpg` |
| Explorer Full-Body | 4 | PNG (transparent) | 231-353 KB ea | `explorer-{nova,cosmo,star,orbit}.png` |
| Landing Page | 1 | HTML | 19 KB | `index.html` |
| **Total** | **17** | Mixed | **~23 MB** | All in git ✅ |

## Never Again

**Root cause:** Assets weren't committed to git → Vercel couldn't access them

**Prevention:**
1. All assets MUST go in `/public/flavorgalaxy/`
2. Always run `git add` + `git commit` + `git push`
3. Verify with `git ls-files` before deployment
4. Test deployed URLs before announcing

**Command to verify everything is committed:**
```bash
cd /Users/rk/clawd/rob-kremers-portfolio
echo "=== Files in public/flavorgalaxy ===" && ls public/flavorgalaxy/ | wc -l
echo "=== Files in git ===" && git ls-files public/flavorgalaxy/ | wc -l
# Both should match
```

---

**Last Updated:** 2026-03-08 20:40 PDT  
**Status:** ✅ All assets committed, awaiting Vercel rebuild
