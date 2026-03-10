# Expanded Food Database + LLM Guardrails

## Current Foods in App (62 items)

Based on FoodDatabase.swift:
- Chicken Nugget, Turkey Slices, Ground Beef, Salmon, Fish Stick, Shrimp
- White Bread, Whole Wheat Bread, Toast, Pasta, Rice, Mac & Cheese
- Scrambled Eggs, Fried Eggs, Cheese, Yogurt, Cottage Cheese, Milk
- Peanut Butter, Jelly, Honey, Butter
- Apple, Banana, Orange, Grapes, Strawberries, Blueberries, Watermelon, Cantaloupe
- Carrot, Broccoli, Green Beans, Corn, Peas, Spinach, Cucumber
- Crackers, Pretzels, Potato Chips, Cheerios, Rice Crispy Treats
- Hamburger Bun, Hot Dog Bun, Pizza (Cheese)
- Peanut Butter & Jelly Sandwich
- Cheese Quesadilla, Hot Dog, Taco, Grilled Cheese, PB&J Sandwich
- Sweet Potato Fries, Regular Fries
- Mashed Potatoes, Baked Potato
- Pancakes, Waffles, French Toast
- Granola, Oatmeal
- Chicken Breast, Turkey Breast
- Mozzarella Sticks, Fish Sticks
- Deli Meat
- Apple Sauce
- Orange Slices
- Cheese Pizza
- And ~12 more

---

## EXPANDED Food Database (100+ foods)

### PROTEINS (20+ items)
- Chicken Nugget, Chicken Breast, Chicken Tenders, Rotisserie Chicken
- Turkey Slices, Turkey Breast, Turkey Meatball
- Ground Beef, Beef Meatball, Hamburger Patty, Steak (cubed/tender)
- Salmon, Fish Stick, Cod, Tilapia, Shrimp, Tuna
- Bacon, Deli Meat (Ham, Turkey, Roast Beef)
- Eggs (Scrambled, Fried, Boiled, Scrambled Soft)
- Tofu, Tempeh

### DAIRY & ALTERNATIVES (15+ items)
- Cheese (Cheddar, Mozzarella, American, Swiss, Parmesan)
- Yogurt (Plain, Vanilla, Fruit)
- Cottage Cheese
- Milk
- Butter
- Cream Cheese
- Greek Yogurt
- Cheese Slices
- String Cheese
- Mozzarella Sticks

### GRAINS & BREAD (18+ items)
- White Bread, Whole Wheat Bread, Rye Bread
- Crackers (Goldfish, Animal, Saltines)
- Pretzels, Pretzel Rods, Pretzel Crisps
- Rice (White, Brown, Sticky)
- Pasta (Spaghetti, Penne, Elbow, Mac)
- Cereal (Cheerios, Rice Krispies, Frosted Flakes, Lucky Charms)
- Oatmeal, Granola
- Toast (White, Wheat, Sourdough)
- English Muffin
- Bagel
- Dinner Roll, Hamburger Bun, Hot Dog Bun
- Waffle, Pancake, French Toast

### FRUITS (20+ items)
- Apple, Apple Slices, Apple Sauce
- Banana, Banana Chips
- Orange, Orange Slices, Mandarin
- Grapes (Red, Green, Seedless)
- Strawberries, Blueberries, Raspberries, Blackberries
- Watermelon, Cantaloupe, Honeydew
- Peach, Pear, Plum
- Dried Fruit (Raisins, Cranberries, Apricots)
- Fruit Cup (Canned)
- Pineapple

### VEGETABLES (15+ items)
- Carrot, Carrot Sticks, Carrot Coins
- Broccoli, Broccoli Florets
- Green Beans, Snap Peas
- Corn, Corn Kernels
- Peas
- Spinach, Kale (cooked/soft)
- Cucumber, Cucumber Slices
- Tomato, Tomato Slices
- Bell Pepper (mild)
- Zucchini
- Sweet Potato, Sweet Potato Fries
- Regular Potato, Fries, Baked Potato, Mashed Potatoes, Tater Tots
- Cauliflower (soft/roasted)

### COMBINATION MEALS (12+ items)
- Pizza (Cheese, Pepperoni, Veggie)
- Hamburger, Cheeseburger
- Hot Dog
- Taco (Soft Shell, Hard Shell)
- Grilled Cheese Sandwich
- Peanut Butter & Jelly Sandwich
- Turkey Sandwich
- Pasta with Sauce (Mild)
- Mac & Cheese
- Quesadilla (Cheese, Chicken)
- Burrito (Mild)
- Rice & Beans

