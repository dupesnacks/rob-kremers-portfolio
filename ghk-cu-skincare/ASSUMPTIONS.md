# Assumptions Log (Phase 0)

Last updated: 2026-06-13
Owner: OpenClaw
Status: SEED (to be expanded with Phase 1 attorney findings)

---

## Verified Assumptions

(Assumptions with evidence or clear foundation)

| Assumption | Evidence | Risk | Owner | Status |
|-----------|----------|------|-------|--------|
| GHK-Cu (Copper Tripeptide-1) is a cosmetic-grade ingredient available in U.S. supply chains | Ingredient widely available from global suppliers (Spec Chem, Actives, others); used in existing skincare products | Low | OpenClaw | ✅ VERIFIED |
| Cosmetic claims "improves appearance of fine lines" are defensible under FTC guidance | FTC Guides on Substantiation; common in skincare marketing | Low | ChatGPT (pending attorney confirmation) | ✅ ASSUMED |
| $49–$69 retail price band is viable for D2C premium serum | Comparable peptide serums (Ordinary, ordinary-adjacent brands) retail $30–80 | Low | OpenClaw | ✅ ASSUMED |
| U.S. contract manufacturers exist with GHK-Cu formulation experience | Seed list of 10 candidates (Pravada, Indigo, etc.) identified | Low | OpenClaw | ✅ ASSUMED |
| Product liability insurance for cosmetic skincare is obtainable | Standard product lines insure easily; peptide positioning may add complexity | Medium | OpenClaw (Phase 9 broker verification) | ⏳ PENDING |

---

## Assumed (Needing Verification)

(Assumptions baked into the project plan that require validation but not yet confirmed)

| Assumption | Rationale | Verification Method | Priority | Timeline |
|-----------|-----------|---|----------|---|
| GHK-Cu positioning as "cosmetic" (not "drug" or "peptide therapy") is FTC-defensible and won't trigger FDA reclassification | Customer interest in GHK-Cu is high; strict cosmetic framing avoids drug definition per 21 CFR 700.3 | Attorney review of CLAIMS_GUARDRAIL.md + FTC/FDA guidance; test edge-case claims | CRITICAL | Phase 1 (Jun 20) |
| U.S. payment processors (Stripe, Shopify, PayPal) will accept GHK-Cu skincare as cosmetic (not flagging as peptide therapy or supplement) | Cosmetics are generally low-risk for processors; peptide positioning may trigger higher scrutiny | Email compliance teams at Stripe + Shopify; review merchant category codes | HIGH | Phase 2b (Jun 24) |
| Supplier MOQ ≤1.5k units is achievable (to manage cash flow + inventory risk) | First-time D2C brand requires lean inventory; MOQ >3k units = deal-breaker risk | Supplier outreach responses; Phase 2b evaluation | HIGH | Phase 2 (Jun 24) |
| Product can be formulated to be profitable at $49–$69 retail (target: 60%+ gross margin after COGS + packaging) | Standard cosmetic margins are 50–70%; peptide actives may be higher-cost | Supplier COGS quotes + financial modeling (Phase 8) | CRITICAL | Phase 8 (Jul 04) |
| Customer demand exists for "cosmetic GHK-Cu" positioning (not drug/therapy framing) | Skincare audiences are familiar with peptides; cosmetic angle differentiates from gray-market research peptides | Customer validation interviews (Phase 10) | CRITICAL | Phase 10 (Jul 10) |
| Insurance broker can quote product liability without requiring clinical trials or FDA approval | Cosmetics don't require FDA approval; liability insurance should be standard | Phase 9 broker calls + questionnaire | HIGH | Phase 9 (Jul 08) |
| Batch record + testing documentation will be obtainable from suppliers at standard MOQ | Leading manufacturers provide COA + batch records; smaller suppliers may not | Phase 2 supplier outreach + calls | HIGH | Phase 2b (Jun 24) |
| Amazon private-label market won't immediately commoditize the product (i.e., we have 6–12 month window for differentiation) | Amazon moves fast; premium positioning + customer education (content) can sustain differentiation early | Phase 3 competitive research + Phase 6 marketing strategy | MEDIUM | Phase 3 (Jun 26) |

---

## Unknown (Needs Attorney or Supplier Confirmation)

(Unknowns that block decisions; must be resolved before proceeding past phases)

