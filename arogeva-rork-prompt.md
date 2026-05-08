# Arogeva Nutrition Intelligence Platform — Refinement Brief for Rork AI

## Executive Context

**App Name:** Arogeva™  
**Founder/Expert:** Mitali Kapila, MS, RD, CLT (20+ years clinical dietitian experience)  
**Current Version:** Multi-market launch ready (India + US versions)  
**Market Focus:** India/GCC diaspora + US-centric version  
**Core Thesis:** Functional nutrition intelligence — not calories, but *condition-specific wisdom*

---

## What Makes Arogeva Different (The Intelligence Layer)

Unlike basic calorie-counting apps, Arogeva answers:
- **"What should I eat if I have [condition]?"** → Personalized protocols, not generic lists
- **"What's safe to eat outside?"** → Restaurant navigation for your condition
- **"What should I shop for?"** → Grocery lists tailored to your health goals
- **"How do my conditions connect?"** → Functional medicine approach (gut issues → hormonal issues)
- **"What do my lab values mean?"** → Clinical interpretation tied to food choices

The app uses **condition + diet + lifestyle data** to build personalized action plans rooted in Mitali's clinical experience.

---

## Current Platform Strengths (Preserve These)

✅ **Privacy-first design** — User data encrypted, never sold, transparent collection  
✅ **Founder authority** — Mitali's credentials prominently featured (bonds with users)  
✅ **Smart onboarding** — Captures: demographics, activity, diet type, life stage, regional cuisine, primary+secondary conditions  
✅ **Dual app tracks** — Adult app + Arogeva Junior (kids with autoimmune conditions)  
✅ **Regional specificity** — Indian food wisdom + 180 regional recipes across 8 Indian food cultures  
✅ **Personalized insights** — "Mitali's Reading" (clinical interpretation) + "Mitali's First Prescription" (actionable protocol)  
✅ **Condition library** — 12+ conditions supported: Anemia, Autoimmune, Diabetes, Bone Health, Brain & Focus, Fertility, Gut Health, Heart Health, PCOS, Perimenopause, Skin & Hair, Stress/Burnout

---

## Areas for Refinement & Development

### 1. **Condition Interconnection Engine** ⚡ HIGH PRIORITY
- **Current:** Users select primary + secondary conditions independently
- **Needed:** AI logic that connects related conditions (e.g., "PCOS + Gut Health" → hormonal-gut protocol vs. standalone gut protocol)
- **Why:** Functional medicine recognizes conditions rarely exist alone; the *interactions* matter
- **Refinement:** Build a decision tree/graph showing how conditions amplify or ameliorate each other
- **Example:** User selects Gut Health + Brain & Focus → show how leaky gut impacts cognition; adjust recipes/supplements accordingly

### 2. **Multi-Market Content Strategy** 🌍 CRITICAL
- **Current:** India version sketched; US version mentioned as "same structure, different content"
- **Needed:** Define content architecture:
  - **India:** 180 regional recipes × 8 food cultures + Ayurvedic food wisdom + common diaspora health issues
  - **US:** Adapted recipes, FDA-standard ingredients, US regional cuisines (Southern, Tex-Mex, etc.), insurance/clinical pathway integration
  - **GCC:** Halal-certified recipes, expat-specific protocols, local ingredient substitutions
- **Refinement:** Build a content taxonomy that allows recipes/protocols to be region-swappable without UI changes

### 3. **Travel Meal Navigation (API Integration)** ✈️ MEDIUM PRIORITY
- **Current:** Mentioned but not shown in screenshots; needs API tie-in
- **Needed:** Integration with restaurant/food delivery APIs (Zomato for India, Uber Eats/GrubHub for US) + a *smart filter*:
  - User picks primary condition + selects restaurant
  - App shows: "Safe meals" / "Modify these" / "Avoid"
  - Links to actual menu items with nutritional breakdowns
- **Refinement:** Design the "meal safety score" algorithm + clarify which APIs to target (regional availability varies)
- **Example:** User at Chipotle with Gut Health focus → highlight cilantro-lime rice (fermented), flag sour cream (if lactose-sensitive), suggest carnitas (protein without seed oils)

