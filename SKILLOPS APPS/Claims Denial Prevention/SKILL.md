---
name: denial-prevention
description: Flag claims with high denial risk before submission using payer behavior patterns and coding rules. Use this skill whenever reviewing claims before submission, analyzing denial trends, auditing coding accuracy, or building pre-submission claim edits. Always use this skill when the request involves "denials", "claim submission", "coding review", "clean claim", "E&M coding", "procedure codes", or "pre-billing review". This skill catches what coders and systems miss.
---

# Denial Prevention

## Purpose
Identify claims at high risk of denial before submission — using payer behavior patterns, coding rules, and documentation requirements that are not captured in standard claim edits.

## Core Principle
**Standard claim edits catch format errors. This skill catches judgment errors.** The most expensive denials are the ones that pass system edits but fail medical necessity or documentation review.

---

## Data Security & Privacy Requirements

### PHI Handling
- **All patient identifiers must be masked** — use claim ID, not patient name/DOB/SSN in outputs
- **Minimum necessary rule**: Only access claim data elements required for denial risk assessment
- **Data masking format**: Patient ID → P-XXXX, Provider → DR-XXXX, Member ID → M-XXXX

### Audit Logging
- Log all claim data access with timestamp, user ID, and claim identifier
- Record risk assessments and recommendations for compliance tracking
- Maintain audit trail for post-submission denial correlation analysis

### Data Retention & Deletion
- Claim review data retained for 7 years per HIPAA requirements
- Secure deletion of temporary processing files within 24 hours
- Archive completed assessments to encrypted long-term storage

### Role-Based Access Controls
- **Coders**: Access to coding and documentation review functions only
- **Revenue Cycle Staff**: Full access to all denial prevention features
- **Auditors**: Read-only access to historical assessments and patterns
- **Compliance**: Access to audit logs and policy adherence reports

---

## High-Risk Procedure Code Rules

### E&M Coding — Most Common Denial Source

#### 99214 (Level 4 Office Visit)
- **Requires documented Medical Decision Making (MDM) of MODERATE complexity OR total time ≥ 30 minutes**
- Flag before submission if:
  - Note does not document number and complexity of problems addressed
  - No documentation of amount/complexity of data reviewed
  - Risk of complications not explicitly stated
  - Time-based billing used but total time not documented in note
- **If MDM is absent or incomplete: downcode to 99213 or request addendum before submitting**

#### 99215 (Level 5 Office Visit)
- Requires HIGH complexity MDM or ≥ 40 minutes
- High audit target — always verify documentation supports level before submitting
- Independent interpretation of results (labs, imaging) must be separately documented

#### New Patient vs Established Patient
- New patient (99202-99205): Patient must not have been seen by provider or same specialty group in last 3 years
- Flag if patient has prior visits in system — may need to bill as established

### Surgical Procedures
- Global period rules: Post-op visits within global period cannot be billed separately unless unrelated diagnosis
- Assistant surgeon: Verify payer allows assistant — many payers deny for common procedures
- Bilateral procedures: Use modifier 50 — without it, payer may pay only one unit

### Diagnostic Testing
- Ordering provider must have ordered the test — self-referral flags trigger review
- Medical necessity diagnosis must be listed first on claim
- Repeat testing: Document why repeat test was medically necessary

---

## Payer-Specific Denial Patterns

### Medicare
- Most common: Missing or insufficient documentation for medical necessity
- Therapy services: Functional improvement must be documented — maintenance therapy not covered
- DME: Certificate of Medical Necessity (CMN) must be on file before claim submission

### BCBS
- Coordination of benefits (COB) — verify primary/secondary before submitting
- Out-of-network claims: Verify member benefits — silent PPO arrangements may reduce payment

### Medicaid
- Timely filing: Most states have 90-day limit — flag any claim older than 60 days
- Provider enrollment: Rendering provider must be enrolled at time of service — not just at submission

### Commercial
- Retroactive eligibility terminations: Verify eligibility on date of service, not just at scheduling

---

## Error Handling & Data Validation

### Invalid Claim Data
- **Missing required fields**: Return error with specific missing elements
- **Invalid procedure codes**: Flag unrecognized CPT codes for manual review
- **Date inconsistencies**: Validate service date vs eligibility period vs submission date
- **Provider mismatches**: Verify rendering provider matches service location

### Incomplete Documentation
- **Partial notes**: Flag for completion before risk assessment
- **Missing signatures**: Hold claim until documentation complete
- **Illegible entries**: Request clarification before proceeding

### System Integration Failures
- **Eligibility verification timeout**: Default to manual verification process
- **Payer rule updates**: Graceful degradation to general denial risk patterns
- **Database connectivity issues**: Queue claims for batch processing when connection restored

---

## Batch Processing Options

### High-Volume Scenarios (>100 claims)
- **Batch upload**: CSV format with standardized claim data fields
- **Priority queuing**: Rush processing for same-day submission deadlines
- **Parallel processing**: Multiple claims assessed simultaneously for faster throughput
- **Summary reporting**: Aggregate risk statistics across claim batches

### Cost Optimization
- **Off-peak processing**: Schedule large batches during low-usage hours
- **Risk-based sampling**: Full review for high-risk claims, spot-check for low-risk
- **Automated pre-screening**: System flags only require human review for medium/high risk

---

## Pre-Submission Checklist

Run this before any claim is submitted:

**Demographics & Eligibility**
- [ ] Patient eligibility verified for date of service (not today)
- [ ] Correct insurance plan and group number
- [ ] Referral/authorization on file if required

**Coding**
- [ ] Primary diagnosis supports medical necessity for all services billed
- [ ] E&M level matches documentation (MDM or time documented)
- [ ] Modifiers applied correctly (bilateral, assistant, distinct service)
- [ ] No unbundling of services that should be billed together

**Documentation**
- [ ] Signed and dated note in chart
- [ ] For 99214/99215: MDM complexity or total time documented
- [ ] For procedures: Operative report complete and signed
- [ ] For ordered tests: Order in chart with diagnosis

---

## Denial Risk Scoring

| Risk Level | Triggers | Action |
|---|---|---|
| HIGH | Missing MDM on E&M, no auth on file, expired authorization | Hold claim — fix before submitting |
| MEDIUM | Diagnosis-procedure mismatch, modifier missing | Review and correct or document justification |
| LOW | Minor formatting issues | Submit with note for follow-up |

---

## Output Format
For each claim reviewed:
1. **Risk level** (High / Medium / Low)
2. **Denial risk reason** — specific rule triggered
3. **Recommended action** — fix, addendum, hold, or submit
4. **Estimated denial rate** for this claim type if submitted as-is
5. **Masked identifiers** — no PHI in assessment outputs

---

## Governance Notes
- E&M coding rules reflect 2024 AMA guidelines — updated from 2021 documentation changes
- 99214 MDM requirement is the #1 source of post-payment audits — treat with high priority
- Payer-specific patterns updated based on quarterly denial analysis by Revenue Cycle team
- Changes to this skill require review by Compliance, Coding, and Revenue Cycle leadership
- Security controls reviewed annually by Information Security and Privacy Officer