# Sensory Explorer: Points & Rewards Economy

**Purpose:** Define how kids earn points, unlock badges, and progress through the galaxy without feeling forced or grindy.

**Goal:** Balance motivation with realism. Kid should feel progress within days, not months.

---

## Design Principles

1. **Progress is Visible** — Points accumulate visibly, badges unlock frequently
2. **No Forced Grinding** — Can't "grind" sensory therapy; reward consistent behavior
3. **Risk = Reward** — Trying harder foods = bigger point boost
4. **Streaks Matter** — Consistency is more valuable than one-time actions
5. **Celebration Moments** — Visual/audio feedback when milestones hit (not annoying, just satisfying)

---

## Points System

### Per-Action Points

#### **Logging a Food (Daily Incentive)**
```
Log any food:                  +10 points
- Completes a SOS phase:       +5 bonus points
- Completes TASTE phase:       +10 bonus points (full journey complete)
- First log of the day:        +5 bonus points (encouraging daily habit)

Example:
Kid logs "Chicken Nugget" at LOOK phase = 10 + 5 = 15 points
Kid logs same food reaching TASTE = 10 + 10 = 20 points
```

#### **Bridge Food Actions**
```
Try a recommended bridge food:  +20 points
- Accept bridge food (eat/enjoy): +30 points (bigger reward for success)
- Reject bridge food:           +5 points (still reward trying)
```

#### **New Foods (Exploration)**
```
Try a completely new food:     +25 points
- First time ANY sensory phase: +25 points
- Reach TASTE on new food:     +50 points (major milestone)
```

#### **Streaks**
```
Log food on 7 consecutive days:  +100 points (1-week milestone)
Log food on 30 consecutive days: +500 points (1-month major milestone)
Log food on 60 consecutive days: +1,000 points (elite milestone)
Maintain 3+ day streak:          Unlock fire 🔥 animation
```

#### **Goal Food Progress**
```
Log progress on goal food:     +50 points per phase reached
Complete all 5 phases of goal: +200 bonus points + celebration

Example: Goal is "Pizza"
- Log Pizza at LOOK:  +50 points
- Log Pizza at TOUCH: +50 points
- ...
- Log Pizza at TASTE: +50 points + 200 bonus = 250 points total
```

---

## Badge Unlock Thresholds

### Tier 1: Getting Started (3 badges)

| Badge | Unlock Condition | Points Needed |
|-------|-----------------|--------------|
| **First Taste Explorer** | Log first food in TASTE phase | Immediate |
| **Sensory Seeker** | Complete LOOK phase with any food | Immediate |
| **Brave Mouth** | Reach LICK or TASTE with 3+ foods | ~500 points (3-4 days) |

### Tier 2: Building Comfort (4 badges)

| Badge | Unlock Condition | Points Needed |
|-------|-----------------|--------------|
| **Touch Adventurer** | Complete TOUCH phase with 5+ foods | ~750 points (5-6 days) |
| **Smell Specialist** | Complete SMELL phase with 5+ foods | ~750 points (5-6 days) |
| **Color Explorer** | Try foods from 5+ different colors | ~1,000 points (depends on existing safe foods) |
| **Texture Master** | Try 5+ different textures | ~1,200 points (1-2 weeks) |

### Tier 3: Flavor Progression (3 badges)

| Badge | Unlock Condition | Points Needed |
|-------|-----------------|--------------|
| **Sweet Discoverer** | Try 3+ sweet-flavored foods | ~600 points (depends on existing) |
| **Salty Sampler** | Try 3+ salty-flavored foods | ~800 points (1 week) |
| **Flavor Frontier** | Try 6+ flavor families | ~2,000 points (RARE - 2-3 weeks) |

### Tier 4: Speed Milestones (2 badges)

| Badge | Unlock Condition | Points Needed |
|-------|-----------------|--------------|
| **Week Warrior** | Log 7 consecutive days | Automatic @ day 7 |
| **30-Day Devotee** | Log 30 consecutive days | Automatic @ day 30 |

### Tier 5: Bridge & Variety (3 badges)

