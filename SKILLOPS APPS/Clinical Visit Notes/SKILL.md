I have enough information to create a clinical visit notes summarization skill for you. Here's the skill:

GENERATED_SKILL_JSON::{"name": "clinical-visit-notes-summarizer", "domain": "HCLS", "subdomain": "Clinical Documentation", "sensitivity": "PHI", "description": "Summarizes clinical visit notes into structured, concise summaries for healthcare providers", "content": "---
name: clinical-visit-notes-summarizer
description: Summarizes clinical visit notes into structured, concise summaries for healthcare providers
---

# Clinical Visit Notes Summarizer

## Purpose
This skill extracts and summarizes key information from clinical visit notes to provide healthcare providers with concise, structured summaries that highlight the most important clinical details, diagnoses, treatments, and follow-up actions.

## Instructions
1. Read and analyze the provided clinical visit notes thoroughly
2. Extract the following key information:
   - Patient demographics and visit details
   - Chief complaint and presenting symptoms
   - Relevant medical history and current medications
   - Physical examination findings (abnormal findings prioritized)
   - Assessment and diagnoses (primary and secondary)
   - Treatment plan and interventions
   - Follow-up instructions and next steps
3. Organize the information into a clear, structured summary
4. Use medical terminology appropriately while ensuring clarity
5. Prioritize clinically significant information
6. Maintain chronological flow when relevant

## Output Format
Provide a structured summary with the following sections:

**VISIT SUMMARY**
- Date: [visit date]
- Provider: [provider name if available]
- Visit Type: [routine, follow-up, urgent, etc.]

**CHIEF COMPLAINT**
[Primary reason for visit]

**KEY FINDINGS**
- Vital Signs: [if documented]
- Physical Exam: [significant findings only]
- Diagnostics: [lab results, imaging, etc.]

**ASSESSMENT & DIAGNOSIS**
- Primary: [main diagnosis/condition]
- Secondary: [additional diagnoses if applicable]

**TREATMENT PLAN**
- Medications: [new prescriptions, changes, discontinuations]
- Interventions: [procedures, therapies, lifestyle modifications]
- Follow-up: [next appointments, monitoring requirements]

**ACTION ITEMS**
[Specific tasks for patient or care team]

## Constraints
- Maintain patient confidentiality and handle PHI appropriately
- Do not add clinical interpretations beyond what is documented
- Preserve critical medical details and exact medication names/dosages
- If information is unclear or missing, note as "Not documented" rather than inferring
- Keep summary concise but comprehensive (typically 200-400 words)
- Use bullet points and clear formatting for readability
- Do not include personal opinions or recommendations not present in the original notes"}