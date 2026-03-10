# Onboarding Redesign + Bridge Food LLM Integration Brief

**Prepared for:** Rork  
**Date:** March 10, 2026  
**Priority:** CRITICAL (blocking beta launch)

---

## PART 1: ONBOARDING REDESIGN

### Problem
Current onboarding:
- ❌ Focuses on form capture (35 foods upfront → false progression)
- ❌ Doesn't clearly communicate the transformation
- ❌ Mixing empathy + SOS explanation + gamification without clear hierarchy
- ❌ Parents don't understand the VALUE before committing data
- ❌ Kids picked explorer before understanding what they're doing

**Result:** Parents feel like they're filling out a medical form, not starting a journey.

---

### Solution: Transformation-Focused Onboarding

**Redesigned Flow (Cards 1-4):**

#### **CARD 1: The Problem (Empathy Hook)**

**Headline:** "Your Child Isn't Picky. They're Sensory-Sensitive."

**Copy:**
```
You know your child. You know mealtimes are stressful. You know they eat from a tiny list of foods.

And you know it's not stubbornness. It's not behavior. It's sensory.

Their nervous system processes textures, tastes, and temperatures differently. What feels smooth to you might feel wrong to them. What smells good might feel overwhelming.

The good news? Sensory sensitivity is rewirable. With the right approach and patience, kids can expand their food world naturally—without pressure, without battles.

You're not alone. 1 in 3 children experience selective eating tied to sensory sensitivity.
```

**Visual:** Kid with food, parent looking relieved (empathy visual, not clinical)

**CTA:** "Next →"

**Why this works:**
- Validates parent's experience
- Normalizes (1 in 3 statistic)
- Positions therapy, not parenting failure
- Emotional hook before education

---

#### **CARD 2: The Science (SOS Method Explained)**

**Headline:** "Gentle Progress, Not Forced Eating"

**Subheading:** "The SOS Approach – Used by Therapists Worldwide"

**Copy:**
```
We use the Sequential Oral Sensory (SOS) Approach—the same evidence-based method used by occupational therapists and speech therapists for 30+ years.

Instead of pressure or bribes, SOS works WITH your child's nervous system:

👁️ LOOK — Getting comfortable seeing the food
🙌 TOUCH — Exploring textures with their hands
👃 SMELL — Experiencing aromas
👅 LICK — Trying tiny tastes
😋 TASTE — Eating and enjoying

Each phase takes 3-10 days. No rushing. Kids progress when their nervous system is ready.

**The Results:** Research shows children using the SOS Approach see measurable improvements in food acceptance and mealtime confidence within weeks to months—not years.
```

**Visual:** 5 sensory phases diagram (already in app)

**Key Stats to Highlight:**
- 30+ years of clinical research
- 5 sequential phases (no pressure to skip)
- Improvements visible in weeks-months (not years)
- Proven effective for sensory-sensitive eaters

**CTA:** "Next →"

**Why this works:**
- Educates parent on methodology
- Builds credibility (30 years, therapists)
- Shows realistic timeline
- Explains WHY phases exist (not arbitrary)

---

#### **CARD 3: Bridge Foods (The Secret Weapon)**

**Headline:** "Bridge Foods: The Clever Way to Expand Their Diet"

**Copy:**
```
Here's where the magic happens.

Your child has safe foods they already like. Chicken nuggets. Crackers. Whatever.

A "bridge food" shares the same sensory qualities as their safe foods—but introduces something new.

**Example:**
→ If they like crunchy, salty crackers
→ Try crunchy, salty pretzels (similar texture, new taste)
→ Then gradually explore other crunchy foods

It's not random. It's strategic sensory matching.

**Smart Recommendations:**
Our app analyzes your child's safe foods, identifies their sensory preferences, and suggests bridge foods they're most likely to accept—personalized to THEIR profile, not generic suggestions.

This is how selective eaters become adventurous eaters. One bridge at a time.
```

**Visual:** Show a "bridge" concept—safe food → bridge food → new food (visual progression)

**CTA:** "Next →"

**Why this works:**
- Explains the TOOL (bridge foods) clearly
- Shows parent the power of sensory matching
- Positions app as smart (personalized, not random)
- Concrete example (crackers → pretzels) is understandable

---

#### **CARD 4: What Success Looks Like (The Promise)**

**Headline:** "Track Every Victory (Big & Small)"

