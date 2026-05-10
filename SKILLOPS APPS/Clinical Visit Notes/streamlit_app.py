import streamlit as st
from snowflake.snowpark.context import get_active_session

st.set_page_config(layout="wide")
st.title("Clinical Visit Notes Summarizer")
st.write("Paste clinical visit notes below to get a structured summary with key findings, diagnoses, and action items.")

session = get_active_session()

SYSTEM_PROMPT = """You are a clinical documentation specialist. Summarize clinical visit notes into structured, concise summaries for healthcare providers.

Extract and organize the following:
- Patient demographics and visit details
- Chief complaint and presenting symptoms
- Relevant medical history and current medications
- Physical examination findings (abnormal findings prioritized)
- Assessment and diagnoses (primary and secondary)
- Treatment plan and interventions
- Follow-up instructions and next steps

Output Format:

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

Constraints:
- Do not add clinical interpretations beyond what is documented
- Preserve critical medical details and exact medication names/dosages
- If information is unclear or missing, note as "Not documented"
- Keep summary concise but comprehensive (200-400 words)
"""

notes_input = st.text_area(
    "Clinical Visit Notes",
    height=300,
    placeholder="Paste the full clinical visit notes here..."
)

if st.button("Summarize Notes", type="primary"):
    if not notes_input.strip():
        st.warning("Please enter clinical visit notes to summarize.")
    else:
        with st.spinner("Generating structured summary..."):
            prompt = notes_input.replace("'", "\\'")
            system = SYSTEM_PROMPT.replace("'", "\\'")

            sql = f"""
                SELECT SNOWFLAKE.CORTEX.COMPLETE(
                    'mistral-large2',
                    [
                        {{'role': 'system', 'content': '{system}'}},
                        {{'role': 'user', 'content': '{prompt}'}}
                    ],
                    {{}}
                ) AS summary
            """
            result = session.sql(sql).collect()
            import json
            response = json.loads(result[0]["SUMMARY"])
            summary_text = response["choices"][0]["messages"]

            st.divider()
            st.subheader("Structured Summary")
            st.markdown(summary_text)