### SNACKS & TREATS (15+ items)
- Potato Chips, Baked Chips, BBQ Chips, Salt & Vinegar Chips
- Goldfish, Animal Crackers
- Fruit Snacks, Gummy Bears, Gummy Worms
- Granola Bar, Cereal Bar, Protein Bar
- Cookie (Chocolate Chip, Sugar Cookie)
- Brownie, Rice Krispie Treat
- Fruit Leather, Fruit Roll-Up
- Trail Mix, Nuts & Raisins
- Popcorn (plain, buttered, cheese)
- Tortilla Chips, Salsa (mild)

### BEVERAGES (non-solid options - LIMITED for app focus)
- Milk, Chocolate Milk
- Orange Juice, Apple Juice, Fruit Juice
- Smoothie (plain fruit)
- Water
- Yogurt Drink

---

## LLM GUARDRAILS (Prevent "Salty Liquid" Problem)

### FORBIDDEN COMBOS (Never suggest these)
```
- Salty + Liquid (liquids are rarely eaten as salty)
- Bitter + any (kids won't accept bitter)
- Sour + Liquid (very rare - sour drinks unusual for selective eaters)
- Multiple bold flavors combined (too complex)
- Texture + Temperature mismatch (e.g., crunchy + hot rarely works)
```

### VALID COMBO EXAMPLES (DO suggest these)
```
Crunchy + Salty + Room Temp → Pretzels, Chips, Crackers ✅
Soft + Bland + Warm → Mac & Cheese, Mashed Potatoes ✅
Soft + Sweet + Cold → Yogurt, Apple Sauce ✅
Crunchy + Sweet + Room Temp → Graham Crackers, Cereal ✅
Chewy + Sweet + Room Temp → Gummy Bears, Fruit Leather ✅
```

### CONSTRAINT RULES FOR LLM PROMPT
```
1. ONLY suggest foods from the approved food database (100+ items above)
2. NEVER suggest "liquid" foods as primary recommendations
3. NEVER combine more than 2 flavor profiles (e.g., don't suggest "spicy salty sour")
4. AVOID rare/unusual combos - stick to common kid-friendly pairings
5. When suggesting salty foods, make them SOLID (pretzels, chips, crackers)
6. When suggesting sour, pair with sweet (strawberries, oranges - natural acids)
7. When suggesting bitter, it must be MILD (carrots cooked soft, not raw broccoli)
8. Temperature rule: Hot foods should be soft (mac & cheese, warm potatoes)
9. Cold foods should be soft or naturally frozen (yogurt, fruit, juice pops)
10. VALIDATE suggested food exists in database before returning to parent
```

---

## Updated LLM System Prompt (Bridge Food Suggestions)

```
You are a Sensory Feeding Expert. Suggest bridge foods for selective eaters using the SOS Approach.

CHILD'S PROFILE:
- Safe foods logged: [list with attributes]
- Sensory patterns detected: [texture, flavor, temp preferences]
- Foods to avoid: [any flagged foods]

APPROVED FOOD DATABASE:
[100+ foods above]

CONSTRAINTS:
1. ONLY suggest foods from approved database
2. Match 1-2 sensory attributes (not 3+)
3. Avoid rare/nonsensical combos
4. Suggest SOLID foods, not liquids
5. Follow valid combo examples above
6. Explain WHY the food bridges (which attributes match)

OUTPUT FORMAT:
{
  "suggestion": "Food name",
  "reason": "Matches their crunchy + salty preference like [safe food]",
  "attributes": "Crunchy, Salty, Room Temp",
  "risk": "Low/Medium/High",
  "next_step": "How to introduce it"
}

Example:
Child ate: Crackers (crunchy, salty, room temp)
Suggestion: "Pretzels" (same attributes, familiar texture progression)
NOT "Salty liquid soup" (violates constraints)
```

---

## Implementation for Rork

### Database Update
Replace current 62 foods with 100+ food list above.

### LLM Integration
Add constraint validation:
```
// Pseudocode
function suggestBridgeFood(childProfile) {
  // 1. Detect patterns from safe foods
  const patterns = analyzePatterns(childProfile.safeFoods)
  
  // 2. Filter approved database
  const candidates = FOOD_DATABASE.filter(food => 
    !FORBIDDEN_COMBOS.includes(food.attributes)
  )
  
  // 3. Call Qwen with guardrails
  const suggestion = await qwenBridgeFood({
    profile: childProfile,
    patterns: patterns,
    approvedFoods: candidates,
    constraints: GUARDRAILS
  })
  
  // 4. Validate suggestion exists in database
  if (!FOOD_DATABASE.find(f => f.name === suggestion.food)) {
    return "Log more foods to unlock bridge suggestions"
  }
  
  return suggestion
}
```

### Cost Impact
- Expanded database = no API cost increase
- Constraint validation = negligible (client-side rules)
- LLM calls = same (still ~250K/year at threshold)
- **Total stays under $2,150/year** ✅

---

## Result

✅ **No more "salty liquid" suggestions**
✅ **All suggestions use real foods in app**
✅ **LLM stays creative within safe guardrails**
✅ **Parents see smart, thoughtful recommendations**

