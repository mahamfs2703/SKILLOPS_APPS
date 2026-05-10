---
name: chronic-disease-management
description: Apply disease-specific clinical protocols for chronic condition management including CHF, COPD, diabetes, and hypertension. Use this skill whenever managing chronic disease patient populations, building disease registry outreach lists, designing care management workflows, or reviewing chronic condition clinical protocols. Always use this skill when the request involves "CHF", "heart failure", "COPD", "diabetes management", "chronic disease", "disease registry", "care management protocol", or "post-discharge outreach". Protocol decisions are clinical — not data rules.
---

# Chronic Disease Management

## Purpose
Apply disease-specific clinical protocols to chronic condition management — ensuring that outreach, escalation, and care coordination decisions follow evidence-based and organizationally-approved protocols.

## Core Principle
**Clinical protocols are not data rules.** The timing, method, and owner of an outreach are clinical decisions that cannot be derived from a query. This skill encodes those decisions so they are applied consistently across care management staff and AI-assisted workflows.

---

## Data Security and Privacy Requirements

### PHI Protection
- **Mask all PHI** in outputs (names, DOB, SSN, MRN, addresses, phone numbers)
- Use generic identifiers (Patient A, Case #1) in examples and documentation
- **Never store or cache** patient-specific data between sessions
- Redact identifiable information from all logs and audit trails

### Input Validation
- **Validate data completeness** before applying protocols
- **Sanitize all inputs** to prevent data corruption or injection
- **Flag incomplete records** that may compromise clinical decision accuracy
- **Verify data format consistency** (dates, measurements, codes)

### Audit and Compliance
- **Log all protocol applications** with timestamp and decision rationale
- **Track clinical decision points** for quality assurance review
- **Record data access patterns** for compliance monitoring
- **Maintain decision audit trail** for 7 years minimum

### Error Handling
- **Graceful degradation** when patient data is incomplete
- **Clear error messaging** for missing critical information
- **Fallback protocols** for partial data scenarios
- **Escalation pathways** for data quality issues

### Access Controls
- **Role-based access** to protocol functions
- **Session timeout** after 30 minutes of inactivity
- **Multi-factor authentication** required for clinical staff
- **Data retention limits**: Patient data purged after session completion

---

## CHF (Congestive Heart Failure) Protocol

### Post-Discharge — Highest Priority
- **Outreach within 48 hours of discharge** — hard protocol requirement
- Outreach by **care coordinator or nurse — not automated message**
- Follow-up appointment must be **scheduled before discharge**

### Ongoing Management
- Weight monitoring: Daily weighing plan required
- Weight gain alert: 2+ lbs/day OR 5 lbs/week = escalate
- Medication adherence: Confirm diuretic and ACE inhibitor fills
- Fluid restriction: Assess compliance at every touchpoint

### Escalation Triggers
- Rapid weight gain → Same-day clinical notification
- Missed follow-up → Reschedule within 24 hours
- Dyspnea at rest → Direct to ER
- 3+ missed medication fills → Care manager escalation

---

## COPD Protocol

### Exacerbation Prevention
- Ensure current vaccines (influenza, pneumococcal)
- Confirm rescue inhaler supply
- Pulmonary rehabilitation referral for GOLD Stage 2+

### Post-Exacerbation
- Follow-up within 7 days for severe exacerbations
- Confirm inhaler technique at every contact
- Smoking cessation referral if current smoker

### Escalation Triggers
- 2+ exacerbations in 12 months → Refer to pulmonology
- No rescue inhaler fill in 60 days → Pharmacy outreach
- SpO2 < 88% → Direct to ER

---

## Diabetes Protocol

### Glycemic Monitoring
- HbA1c target: < 7% (< 8% for elderly/high comorbidity)
- Testing frequency: Every 3 months if uncontrolled; every 6 months if stable
- Flag: HbA1c > 9 AND 2+ missed appointments

### Complication Prevention
- Annual dilated eye exam
- Annual foot exam documentation
- Nephrology referral: eGFR < 45 or ACR > 300

### Medication Management
- GLP-1/SGLT2 inhibitors preferred with CVD/CKD
- Insulin patients: Confirm monitoring plan

---

## Hypertension Protocol

### BP Targets
- General: < 130/80 mmHg
- Elderly: < 130/80 if tolerated
- CKD: < 130/80 with ACE inhibitor/ARB

### Follow-Up
- New/medication change: 4 weeks
- Controlled: 3-6 months
- Uncontrolled (> 160/100): 2 weeks

---

## General Rules

1. Annual care plan updates required
2. Document patient self-management goals
3. Include caregiver for elderly/cognitively impaired
4. Annual depression screening (PHQ-9)

---

## Output Format
1. **Condition(s)** managed
2. **Protocol compliance** status
3. **Escalation flags**
4. **Recommended actions** with timeline
5. **Care plan update needed?**