### 4. **Personalized Recipe Engine** 👨‍🍳 MEDIUM PRIORITY
- **Current:** 180 pre-built regional recipes (good foundation)
- **Needed:** Dynamic recipe filtering/generation:
  - Filter by: condition + dietary pattern + available ingredients + prep time + cuisine preference
  - Stretch goal: AI-powered recipe generation (e.g., "Generate a gut-healing khichdi variation for vegan + Andhra Pradesh style")
  - Include nutrition facts tied back to condition goals (e.g., "This recipe is high in [prebiotic fiber] which supports your Gut Health protocol")
- **Refinement:** Schema for recipes (ingredients, method, nutritional breakdown, condition tags, regional variants)

### 5. **Protocol Recommendation System** 📋 HIGH PRIORITY
- **Current:** Mitali can hand-craft protocols (seen in screenshot: 3-day khichdi reset for gut issues)
- **Needed:** Scalable system for Mitali to *author* protocols that the app personalizes:
  - Input: Condition + secondary conditions + diet type + activity level + life stage
  - Output: Phased protocol (e.g., Phase 1: Elimination, Phase 2: Reintroduction, Phase 3: Maintenance)
  - Include: Recipes tied to each phase, shopping lists, supplement guidance, timeline
- **Refinement:** Admin panel for Mitali to create/edit protocols; versioning for updates (if she refines a protocol, users should see the update)

### 6. **Lab Value Interpretation** 🧪 MEDIUM PRIORITY
- **Current:** Mentioned in app features ("Lab value interpretation with functional medicine")
- **Needed:** User uploads lab reports (blood work, stool analysis, etc.) → app interprets in context of their condition + food choices
  - Example: User with low ferritin + anemia → "Your iron is low. This is common with [your dietary pattern]. Start the Anemia protocol with iron-rich foods like [regional options]"
  - Safe guardrail: App doesn't diagnose, just educates + empowers user to discuss with their doctor
- **Refinement:** Define which lab markers matter for each condition; build interpretation logic that ties to protocols/recipes

### 7. **Gut Score & Condition Score Dashboard** 📊 MEDIUM PRIORITY
- **Current:** Screenshot shows "Needs Attention 10/15" + "Active 10/15" (red cards)
- **Needed:** Clarify the scoring system:
  - What's measured? (User input + AI analysis of food log + lab data?)
  - What does the score mean? (10/15 = "moderate imbalance"?)
  - How does it update? (Daily? Weekly? After user logs meals?)
  - Visualization: Show trend over time (improving trend = motivation)
- **Refinement:** Dashboard mockup showing daily/weekly score trends + milestone celebrations