| Badge | Unlock Condition | Points Needed |
|-------|-----------------|--------------|
| **Bridge Builder** | Try 5+ bridge foods, accept 3+ | ~1,500 points (2 weeks) |
| **Food Group Collector** | Try 5+ food groups | ~2,000 points (2-3 weeks) - RARE |
| **Rainbow Eater** | Try all 9 colors | ~3,000 points (3-4 weeks) - RARE |

### Optional Tier 6: Special (5 badges)

| Badge | Unlock Condition | Points Needed |
|-------|-----------------|--------------|
| **SOS Master** | Complete all 5 phases with 10+ foods | ~3,500 points (4+ weeks) |
| **Planet Pioneer** | Reach planet 4+ | Automatic w/ progression |
| **Brave Taste Tester** | Try HIGH-RISK food & accept | Automatic on success |
| **Consistency Champion** | 60+ day logging streak | Automatic @ day 60 |
| **Galaxy Legend** | Unlock 12+ other badges | Automatic w/ mastery |

---

## Level Progression (Galaxy Path)

**Current Issue:** Kid approved 35 foods → jumped to Planet 7 immediately (no progression).

**New Logic:** Progression tied to PHASE completion, not food count.

```
Planet 1: Base Camp
- Unlock: First food logged
- Progress: Complete LOOK phase with 3+ foods (50 points)

Planet 2: Sensory Grove
- Unlock: Reach TOUCH with 3+ foods (200 points)
- Progress: Complete TOUCH phase with 5+ foods (500 points)

Planet 3: Texture Trails
- Unlock: Reach SMELL with 3+ foods (300 points)
- Progress: Complete SMELL phase with 5+ foods (600 points)

Planet 4: Aroma Airship
- Unlock: Reach LICK with 3+ foods (400 points)
- Progress: Complete LICK phase with 5+ foods (750 points)

Planet 5: Flavor Mountains
- Unlock: Reach TASTE with 3+ foods (500 points)
- Progress: Reach TASTE with 10+ foods (1,000 points)

Planet 6: Taste Ocean
- Unlock: Try 3+ bridge foods (750 points)
- Progress: Accept 5+ bridge foods (1,200 points)

Planet 7: Taste Jungle
- Unlock: Explore 5+ food groups (1,000 points)
- Progress: Try all 9 colors (1,500 points)

Planet 8: Galaxy's Heart
- Unlock: Master 50+ foods across all phases (2,000 points)
- Unlock: Complete goal food journey (1,000 points)
- Progress: Achieve Galaxy Legend badge (unlock 12+ badges)
```

**Result:** Kid progresses 1 planet every 1-2 weeks with consistent logging.

---

## Celebration Moments

### Visual Feedback (Non-Annoying)
```
Milestone Animations:
- +50 points: Subtle point pop-up (cyan), no sound
- Badge unlock: Celebration confetti (3 seconds), success chime
- +100 point milestone: Explorer "walks" visually toward next planet
- 3-day streak: Fire 🔥 animation, "On Fire!" message
- 7-day streak: Major celebration, confetti, "Week Warrior!" badge
- 30-day streak: Full screen celebration (optional, can skip)
- Planet unlock: Explorer arrives at new planet, intro screen
```

### No:
- ❌ Constant notifications
- ❌ "You earned X points!" popups on every action
- ❌ Audio unless kid/parent enables
- ❌ Aggressive re-engagement pushes

### Yes:
- ✅ Satisfying visual moments
- ✅ Clear progress indicators
- ✅ Milestone celebrations (7/30/60 days)
- ✅ Optional sounds (toggle in Settings)

---

## Weekly Challenge (Optional, Phase 2)

**Proposed (not in MVP):**
```
Every week, assign a sensory challenge:
- "Try 3 crunchy foods this week"
- "Explore a sour flavor"
- "Reach TASTE with 2 new foods"

Reward: +100 bonus points + unique badge if completed

Keeps app engagement fresh without feeling forced.
```

---

## Parent Dashboard View

