# Risk Register

Last updated: 2026-06-13
Owner: OpenClaw
Status: SEED (baseline risks identified in brief; will expand during research)

---

## No-Go Triggers (Hard Stops)

Any of these fires = immediate escalation in LOG.md + DECISIONS.md + pause/pivot signal to Rob.

| Risk ID | No-Go Trigger | Severity | Likelihood | Owner | Status | Evidence / Detection |
|---------|---|----------|-----------|-------|--------|---|
| **NG-001** | No manufacturer can document formula/testing | Critical | Unknown (Phase 2) | OpenClaw | OPEN | Check batch records, 3rd-party testing, COAs during supplier outreach |
| **NG-002** | No product liability insurance available for cosmetic peptides | Critical | Medium-High | OpenClaw | OPEN | Get broker quotes Phase 9; peptide positioning may limit insurability |
| **NG-003** | Product needs drug-like claims to be viable (can't differentiate as cosmetic) | Critical | Medium | OpenClaw | OPEN | If Safe claims (CLAIMS_GUARDRAIL.md) insufficient to drive interest; flag in Phase 10 validation |
| **NG-004** | Supplier refuses to provide batch records / traceability | Critical | Medium | OpenClaw | OPEN | Mandate in Phase 2 outreach; non-negotiable for compliance + liability |
| **NG-005** | MOQ forces excessive upfront risk (>$15k inventory investment before validation) | Critical | Medium | OpenClaw | OPEN | Get MOQ + lead time Phase 2; if >500 units @ COGS, flag in DECISIONS.md |
| **NG-006** | Product feels generic vs. Amazon private-label competitors | High | Medium | OpenClaw | OPEN | Phase 3 competitive research; if no differentiation, escalate Outcome B pivot |
| **NG-007** | CAC too high + weak repeat purchase signals in Phase 10 validation | High | Medium | OpenClaw | OPEN | Need 10+ interviews showing >30% likelihood of repeat; if fails, no-go |
| **NG-008** | Claims drift toward medical/therapy language in copy/marketing | Critical | Medium-High | OpenClaw | OPEN | CLAIMS_GUARDRAIL.md enforcement in all drafts; any violation → DECISIONS.md flag |
| **NG-009** | Rob uncomfortable with reputational exposure (peptide gray-market association) | High | Low-Medium | Rob | OPEN | Subjective; Rob signals in DECISIONS.md feedback |
| **NG-010** | Excessive family/time stress (work-life balance breaks) | High | Low | Rob | OPEN | Rob signals; take to DECISIONS.md for Outcome B/C discussion |
| **NG-011** | Attorney says model isn't defensible (cosmetic positioning risky) | Critical | Low-Medium | ChatGPT/Attorney | OPEN | Phase 1 legal review; if unfavorable, pivot to drug pathway or no-go |
| **NG-012** | Platform stack looks unstable due to claims (payment processor blocks GHK-Cu) | High | Medium | OpenClaw | OPEN | Verify Stripe/Shopify accept; if blocked, research alternative payment (Wise, ACH direct) |
| **NG-013** | Quality unverifiable (supplier provides no testing, third-party labs won't test) | Critical | Low-Medium | OpenClaw | OPEN | Phase 2 supplier due diligence; if no testing path, NG-001 triggered |

---

## Active Risks (Being Monitored)

| Risk ID | Risk | Severity | Likelihood | Mitigation | Owner | Status | Target Resolution |
|---------|------|----------|-----------|-----------|-------|--------|---|
| **R-001** | **Regulatory uncertainty on GHK-Cu cosmetic claims** | High | Medium | Phase 1: Consult attorney on ingredient status (CPTPP, GDPR, FDA cosmetic vs. drug); map safe-claim boundaries; document in ASSUMPTIONS.md | OpenClaw | OPEN | Post-Phase 1 (by Jun 20) |
| **R-002** | **Supplier capacity/reliability unknown** | High | High | Phase 2: Contact 10+ candidates; prioritize those with existing cosmetic lines + third-party testing; check references | OpenClaw | OPEN | Post-Phase 2 supplier responses (by Jun 24) |
| **R-003** | **Ingredient sourcing costs not validated** | Medium | High | Phase 2: Request pricing on GHK-Cu raw material + formula cost; model against $49–$69 retail band | OpenClaw | OPEN | During Phase 8 financial model (by Jun 28) |
| **R-004** | **Customer interest unvalidated (is GHK-Cu a real demand driver?)** | High | Medium | Phase 10: Run 10+ customer interviews with skin-health audience; ask about peptide awareness + willingness to try cosmetic GHK-Cu | OpenClaw | OPEN | Post-Phase 10 (by Jul 05) |
| **R-005** | **Amazon private-label commoditization** | Medium | Medium | Phase 3: Research competitive landscape; identify positioning gaps (premium/minimalist, education-driven, community) vs. generic peptide serums | OpenClaw | OPEN | Post-Phase 3 (by Jun 26) |
| **R-006** | **Adverse event liability (even rare, can be reputational + financial)** | High | Low | Phase 7: Draft adverse-event SOP + escalation process; Phase 9: Verify insurance covers; keep batch records for traceability | OpenClaw | OPEN | Post-Phase 7 (by Jul 02) |
| **R-007** | **Payment processor (Stripe/Shopify) may flag peptide positioning** | Medium | Medium | Phase 2: Parallel research; contact processor compliance teams early; prepare alternative (Wise, Gumroad if needed) | OpenClaw | OPEN | By Jun 24 |

---

## Closed Risks (Resolved)

(None yet — project in seed phase.)

---

## Risk Review Cadence

- **Weekly:** OpenClaw reviews risks in LOG.md, updates status.
- **Trigger-based:** Any new risk discovered → add to Risk Register immediately + flag in DECISIONS.md.
- **Monthly:** Rob + ChatGPT review DECISIONS.md items tied to open risks.

---

## Escalation Path

**Any No-Go Trigger fires →**
1. OpenClaw documents in Risk Register (date, evidence).
2. OpenClaw writes DECISIONS.md entry with context + recommendation (Outcome A/B/C).
3. OpenClaw flags in LOG.md entry (newest on top).
4. Rob reviews; decides go/pivot/no-go.

---

## Notes

- **No-Go Triggers are binary:** When evidence suggests trigger has fired, pause project and escalate immediately. Don't wait for perfect certainty.
- **Tolerances:** If MOQ >$15k, Supplier score <2/5, or Insurance unavailable, treat as high-probability no-go unless explicitly overridden by Rob.
- **Audit trail:** Keep Risk Register + DECISIONS.md in sync. Every decision tied to a risk should reference the risk ID.

