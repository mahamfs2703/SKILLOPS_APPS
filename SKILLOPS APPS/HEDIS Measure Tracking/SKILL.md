---
name: hedis-measure-tracking
description: Calculate and track HEDIS measure rates with correct technical specifications, exclusions, and denominator logic. Use this skill whenever calculating HEDIS rates, building HEDIS dashboards, identifying HEDIS gaps, validating HEDIS submissions, or preparing for HEDIS audits. Always use this skill when the request involves "HEDIS", "measure rates", "Star Ratings measures", "quality measures", "numerator", "denominator", or "exclusions". Clinical exclusions that are not in the data must be applied manually — this skill captures those.
---

# HEDIS Measure Tracking

## Purpose
Calculate HEDIS measure rates accurately using NCQA technical specifications, applying correct exclusions — including clinical exclusions that may not be coded in the data.

## Core Principle
**HEDIS exclusions are not optional.** Failing to apply correct exclusions inflates your denominator and deflates your rate — making performance look worse than it is. Some exclusions require clinical knowledge that is not captured in claims or coded diagnoses.

---

## Critical Clinical Exclusions — These Are Frequently Missed

### Colorectal Cancer Screening (COL)
- **Exclude patients with prior colectomy** — even if not coded in current system
  - ICD-10 codes: Z90.49, Z90.5 (partial or total colectomy history)
  - Also exclude if operative note exists anywhere in record — not just coded diagnosis
  - Do not flag these patients for gap closure — they are ineligible
- Exclude patients with colorectal cancer diagnosis (active or historical)
- Exclude patients who had a colostomy
- **Valid numerator options**: FIT/FOBT in measurement year, flexible sigmoidoscopy in last 5 years, colonoscopy in last 10 years, CT colonography in last 5 years

### Breast Cancer Screening (BCS)
- Exclude patients with bilateral mastectomy
- Exclude patients with unilateral mastectomy + right/left modifier (if both sides done)
- ICD-10: Z90.11 (right), Z90.12 (left), Z90.13 (bilateral)
- Check for mastectomy in both claims AND operative notes

### Diabetes Measures (HbA1c Testing, Poor Control, Eye Exam)
- Exclude patients who are no longer diabetic (documented reversal or reclassification)
- Exclude gestational diabetes (O24.4x) — these patients are NOT in the diabetes denominator
- For HbA1c Poor Control (HPC): Rate is inverted — LOWER rate = BETTER performance

### Medication Adherence Measures
- Exclude patients who died during measurement year
- Exclude patients who were not continuously enrolled for required period
- PDC (Proportion of Days Covered) threshold: ≥ 80% = compliant

### Follow-Up After Hospitalization for Mental Illness (FUH)
- 7-day and 30-day follow-up windows start day after discharge
- Readmissions within the window do not count as follow-up
- Telehealth visits qualify — ensure they are coded as qualifying visit types

---

## Denominator Construction Rules

For every measure, confirm:
1. **Continuous enrollment** requirement met (typically 11 of 12 months with allowable gap)
2. **Age range** correct for the measure and the measurement year
3. **Product line** separation — Commercial, Medicaid, and Medicare are reported separately
4. **Event-based vs cross-sectional** — some measures require a qualifying event (like a hospitalization)

---

## Measurement Year Dates

- HEDIS measurement year = January 1 through December 31
- Rate is calculated based on events occurring in the measurement year
- **Do not use plan year or contract year** unless the measure specification explicitly states otherwise
- Look-back periods (e.g., colonoscopy in last 10 years) reference prior to December 31 of measurement year

---

## Hybrid vs Administrative Methodology

| Method | When Used | Key Difference |
|---|---|---|
| Administrative | Most measures, most plans | Claims data only — faster but may miss documented services |
| Hybrid | Plans seeking higher rates | Supplement claims with medical record review |
| Medical Record Only | A few specific measures | Must follow NCQA record review protocols |

**If running administrative rates:** Acknowledge that true performance may be higher due to services not captured in claims.

---

## Output Format
For each HEDIS measure report:
1. **Measure name and NCQA code**
2. **Product line** (Commercial / Medicaid / Medicare)
3. **Denominator** — eligible population count
4. **Exclusions applied** — count and types
5. **Numerator** — compliant members count
6. **Rate** — expressed as percentage
7. **Benchmark comparison** — NCQA national percentile if available
8. **Gap list** — non-compliant members eligible for outreach

---

## Governance Notes
- HEDIS technical specifications update annually — this skill must be reviewed each January when NCQA releases new specs
- Colectomy exclusion for COL is the most frequently missed exclusion — added to this skill after 2023 audit finding
- Mastectomy exclusion requires checking both claims and operative notes — claims alone are insufficient
- All HEDIS rate calculations for external reporting require validation by the Quality team before submission
