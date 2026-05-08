# Bridge Food Recommendation Algorithm Specification

**Purpose:** Generate safe, progressive food recommendations for children with selective eating based on multi-dimensional sensory analysis.

**Philosophy:** Rules-based (not LLM) for transparency, cost, and App Store compliance.

---

## 1. Sensory Profile Model (6 Dimensions)

Every food is mapped across these sensory axes:

### 1.1 Texture Dimension (0-10 scale)
- **0:** Pure liquid (juice, milk)
- **2:** Soft/mushy (applesauce, oatmeal)
- **4:** Soft/chewy (bread, pasta)
- **6:** Mixed (chicken nuggets: crunchy exterior, soft interior)
- **8:** Crunchy (chips, apples, carrots)
- **10:** Hard/brittle (raw carrot, nuts)

**Also track:** Mouthfeel variability (uniform vs. mixed texture in same bite)

### 1.2 Flavor Dimension (5 sub-dimensions)
- **Sweet:** 0-10 (none to very sweet)
- **Salty:** 0-10 (none to very salty)
- **Savory:** 0-10 (umami/meaty)
- **Sour:** 0-10 (acidic)
- **Bitter:** 0-10 (astringent)

**Dominant flavor combination:** e.g., "salty-savory," "sweet," "plain"

### 1.3 Temperature Dimension
- **Cold:** 0-5°C (ice cream, cold juice)
- **Cool:** 5-15°C (yogurt, cheese)
- **Room temp:** 15-25°C (bread, cookies)
- **Warm:** 25-45°C (warm applesauce)
- **Hot:** 45°C+ (soup, oatmeal)

**Track probability distribution:** "80% warm, 20% room temp" (food served multiple ways)

### 1.4 Color Dimension
- **Red:** tomatoes, strawberries, watermelon
- **Orange:** carrots, sweet potato, orange
- **Yellow:** banana, corn, cheese
- **Green:** broccoli, peas, lettuce
- **Brown:** chicken, toast, chocolate
- **White:** rice, milk, bread
- **Mixed/Multi-color:** pizza, casseroles

**Track color intensity:** pale vs. bright

### 1.5 Mouthfeel Dimension
- **Juicy:** releases liquid (watermelon, grapes)
- **Dry:** absorbs moisture (crackers, bread)
- **Creamy:** smooth, coating (peanut butter, yogurt)
- **Crispy:** shatters/crunches (chips, cookies)
- **Tender:** cuts easily (cooked meat, banana)
- **Chewy:** requires sustained chewing (gummy, taffy)

### 1.6 Preparation Method Dimension
- **Raw:** no heat (apple, carrot, lettuce)
- **Cooked (boiled):** soft, texture lost (peas, potatoes)
- **Cooked (baked):** dry, structured (bread, cookies)
- **Cooked (fried):** crunchy exterior, soft interior (chicken nuggets, fries)
- **Cooked (steamed):** gentle heat, texture preserved (broccoli, dumplings)

---

## 2. Sensory Profile Baseline Calculation

### 2.1 Input: Safe Foods Collection (Onboarding)

During onboarding, parent provides:
- **Safe foods:** 1-5 foods kid eats regularly
- **Super safe foods:** 2-3 foods kid is obsessed with (subset of safe)

Example:
```
Safe foods: [chicken nuggets, rice, toast, cheddar cheese]
Super safe foods: [chicken nuggets, toast]
```

### 2.2 Sensory Profile Weighting

Calculate weighted average sensory profile:

```
Super Safe weight: 60%
Regular Safe weight: 40%

Profile_avg = (0.60 × avg(super_safe)) + (0.40 × avg(regular_safe))
```

**Example Calculation:**