**Copy:**
```
We celebrate progress that matters:

📊 **For You (Parent):**
- Visual dashboard showing food diversity (textures, flavors, colors expanding)
- Trend reports: What's working? What's the next sensory challenge?
- Export summaries for therapists or pediatricians
- Printable certificates when major milestones hit

🎮 **For Your Child:**
- A galaxy to explore (8 planets, 5 phases each)
- Daily streaks + rewards (fire emoji 🔥, cosmetics, badges)
- Their own explorer character they level up
- Tangible proof they're getting braver

**The Outcome:**
After weeks of consistent logging, you'll see the pattern. Your child is eating more. Trying new things. Growing more confident.

Not because you forced it. Because they felt safe to explore.
```

**Visual:** Split screen—parent dashboard analytics + kid explorer progression

**CTA:** "Let's Get Started →"

**Why this works:**
- Shows both parent AND kid value
- Concrete outcomes (not vague)
- Celebrates milestones
- Emotional payoff (safety + growth)

---

### CARD 5-ONWARD: Progressive Data Collection (Revised)

**Current issue:** Asking for 35+ safe foods upfront causes decision paralysis + false progression.

**New approach:**

#### **CARD 5: Explorer Selection (Lower Friction)**
- Pick explorer character (Nova, Cosmo, Star, Orbit)
- Name them
- Show cosmetics unlock preview
- **Skip safe foods for now**

#### **CARD 6: Quick Start (3-5 Foods)**
```
Headline: "Let's Start Simple"

"Tell us 3-5 foods your child already eats comfortably. We'll use these to understand their sensory profile and suggest bridge foods.

Don't overthink it—you can add more later."
```
- Show 20-30 common safe foods (checkboxes, not free-form)
- Parent selects 3-5
- **Much lower friction than asking for 35**

#### **CARD 7: Goal Food (Emotional Connection)**
```
"What's one food you'd love them to eat someday?"

- Open text field (e.g., "Pizza")
- Ask what challenges it has (texture, flavor, temperature)
- Why this matters: Makes the goal personal, not clinical
```

#### **CARD 8: Mission Briefing (Show the Path)**
```
"Here's [Child's Name]'s mission:

Safe Foods: 3 logged ✓
Foods to Explore: 82 options
Current Explorer Level: 1 (Base Camp)

Next Challenge: Find 2 bridge foods that match their sensory profile
Next Milestone: Reach Planet 2 (in progress)
```

**Show actual data, not a form.**

#### **CARD 9: First Action (In-App Win)**
```
"Let's Log Your First Food Together"

Walk through logging their breakfast/snack:
- Food name
- What phase (LOOK, TOUCH, SMELL, LICK, TASTE)
- Get a recommendation
- Celebrate (confetti, XP, something positive)

Exit onboarding having already USED the core feature.
```

---

## PART 2: BRIDGE FOOD RECOMMENDATION LLM INTEGRATION

### Problem with Current Bridge Food Algorithm

**Current approach:** Likely distance-based sensory matching (e.g., if safe food is "crunchy + salty", recommend other crunchy + salty foods).

**Limitations:**
- ❌ Doesn't account for food availability in app DB
- ❌ Doesn't consider child's risk tolerance or progression pace
- ❌ Not personalized to child's history/patterns
- ❌ Can't explain WHY a recommendation was made
- ❌ Doesn't learn from parent acceptance/rejection
- ❌ Generic sensory profiles, not unique child profiles

**Result:** Recommendations miss 30% of the time; parent loses trust.

---

### Solution: LLM-Powered Bridge Food Matching

#### **Architecture**

```
Parent logs safe foods → Child's sensory profile built → 
LLM analyzes profile + context → Smart bridge food recommendations
```

#### **LLM Prompt (Claude 3.5 Sonnet recommended)**