### 8. **User Engagement & Logging** 📱 MEDIUM PRIORITY
- **Current:** Onboarding flow visible; logging/journaling not shown
- **Needed:** Simple logging system for:
  - Meals eaten (+ condition impact feedback)
  - Symptoms (feeling bloated? brain fog? energy?)
  - Sleep, stress, exercise
  - Access to "Daily Mitali Lesson" (AI-powered education or Mitali's recorded content?)
- **Refinement:** Design the daily dashboard + journaling flow; keep friction low (voice-to-meal capture? photo recognition?)

### 9. **Accessibility & Localization** 🌐 MEDIUM PRIORITY
- **Current:** Screenshots show English; India version will need Hindi/regional language support
- **Needed:** 
  - Language support: Hindi, Tamil, Telugu, Kannada (India); Spanish (US diaspora)
  - Voice content: "Daily Mitali Lesson" could be audio for lower-literacy users or on-the-go consumption
  - Metric conversions: grams/cups based on user preference
- **Refinement:** Localization strategy + voice recording plan for Mitali's lessons

### 10. **Monetization & Subscription Tiers** 💰 BUSINESS LAYER
- **Current:** Not visible in screenshots; likely planned
- **Needed:** Define tiers:
  - Free tier: Onboarding + basic condition info + read-only recipe library
  - Pro: Personalized protocols + API-integrated travel meal navigation + lab interpretation + Mitali Q&A
  - Premium: 1:1 consultations with Mitali (optional, high-touch tier)
- **Refinement:** Clarify paywall strategy + which features unlock at each tier

---

## Technical & Design Refinements

### Frontend/UX
- **Onboarding** is excellent; polish the condition selection flow to show interconnection hints
- **Results screen** (Gut Health card) needs to evolve → animated trends, quick-win suggestions ("Try fermented dhal today!")
- **Navigation** between tabs (protocols, recipes, journal, insights) should feel seamless
- **Accessibility:** Ensure high contrast on dark teal background; test color-blind modes

### Backend
- **Data architecture:** Design schemas for Conditions, Protocols, Recipes, RegionalVariants, LabMarkers
- **Personalization engine:** Rules-based (if-then logic for conditions) vs. ML-powered? Start with rules; layer ML later if needed
- **API integrations:** Restaurant data (Zomato, Uber Eats) + payment (Stripe) + WhatsApp notifications (mentioned in privacy section)
- **Analytics:** Track which conditions drive engagement, which recipes are popular, which protocols convert (if paid)

### Content Management
- **Mitali as the voice:** All protocols, insights, lessons should feel personally from her (or clearly AI-assisted)
- **Regional recipe curation:** Partner with regional food culture experts or crowdsource variants
- **Lab interpretation library:** Collaborate with functional medicine labs to ensure accuracy

---

## Launch Priorities (Phased Approach)

**Phase 1 (MVP - India):** 
- ✅ Onboarding + profile
- ✅ Condition selection + Mitali's protocols
- ✅ 180 regional recipes filtered by condition + diet type
- ✅ Basic dashboard (score cards)
- ✅ WhatsApp notifications

**Phase 2 (Post-launch - India):**
- Condition interconnection logic
- Travel meal API (Zomato)
- Lab value interpreter
- Daily Mitali Lessons (audio/video)

**Phase 3 (US Launch):**
- Localize for US cuisine + health system
- Travel meal API (Uber Eats / GrubHub)
- Insurance pathway (if targeting US market seriously)
- A/B test messaging (India diaspora vs. native US health-conscious)

**Phase 4 (GCC):**
- Halal sourcing + ingredient swaps
- Expat-specific protocols (jet lag, adjustment stress)

---

## Key Success Metrics

Track these to know if refinements are working:
- **Onboarding completion rate** (% who finish setup)
- **Protocol adoption** (% who start Mitali's recommendation)
- **Recipe engagement** (avg recipes viewed/week per user)
- **Score improvements** (% of users showing improving Gut/Condition scores over 30 days)
- **Retention** (30-day, 90-day active user rates by region)
- **NPS** (Net Promoter Score: Are users telling friends?)

---

## Design Philosophy to Preserve

- **Authority through expertise:** Mitali's voice & credentials matter. Don't bury the founder.
- **Simplicity with depth:** Easy to start, room to dig deeper (protocols, lab interpretation, interconnections)
- **Cultural respect:** Indian food wisdom ≠ Ayurvedic pseudoscience. Balance tradition with clinical evidence.
- **User empowerment:** Don't diagnose; educate and guide. Always tie recommendations to their conditions.
- **Privacy as a feature:** Keep repeating "your data is yours" — it's a differentiator.

---

## Questions for Refinement Conversations

1. **Condition interconnection:** Which condition pairs are most common in your clinic? (e.g., PCOS + Gut Health is common in Indian women)
2. **Travel meals:** Which restaurants/cuisines matter most for your target market?
3. **Lab markers:** Which 5-10 lab tests should the app interpret first?
4. **Regional variants:** How many recipe variants per dish for cultural authenticity? (e.g., 3 khichdi styles?)
5. **Monetization:** Is the goal lifestyle/health app (free + community) or premium wellness platform?

---

**Next Step:** Share this with Rork AI developer. They now have:
- Context (what makes Arogeva different)
- Current state (what's working)
- Refinement areas (what to build/improve)
- Priorities (phased roadmap)
- Design philosophy (what to preserve)

Good luck! 🌿