```
Chicken Nuggets:
- Texture: 6 (mixed)
- Flavor: [salty: 7, savory: 5, sweet: 1, sour: 0, bitter: 0]
- Temperature: 8 (80% warm)
- Color: 5 (brown)
- Mouthfeel: [crispy: 8, tender: 6]
- Prep: 5 (fried)

Toast:
- Texture: 4 (soft/chewy)
- Flavor: [salty: 2, savory: 3, sweet: 1, sour: 0, bitter: 0]
- Temperature: 7 (70% warm, 30% room temp)
- Color: 6 (brown)
- Mouthfeel: [crispy: 5, dry: 7]
- Prep: 4 (baked)

Rice (regular safe, not super safe):
- Texture: 2 (soft/mushy)
- Flavor: [salty: 1, savory: 2, sweet: 0, sour: 0, bitter: 0]
- Temperature: 6 (60% warm)
- Color: 8 (white)
- Mouthfeel: [dry: 6]
- Prep: 2 (boiled)

Cheese:
- Texture: 6 (soft/chewy)
- Flavor: [salty: 7, savory: 8, sweet: 0, sour: 1, bitter: 0]
- Temperature: 5 (room temp)
- Color: 7 (yellow)
- Mouthfeel: [creamy: 6]
- Prep: 1 (none)

Baseline Profile (weighted):
Texture: 0.60 × [(6+4)/2] + 0.40 × [(2+6)/2] = 0.60 × 5 + 0.40 × 4 = 4.6
Flavor (salty): 0.60 × [(7+2)/2] + 0.40 × [(1+7)/2] = 0.60 × 4.5 + 0.40 × 4 = 4.3
Flavor (savory): 0.60 × [(5+3)/2] + 0.40 × [(2+8)/2] = 0.60 × 4 + 0.40 × 5 = 4.4
Temperature: 0.60 × [(8+7)/2] + 0.40 × [6+5] = 0.60 × 7.5 + 0.40 × 5.5 = 6.6
Color: 0.60 × [(5+6)/2] + 0.40 × [(8+7)/2] = 0.60 × 5.5 + 0.40 × 7.5 = 6.3

Result: Kid is comfort with WARM (6.6/10), SLIGHTLY-SALTY (4.3), MIXED-TEXTURE (4.6), BROWN/GOLD foods (6.3)
```

**This becomes the sensory "north star."** All bridge recommendations are measured against this baseline.

---

## 3. Sensory Distance Calculation

For each potential bridge food, calculate multi-dimensional distance:

```
Distance² = w_texture × (texture_diff)² 
          + w_flavor_salty × (salty_diff)² 
          + w_flavor_savory × (savory_diff)²
          + w_flavor_sweet × (sweet_diff)²
          + w_flavor_sour × (sour_diff)²
          + w_flavor_bitter × (bitter_diff)²
          + w_temp × (temp_diff)²
          + w_color × (color_diff)²
          + w_mouthfeel × (mouthfeel_diff)²
          + w_prep × (prep_diff)²

Distance = √(Distance²)
```

**Default weights** (can be tuned):
```
w_texture: 0.15     (texture is critical)
w_flavor_salty: 0.12
w_flavor_savory: 0.12
w_flavor_sweet: 0.05 (kids are often OK with added sweetness)
w_flavor_sour: 0.05
w_flavor_bitter: 0.08 (bitter is a big turn-off)
w_temp: 0.10
w_color: 0.08
w_mouthfeel: 0.12
w_prep: 0.10
```

### 3.1 Distance Interpretation

```
Distance 0-2.5: "Super Close" - Kid can try this today
Distance 2.5-4.5: "Stretch Pick" - Challenging but doable
Distance 4.5-6.5: "Difficult" - Maybe week 3+
Distance 6.5+: "Too Far" - Don't recommend
```

---

## 4. Daily Recommendation Strategy

**Each day: Generate 3 recommendations**

### 4.1 Safe Pick (Distance < 2.5)
- Highest similarity to baseline
- Low risk, high success chance
- Role: "This is close to what you like"
- Example: Kid likes crunchy salty chicken nuggets → try crispy seaweed snacks

### 4.2 Stretch Pick (Distance 2.5-4.5)
- Moderate challenge
- One sensory dimension different (e.g., softer but same flavor)
- Role: "Try this tiny challenge"
- Example: Kid likes crunchy → try soft but similar flavor profile

### 4.3 Variety Pick (Targeting nutritional gaps)
- Identifies if kid's diet is unbalanced (e.g., only warm foods, only brown/white colors)
- Recommends different sensory category but still within 4.5 distance if possible
- Role: "Let's add more colors/textures"
- Example: Kid eats brown/white foods only → recommend yellow (sweet potato, banana) or orange (carrots)

### 4.4 Novelty Control
```
Last 7 days:  Don't recommend same food twice
Last 30 days: Lower weight by 50% if recommended before
Last 90 days: Available again at full weight
```

Prevents boredom and encourages true exploration.

---

## 5. Weekly Progression Strategy

Track kid's logged foods over a rolling week:

```
Week texture breakdown: 60% crunchy, 30% soft, 10% mixed
→ Next week: Increase soft recommendations to 40% (gradual shift)

Week color breakdown: 80% brown/white, 20% other
→ Next week: Weight colored foods 50% higher

Week flavor breakdown: 100% salty/savory, 0% sweet, 0% sour
→ Next week: Gently introduce sweet (slight dessert angle)
```

**Goal:** Gradual diversification without forcing. If kid is 80% salty, don't jump to bitter vegetables. Try sweet first (easier acceptance).

---

## 6. Explanation Templates

Every recommendation includes a human-readable explanation:

```
"Safe Pick: Crispy seaweed snacks
Why we picked this: Crunchy like chicken nuggets, salty like you like it, but something new to try. You got this!"

"Stretch Pick: Soft sweet potato fries
Why we picked this: Still warm like you like it, a little softer than usual, but pretty similar. Maybe try just one bite today?"

"Variety Pick: Yellow bell pepper slices
Why we picked this: Your week has been brown & white foods. Let's add some color! This is sweet & crunchy like things you like."
```