| Unknown | Impact | Resolution | Owner | Timeline |
|---------|--------|-----------|-------|---|
| Will FTC or FDA challenge cosmetic GHK-Cu claims if posted on social media or Amazon? | CRITICAL: Could trigger enforcement, product hold, or rebranding | Attorney review of competitive claims landscape + FTC enforcement history; ask ChatGPT for case analysis | OpenClaw + ChatGPT | Phase 1 (Jun 20) |
| What is the actual GHK-Cu sourcing story? (Is it synthesized, extracted, recombinant, etc.? Does sourcing affect claims?) | MEDIUM: May affect supplier certification + ingredient transparency story | Request from suppliers during Phase 2 outreach; verify with ingredient supplier (e.g., Spec Chem) | OpenClaw | Phase 2b (Jun 24) |
| Do ingredient certifications (organic, vegan, cruelty-free) conflict with cosmetic positioning? | LOW: Cosmetics can be organic/vegan; not a blocker, but may limit supplier pool | Ask suppliers during Phase 2 about certification options | OpenClaw | Phase 2 (Jun 24) |
| What adverse event reporting is required for cosmetic skincare? | HIGH: Could affect SOP design + liability exposure | Attorney Q: Must read FDA cosmetic adverse event guidance (21 CFR 720.9) + FTC guidance; document in OPERATIONS.md Phase 7 | OpenClaw + Attorney | Phase 1–7 |
| Is a cosmetic GHK-Cu product insurable if it contains bioactive peptides? | CRITICAL: No insurance = hard no-go (NG-002) | Phase 9 broker calls; prepare sample product liability application with compliance docs | OpenClaw | Phase 9 (Jul 08) |
| How much customer demand is there for a $50+ cosmetic peptide serum? (CAC, repeat-purchase likelihood?) | CRITICAL: Product viability depends on this; Phase 10 gate | Run 10+ interviews with skincare + wellness audience; ask about willingness to try, price sensitivity, repeat likelihood | OpenClaw | Phase 10 (Jul 10) |

---

## Needs Attorney or Supplier Confirmation

(Items that require expert input but are parked until Phase 1–2 kicks off)

| Item | What We Need | Why | Timeline |
|------|------|---|---|
| **FTC/FDA Claim Boundaries for GHK-Cu** | Letter or memo from attorney re: safe claims vs. risky claims; specific guidance on edge cases ("supports healthy-looking skin" vs. "promotes collagen") | CLAIMS_GUARDRAIL.md is draft; attorney review locks down defensibility | Phase 1 (Jun 20) |
| **Cosmetic Adverse Event Reporting SOP** | Attorney guidance on 21 CFR 720.9 requirements + best practices for cosmetic skincare brands | Required for Phase 7 SOP + insurance application | Phase 1–7 |
| **Supplement vs. Cosmetic Positioning** | Clarification: Is GHK-Cu a supplement if ingested vs. cosmetic if topical? (Ensures we're not accidentally creating a supplement product) | CRITICAL: Prevents regulatory misclassification | Phase 1 (Jun 20) |
| **Supplier Due Diligence Checklist** | Attorney template for evaluating suppliers: what questions to ask, what docs to request, red flags | Inform Phase 2 supplier selection + supplier SOP | Phase 2b (Jun 24) |
| **Insurance & Liability Framework** | Attorney guidance on product liability limits, coverage terms, exclusions; what terms to negotiate with broker | Phase 9 inputs + supplier contracts | Phase 1–9 |

---

## Verification Status by Phase

- **Phase 0 (Setup, complete):** Project scope, team roles, memory architecture confirmed ✅
- **Phase 1 (Jun 15–20, in progress):** Attorney review → lock down CLAIMS_GUARDRAIL.md, resolve legal unknowns
- **Phase 2 (Jun 20–30, pending Phase 1):** Supplier outreach → verify MOQ, COGS, batch records; lock down supply chain assumptions
- **Phase 3 (Jun 20–26, parallel):** Competitor research → verify differentiation window + pricing strategy
- **Phases 4–10 (staggered, Jun 25–Jul 10):** Product, brand, marketing, ops, finance, insurance, validation → each phase builds on prior phases' assumptions

---

## Red Flag Review

| Red Flag | Trigger | Action |
|----------|---------|--------|
| Attorney says GHK-Cu cosmetic claims are indefensible | Phase 1 (Jun 20) | Escalate NG-011 in RISK_REGISTER.md; discuss Outcome B (pivot) in DECISIONS.md |
| Suppliers all quote MOQ >2k units or COGS >$15/unit | Phase 2b (Jun 24) | Flag NG-005 (excessive MOQ risk); reassess unit economics |
| No suppliers have prior GHK-Cu experience or won't provide batch records | Phase 2b (Jun 24) | Flag NG-001 + NG-004; consider generic peptide alternative or no-go |
| Insurance broker refuses quote or quotes 10%+ premium for peptide positioning | Phase 9 (Jul 08) | Flag NG-002 (no insurance); pivot or no-go |
| Customer interviews show <30% repeat-purchase likelihood or CAC >$30 | Phase 10 (Jul 10) | Flag NG-007 (weak repeat purchase); reassess viability |

---

## Next Steps (Phase 1, Jun 15–20)

1. OpenClaw: Schedule attorney call to review CLAIMS_GUARDRAIL.md + supply list of edge-case claims for legal opinion.
2. OpenClaw: Prepare attorney questionnaire (adverse events, supplement vs. cosmetic, claim substantiation).
3. ChatGPT: Review FTC enforcement cases for cosmetic peptide products (search: "GHK-Cu" + "FTC cosmetic claims").
4. OpenClaw: Document attorney findings in DECISIONS.md; update ASSUMPTIONS.md "Verified" section.
5. OpenClaw: Update SCORECARD.md legal defensibility score based on attorney feedback.

---

## Notes for Rob

- **Decision point:** If attorney says cosmetic positioning is risky, we discuss Outcome B (content/community/brand angle) or pivot to drug pathway (requires clinical trials). This is a Phase 1 decision gate.
- **Green light:** If attorney confirms CLAIMS_GUARDRAIL.md is defensible, we proceed to Phase 2 supplier outreach (Jun 20+).

