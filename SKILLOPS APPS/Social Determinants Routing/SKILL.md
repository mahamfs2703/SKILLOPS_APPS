---
name: social-determinants-routing
description: Route patients with social determinants of health (SDOH) needs to the correct community and clinical resources based on need type and resource availability. Use this skill whenever assessing SDOH needs, routing patients to social services, building SDOH workflows, or analyzing social risk in patient populations. Always use this skill when the request involves "SDOH", "social determinants", "housing", "food insecurity", "transportation", "social needs", "community health worker", or "social work referral". Routing decisions depend on resource availability — not just need type.
---

# Social Determinants of Health (SDOH) Routing

## Purpose
Route patients with identified social needs to the correct resource — distinguishing between community health worker, social worker, nurse line, and automated resource referral based on need type, urgency, and available resources.

## Core Principle
**SDOH routing is a workflow decision, not a clinical score.** The right routing depends on what resources are available and what level of support the need requires.

---

## SDOH Routing Rules — By Need Type

### Housing Instability / Homelessness
- **Route to: Community Health Worker (CHW)** — not the nurse line
- CHW has relationships with local housing resources, shelters, and HUD programs
- Urgency: High — housing instability is a leading driver of readmissions and ED utilization
- If CHW unavailable: Route to Social Worker with housing expertise

### Food Insecurity
- **Route to: Community Health Worker (CHW)**
- CHW can connect to local food banks, SNAP enrollment assistance, medically tailored meal programs
- For clinical nutrition needs (malnutrition, post-surgical diet): Route to Registered Dietitian, not CHW
- Screen using AHC-HRSN or Hunger Vital Sign tool — document score in chart

### Transportation Barriers
- **Route to: Community Health Worker (CHW)**
- CHW can arrange NEMT (Non-Emergency Medical Transportation) for appointments
- For urgent medical transport needs: Social Worker

### Domestic Violence / Intimate Partner Violence
- **Route to: Licensed Social Worker — only**
- Do not route to CHW or automated resources — this requires clinical assessment
- Follow mandatory reporting obligations per state law

### Mental Health / Behavioral Health Needs (Social Context)
- Social isolation, grief, caregiver stress: Route to Social Worker or Behavioral Health navigator
- Active mental health symptoms (depression, anxiety): Route to BH clinician — not CHW
- Crisis / suicidal ideation: 988 Lifeline + immediate clinical escalation

### Financial / Benefits Assistance
- Medicaid/CHIP enrollment: CHW or benefits navigator
- Disability benefits (SSI/SSDI): Social Worker — complex process requiring advocacy
- Utility assistance (LIHEAP): CHW
- Medical debt / financial counseling: Financial counselor — not CHW or clinical staff

### Immigration / Legal Status Concerns
- Route to Social Worker with immigration experience — or legal aid referral
- Do not ask about immigration status unless patient raises it
- Undocumented patients are entitled to emergency Medicaid — document as emergency only

---

## SDOH Screening Tool Reference

| Tool | Best For | Score Threshold for Routing |
|---|---|---|
| AHC-HRSN (CMS) | Medicare / Medicaid | 2+ positive screens = routing required |
| Hunger Vital Sign | Food insecurity only | Either question positive = food insecure |
| PRAPARE | Comprehensive SDOH | Any domain positive = assess and route |
| WE CARE | Pediatric populations | Any positive = family-level needs assessment |

---

## Resource Availability Decision Tree

Before routing, always check:
1. **Is a CHW available on the patient's care team?** → If yes, route directly
2. **Is CHW caseload at capacity?** → Route to Social Work or waitlist with documented follow-up date
3. **Is the need urgent?** (Housing loss, food crisis, DV) → Escalate regardless of capacity — do not waitlist
4. **Is the need clinical in nature?** → Route to clinical staff, not CHW

---

## Documentation Requirements

For every SDOH screening and routing:
1. **Screening tool used** and score/result
2. **Need identified** — specific domain
3. **Resource routed to** — name, organization, contact
4. **Patient consent** — documented if sharing information with community organizations
5. **Follow-up date** — confirm need was addressed at next touchpoint
6. **Outcome** — was the need resolved? Document at follow-up

---

## SDOH and Clinical Integration

SDOH flags must be visible to clinical team — not siloed in care management:
- Housing instability flag → surfaces in readmission risk score
- Food insecurity flag → triggers dietitian consult for diabetic and post-surgical patients
- Transportation barrier → triggers telehealth as alternative to in-person visit
- DV flag → triggers safety screening at every future clinical encounter

---

## Output Format
For each SDOH routing decision:
1. **Need identified** and screening tool / score
2. **Urgency level** (Immediate / High / Standard)
3. **Routing recommendation** — resource type and specific resource if known
4. **Rationale** — why this resource and not another
5. **Follow-up required** — date and owner
6. **Clinical integration flags** — what clinical team needs to know