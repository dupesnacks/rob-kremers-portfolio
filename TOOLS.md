# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

## ByteRover (Memory)

**Semantic memory management for long-term context.**

### Commands

| Command | Purpose |
|---------|---------|
| `brv query "what to search"` | Search knowledge base semantically |
| `brv curate "what to remember"` | Store knowledge/patterns/decisions |
| `brv curate view` | Show recent curations (last 10) |
| `brv curate view --since 1h` | Show curations in last 1h |
| `brv status` | Check auth, project, provider state |
| `brv push` | Push local context to team space (optional) |
| `brv pull` | Pull team updates (optional) |

### Setup
- CLI: `brv --version` (or `npm install -g @byterover/cipher`)
- Config: `~/.brv/cipher.yml` (optional, uses defaults)
- Data: `~/.brv/context-tree/` (local markdown files)

### Example Workflow

**Before implementing:**
```bash
brv query "patterns for API error handling"
```

**After implementing:**
```bash
brv curate "Error handling: Use custom ErrorBoundary with Winston logging to stdout"
```

### Notes
- ByteRover is local-first (all data stays in `.brv/`)
- Cloud sync (push/pull) is optional, not required
- Context injection happens automatically during prompt building
- Memory flush happens automatically before context compaction

---

Add whatever helps you do your job. This is your cheat sheet.
