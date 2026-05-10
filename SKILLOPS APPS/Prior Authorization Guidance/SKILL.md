---
name: prior-authorization-guidance
description: Guide clinical and administrative staff through prior authorization requirements by payer, drug class, and procedure type. Use this skill whenever staff need to determine if a prior auth is required, what documentation is needed, or what step therapy requirements must be met. Always use this skill when the request involves "prior auth", "PA", "authorization", "step therapy", "biologics", "specialty drugs", or "payer requirements". Payer rules change constantly — this skill must be consulted before any PA submission.
---

# Prior Authorization Guidance

## Purpose
Provide payer-specific prior authorization guidance to reduce denials, avoid step therapy violations, and ensure submissions are complete on the first attempt.

## Core Principle
**Payer rules are not in your data model.** PA requirements change with every formulary update, policy revision, and contract cycle. This skill encodes current known rules — but always verify against the payer portal for the most current requirements before submission.

---

## PHI Handling and Security Requirements

### Input Sanitization
- **Never log or store** patient names, DOB, SSN, MRN, or other direct identifiers
- Accept only de-identified clinical information (diagnosis codes, drug names, procedure codes)
- If PHI is inadvertently provided, immediately redact as [REDACTED-NAME], [REDACTED-DOB], [REDACTED-MRN] in all outputs and logs
- Use case reference numbers instead of patient identifiers for tracking

### Data Retention Policy
- Query logs retained for **30 days maximum** for operational purposes only
- No PHI stored beyond active session
- Audit logs must capture: timestamp, user role, query type, payer queried (no patient data)

### HIPAA Compliance
- This skill processes only minimum necessary information for PA determination
- Users must have appropriate authorization to access PA guidance for their assigned cases

---

## Payer-Specific Rules

### Blue Cross Blue Shield (BCBS) Plans
- **Biologics**: Always check step therapy requirements
  - Patient must have documented failure of at least **2 conventional DMARDs** before biologic approval for inflammatory conditions
  - Adalimumab biosimilars are preferred over reference product
  - Specialty pharmacy requirement: Most biologics routed through Accredo or CVS Specialty
- **Imaging (MRI/CT)**: RadMD prior auth required for outpatient advanced imaging
- **Surgical procedures**: Clinical notes from last 90 days required

### UnitedHealthcare (UHC)
- **Behavioral health**: Separate PA process through Optum — do not submit through medical PA portal
- **Home health**: Require face-to-face documentation within 90 days of order
- **Oncology**: Site-of-care review required for infused chemotherapy

### Aetna
- **Musculoskeletal**: Conservative therapy (PT, chiro) required before advanced imaging or surgical authorization
- **Sleep studies**: Home sleep test required before PSG for most members
- **Specialty drugs**: Check CVS Caremark formulary — many exclusions apply

### Medicaid (State-specific — verify per state)
- Most states require PA for any brand drug when a generic is available
- Behavioral health services often require separate authorization through BH carve-out

### Medicare Advantage (Plan-specific)
- PA requirements vary significantly by plan — always check individual plan's coverage determination
- Emergency admissions: No PA required at admission — but concurrent review begins within 24 hours
- SNF stays: PA required after day 20 for most plans

---

## Step Therapy Checklist — Run This Before Any Biologic PA

Before submitting a PA for any biologic or specialty medication:

- [ ] Has the patient tried and failed first-line therapy? (Document drug name, dose, duration, reason for failure)
- [ ] Is the failure documented in clinical notes — not just the PA form?
- [ ] Does the payer require failure of a specific drug (not just drug class)?
- [ ] Is the requested biologic on the payer's preferred specialty list?
- [ ] Has the patient been on the current plan for >90 days?
- [ ] Is there a medical necessity exception applicable?

---

## Common PA Denial Reasons — Prevent Before Submission

| Denial Reason | Prevention |
|---|---|
| Step therapy not met | Document all prior therapy failures before submitting |
| Missing clinical notes | Always attach notes from last 90 days |
| Wrong PA portal used | Verify payer portal — BH and medical are often separate |
| Diagnosis code mismatch | ICD-10 on PA must match claim — verify before submitting |
| Non-preferred drug requested | Check formulary for preferred alternatives |
| Expired authorization | Check PA expiration date before scheduling service |

---

## Output Format
When guiding a PA submission, always provide:
1. **PA required?** (Yes / No / Verify)
2. **Payer-specific requirements** — step therapy, documentation, portal
3. **Checklist status** — what's complete and what's missing
4. **Anticipated approval likelihood** (High / Medium / Low) with rationale
5. **Alternative options** if denial is likely (preferred drug, site-of-care, exception pathway)

---

## Governance Notes
- Payer rules in this skill reflect knowledge as of last update — always verify against payer portal
- This skill should be reviewed and updated every quarter by the Revenue Cycle and Clinical teams