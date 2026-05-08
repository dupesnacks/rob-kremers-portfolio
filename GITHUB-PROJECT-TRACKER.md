# Phase 2-5 GitHub Project Board

**View Live:** https://github.com/rkremers123/sensory-galaxy/issues

## Issue Summary

| # | Title | Estimate | Blocked By | Priority |
|---|-------|----------|-----------|----------|
| #1 | Food Logging Screen | 2 hrs | None | P0 |
| #2 | Analytics Tab | 2.5 hrs | None | P0 |
| #3 | Suggest Tab + Bridge Food Algorithm | 3 hrs | Algorithm spec | P0 |
| #4 | Design: Food Icons (100+) | 8-12 hrs | None | P1 |
| #5 | Design: Badge System (20) | 6-8 hrs | None | P1 |
| #6 | Design: Points Balancing | 2-3 hrs | Beta feedback | P2 |
| #7 | Feature: Onboarding Redesign | 2 hrs | None | P1 |
| #8 | Feature: Parent Education | 3-4 hrs | Core UI | P1 |
| #9 | Feature: Explorer Cosmetics | 3-4 hrs | Cosmetics spec | P1 |
| #10 | Bug Fixes & Testing | 1-2 hrs | All features | P0 |

## Implementation Order (Suggested)

### Phase 2-5.1: Core Screens (Week 1)
1. Issue #1: Food Logging Screen (2 hrs)
2. Issue #2: Analytics Tab (2.5 hrs)
3. Issue #7: Onboarding Redesign (2 hrs)
- **Subtotal: 6.5 hours**
- **Outcome:** Three core screens working, onboarding collecting safe foods data

### Phase 2-5.2: Bridge Food Algorithm (Week 1-2)
1. Create algorithm spec (4 hrs) - see BRIDGE-FOOD-ALGORITHM.md
2. Issue #3: Suggest Tab + Bridge Food Algorithm (3 hrs)
- **Subtotal: 7 hours**
- **Outcome:** Recommendation engine live, feeding 3 daily suggestions

### Phase 2-5.3: Design Assets (Week 2-3, parallel)
1. Issue #4: Food Icons (100+) (8-12 hrs)
2. Issue #5: Badge System (20 badges) (6-8 hrs)
3. Issue #9: Explorer Cosmetics specs (reference, not code) (0 hrs)
- **Subtotal: 14-20 hours**
- **Outcome:** All visual assets in place, integration ready

### Phase 2-5.4: Polish & Testing (Week 3)
1. Issue #6: Points Balancing (after beta feedback) (2-3 hrs)
2. Issue #8: Parent Education Module (3-4 hrs)
3. Issue #10: Bug Fixes & Testing (1-2 hrs)
- **Subtotal: 6-9 hours**
- **Outcome:** Beta-ready build

## Total Effort Estimate
- **Code:** 6.5 + 7 + 6-9 = **19.5-22.5 hours**
- **Design:** 14-20 hours
- **Total: 33.5-42.5 hours** (~1 week intensive or 2 weeks half-time)

## Daily Tracking

You can query the board status anytime with:
```bash
gh issue list --state open --limit 100
gh issue view <number>
gh issue edit <number> --add-label "in-progress"
```

## Next Steps
1. Create GitHub Project Board (manual via github.com/rkremers123/sensory-galaxy/projects)
2. Assign issues to columns: Backlog → In Progress → Testing → Done
3. Start with Issue #1 (Food Logging Screen)
4. Create BRIDGE-FOOD-ALGORITHM.md spec doc (linked in Issue #3)