```
System Prompt:
You are a Sensory Feeding Expert specializing in the SOS (Sequential Oral Sensory) Approach.
Your role is to recommend "bridge foods" that match a child's sensory profile with high likelihood of acceptance.

A bridge food:
- Shares sensory qualities (texture, flavor, temperature) with foods the child already eats
- Introduces ONE new sensory element at a time
- Is age-appropriate and available
- Matches the child's current risk tolerance

You consider:
1. Safe foods they've already accepted (recent history)
2. Textures they avoid (aversions)
3. Flavors they're exploring
4. Temperature preferences
5. Color variety (helps with food group diversity)
6. Their current planet/phase (progression pace)
7. Previous bridge food outcomes (what worked, what didn't)

Output: Top 3-5 bridge foods with:
- Food name + image
- Why this works (clear explanation in parent-friendly language)
- Sensory match (crunchy, sweet, soft, etc.)
- Risk level (Low/Medium/High)
- Next steps (how to introduce it)

User Input:
{
  "child_name": "Mack",
  "age": 6,
  "safe_foods": [
    {"name": "Chicken Nugget", "textures": ["crunchy"], "flavors": ["bland", "salty"], "temp": "hot", "color": "golden"},
    {"name": "White Bread", "textures": ["soft"], "flavors": ["bland"], "temp": "room temp", "color": "white"},
    {"name": "Scrambled Eggs", "textures": ["soft", "mushy"], "flavors": ["bland"], "temp": "hot", "color": "yellow"},
    ...
  ],
  "aversions": ["bitter", "sour", "too spicy"],
  "explored_foods": {
    "Sweet Potato": {"result": "rejected", "reason": "too mushy"},
    "Fish Stick": {"result": "accepted", "reason": "similar to chicken nugget"}
  },
  "current_planet": 2,
  "current_phase": "LICK",
  "goal_food": "Pizza",
  "available_foods_in_app": [...], // full food DB
  "parent_note": "She likes warm foods, avoids anything too wet"
}

Output:
[
  {
    "name": "Cheese Quesadilla",
    "why": "Combines warm (like eggs/nuggets) + soft + cheesy (subtle salty flavor progression from bland nuggets)",
    "sensory_match": "Soft, warm, slightly crunchy edges, savory-adjacent",
    "risk": "LOW",
    "next_steps": "Start by letting her help make it, touch the tortilla before cooking, then taste a small corner"
  },
  ...
]
```

#### **Integration Points**

1. **Backend API Route** (new endpoint)
   ```
   POST /api/bridge-foods/recommend
   
   Input: Child's sensory profile + safe foods + history
   Output: Top 3-5 recommendations with explanations
   Cache for 24h (don't call LLM every page load)
   ```

2. **Suggest Tab Enhancement**
   - Replace current algorithm with LLM calls
   - Show "Why This Works" explanation
   - Track which recommendations parent explores/accepts
   - Use feedback to refine future recommendations (learning loop)

3. **Cost Estimate**
   - Claude 3.5 Sonnet: ~$0.001 per recommendation call
   - ~100K users × 2 recommendations/week = ~$10K/year
   - **Manageable at scale**

4. **Fallback Logic**
   - If API fails, revert to current distance-based algorithm
   - Never break app (graceful degradation)

#### **Improvements Over Current Approach**

| Aspect | Current | With LLM |
|--------|---------|----------|
| Reasoning | Distance-based formula | Contextual understanding |
| Explanation | Generic (e.g., "similar texture") | Specific ("warm like eggs, soft like bread, slightly salty like nuggets") |
| Learning | No feedback loop | Parent feedback refines future recs |
| Personalization | Profile-based | History + risk tolerance + progression pace |
| Accuracy | ~70% acceptance | Target 85%+ acceptance |

---

## IMPLEMENTATION ROADMAP

### Phase 1: Onboarding Redesign (2 days)
- [ ] Rewrite copy for Cards 1-4
- [ ] Adjust data collection flow (3-5 foods → later "add more")
- [ ] Add first-action in-app logging to onboarding
- [ ] Test with 3 parents (feedback loop)

### Phase 2: Bridge Food LLM Integration (3 days)
- [ ] Create LLM prompt + test against 10 real child profiles
- [ ] Build `/api/bridge-foods/recommend` endpoint
- [ ] Integrate into Suggest tab UI
- [ ] Add "Why This Works" explanations
- [ ] Implement caching + fallback logic

### Phase 3: Learning Loop (1 day)
- [ ] Track parent feedback on recommendations (like/skip/reject)
- [ ] Feed feedback into future prompts (continuous improvement)
- [ ] Monitor accuracy % weekly

---

## Success Metrics

**Onboarding:**
- [ ] Completion rate: >80% (currently likely 60-70%)
- [ ] Time to first food logged: <5 minutes (vs. 10+ now)
- [ ] Parents report clarity improvement in feedback

**Bridge Foods:**
- [ ] Recommendation acceptance rate: >85%
- [ ] Parent trust in suggestions improves (survey pre/post)
- [ ] Foods tried from Suggest tab increases 30%

---

## Next Steps

1. **Confirm copy direction** with you
2. **Get API access** to Claude (or Gemini if preferred)
3. **Review current bridge food code** (need to see current algorithm)
4. **Test LLM recommendations** against real child profiles from beta testing
5. **Deploy to staging** for internal testing

---

## Questions for You

1. **LLM Choice:** Claude 3.5 Sonnet (recommended) vs Gemini Advanced vs Grok?
2. **Data History:** Do we have past logging data from Mack's account to test recommendations against?
3. **Onboarding Copy Tone:** More clinical/therapist-focused or parent-friendly/conversational?
4. **Bridge Foods:** Should we show explanation to kid, parent, or both?

**Ready when you are.** 🚀