Parents should see:
```
📊 Points This Week: 450 points
🔥 Current Streak: 7 days
🏆 Badges Earned: 8/20

Recent Activity:
- 3 days ago: Earned "Touch Adventurer" badge (+5 streak)
- 5 days ago: Tried "Fish Stick" at TASTE phase (+50 points)
- 7 days ago: Started 7-day streak (+100 points)

Next Milestones:
- 30 consecutive days → "30-Day Devotee" badge
- Try 5th food group → "Food Group Collector" badge
- Reach Planet 5 → Flavor Mountains unlock
```

---

## Test Scenarios

### Scenario 1: Fast Progression (Likely Mack's Path)

**Kid:** Approves 35 safe foods upfront → logs all at various phases

```
Day 1: Logs 5 foods at LOOK phase
- +10 pts × 5 = 50 pts
- +5 bonus (first of day) = 5 pts
- Total: 55 pts

Day 2: Logs 8 foods, 3 reach TASTE
- +10 pts × 8 = 80 pts
- +10 bonus × 3 (TASTE) = 30 pts
- +5 bonus (first of day) = 5 pts
- Total: 115 pts

Day 3: Logs 6 foods, 1 bridge food accepted
- +10 pts × 6 = 60 pts
- +30 pts (bridge accepted) = 30 pts
- Total: 90 pts

Weekly Total: 260 points → Planet progression slow (requires phase completion thresholds, not just food volume)
```

**Fix for Mack:** Slow planet progression by requiring multiple foods per phase, not just quantity.

---

### Scenario 2: Steady Progression (Ideal)

**Kid:** Logs 1-2 foods daily, progresses through phases gradually

```
Day 1: Log "Chicken Nugget" at LOOK phase: 15 pts
Day 2: Log "Chicken Nugget" at TOUCH phase: 15 pts
Day 3: Log "Chicken Nugget" at SMELL phase: 15 pts
Day 4: Log "Chicken Nugget" at LICK phase: 15 pts
Day 5: Log "Chicken Nugget" at TASTE phase: 20 pts
Day 6: Log "Fish Stick" at LOOK phase: 10 pts (new food)
Day 7: Log "Fish Stick" at TOUCH phase, maintain 7-day streak: 15 + 100 = 115 pts

Weekly Total: 205 points + 1 Week Warrior badge
```

**Result:** Kid feels steady progress, earns badges, sees planets unlock.

---

## Adjustment Rules

**Monitor these metrics weekly during beta:**

1. **Badge Unlock Rate**
   - Target: 1-2 badges per week per kid
   - If too fast: Increase threshold by 20%
   - If too slow: Decrease threshold by 20%

2. **Streak Maintenance**
   - Target: 70%+ maintain 7+ day streaks
   - If too easy: Increase daily point threshold
   - If too hard: Add "makeup day" feature (catch up one missed day)

3. **Planet Progression**
   - Target: 1 planet every 10-14 days
   - Mack (35 foods): Should take 3-4 weeks to reach Planet 5
   - New user (3 safe foods): Should take 2-3 weeks to reach Planet 2

---

## Implementation Checklist

- [ ] Define points per action (above)
- [ ] Code points system backend
- [ ] Add point animations to UI
- [ ] Create badge unlock notifications
- [ ] Build celebration moments (confetti, explorer walk)
- [ ] Code streak counter + fire animation
- [ ] Test with Mack account for pacing
- [ ] Adjust thresholds based on beta feedback
- [ ] Deploy to TestFlight/Google Play beta
- [ ] Monitor retention + engagement daily

---

## Success Metrics (Phase 1)

- ✅ 80%+ daily logging on days 1-14
- ✅ 70%+ maintain 7+ day streaks
- ✅ 3-5 badges earned per kid in first month
- ✅ 1 planet progression every 10-14 days
- ✅ No complaints about "grinding" or "slow progress"
- ✅ Parents report kids motivated by badges + points

---

**Questions for Implementation:**
1. Should daily login give bonus points even if no food logged? (Current: No)
2. Should bridge food rejection still give points? (Current: Yes, +5)
3. Should goal food progress give daily bonuses? (Current: +50 per phase)
4. Celebration notification frequency: Every 25 points? Every badge? (Recommend: Only badges + milestones)

**Ready to code?** 🚀