---

## 7. Edge Cases & Guardrails

### 7.1 Allergies & Restrictions
- If parent logs celiac/nut allergy in onboarding → blacklist those foods completely
- Never recommend foods matching known allergens

### 7.2 Food Safety
- Don't recommend choking hazards (whole nuts, hard candy) to children under 4
- Warn on high-sodium foods (limit to 1x per week if kid is young)

### 7.3 Low Safe Food Count
- If kid has fewer than 2 safe foods at start → use demographic defaults
- 3-year-olds with picky eating: Default baseline is "soft, warm, mild"
- 5-year-olds with picky eating: Default baseline is "crunchy, warm, salty"

### 7.4 Extreme Sensory Aversion
- If kid has logged 0 attempts at a sensory category (e.g., cold foods) → don't force recommendations there for first 2 weeks
- Let kid build confidence in comfort zone first

---

## 8. Algorithm Pseudo-Code

```python
def generate_daily_recommendations(kid_id: str) -> List[Recommendation]:
    """Generate 3 daily recommendations for a child."""
    
    # 1. Load kid's safe foods & calculate baseline
    safe_foods = load_safe_foods(kid_id)
    super_safe = identify_super_safe(kid_id)
    baseline_profile = calculate_baseline(safe_foods, super_safe, weights=[0.60, 0.40])
    
    # 2. Calculate distance for all foods
    all_foods = load_food_database()
    distances = {}
    for food in all_foods:
        if is_blacklisted(food, kid_id):  # Allergies, etc.
            distances[food] = float('inf')
        else:
            distances[food] = calculate_distance(food.sensory_profile, baseline_profile)
    
    # 3. Apply novelty control
    recent_foods = get_foods_logged_last_7_days(kid_id)
    for food in recent_foods:
        distances[food] = float('inf')  # Don't recommend again this week
    
    recent_month = get_foods_logged_last_30_days(kid_id)
    for food in recent_month:
        distances[food] *= 1.5  # Lower weight (higher distance = less preferred)
    
    # 4. Generate Safe Pick
    safe_pick = min([f for f in all_foods if distances[f] < 2.5], 
                    key=lambda f: distances[f])
    
    # 5. Generate Stretch Pick
    stretch_options = [f for f in all_foods if 2.5 <= distances[f] <= 4.5]
    stretch_pick = random.choice(stretch_options)  # Vary for engagement
    
    # 6. Generate Variety Pick
    week_profile = analyze_week_foods(kid_id)
    if week_profile.color_diversity < 0.3:  # Low color diversity
        variety_pick = find_different_color(baseline_profile, distances)
    elif week_profile.texture_diversity < 0.4:  # Low texture diversity
        variety_pick = find_different_texture(baseline_profile, distances)
    else:
        variety_pick = random.choice([f for f in all_foods if 2.5 <= distances[f] <= 5.5])
    
    # 7. Generate explanations
    return [
        Recommendation(safe_pick, "Safe Pick", explanation_safe()),
        Recommendation(stretch_pick, "Stretch Pick", explanation_stretch()),
        Recommendation(variety_pick, "Variety Pick", explanation_variety())
    ]
```

---

## 9. Implementation Checklist

- [ ] Sensory profile database: Rate all 100+ foods across 6 dimensions
- [ ] Weighting parameters: Tune distances to match expected outcomes (alpha testing)
- [ ] Explanation templates: Write 20+ variations per recommendation type
- [ ] Blacklist system: Build allergen/restriction UI & storage
- [ ] Distance calculator: Implement multi-dimensional math
- [ ] Novelty control: Implement food logging history
- [ ] Weekly analysis: Calculate diversity metrics
- [ ] API endpoint: `/api/recommendations/:kidId` → returns 3 picks + explanations
- [ ] UI integration: Display recommendations with explanations in Suggest Tab
- [ ] Testing: Alpha test with beta families (tune weights based on real data)

---

## 10. Notes for Future Iterations

1. **A/B Testing:** Once live, track which recommendation type (Safe/Stretch/Variety) leads to actual food tries. Weight higher-performing types.

2. **Personalization:** After 4 weeks of data, adjust weights per child. Some kids respond better to texture challenges, others to flavor.

3. **LLM Optional:** If algorithm proves solid in Phase 1, consider LLM in Phase 2 as a "creative suggestion" layer (always below rules-based recommendations, never primary).

4. **Therapist Integration:** Share these distance scores with OTs/speech therapists for professional guidance.

5. **Data Privacy:** All calculations happen on-device. No sensory data sent to servers (unless parent explicitly shares with therapist).

