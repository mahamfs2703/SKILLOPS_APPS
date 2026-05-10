import streamlit as st

st.set_page_config(page_title="SDOH Patient Routing", page_icon="🏥", layout="wide")

NEED_TYPES = [
    "Housing Instability / Homelessness",
    "Food Insecurity",
    "Transportation Barriers",
    "Domestic Violence / Intimate Partner Violence",
    "Mental Health / Behavioral Health (Social Context)",
    "Mental Health / Behavioral Health (Active Symptoms)",
    "Mental Health / Behavioral Health (Crisis)",
    "Financial / Benefits - Medicaid/CHIP",
    "Financial / Benefits - Disability (SSI/SSDI)",
    "Financial / Benefits - Utility Assistance (LIHEAP)",
    "Financial / Benefits - Medical Debt",
    "Immigration / Legal Status Concerns",
]

SCREENING_TOOLS = ["AHC-HRSN (CMS)", "Hunger Vital Sign", "PRAPARE", "WE CARE"]

ROUTING_RULES = {
    "Housing Instability / Homelessness": {
        "route_to": "Community Health Worker (CHW)",
        "fallback": "Social Worker with housing expertise",
        "urgency": "High",
        "rationale": "CHW has relationships with local housing resources, shelters, and HUD programs. Housing instability is a leading driver of readmissions and ED utilization.",
        "clinical_flags": ["Surfaces in readmission risk score"],
    },
    "Food Insecurity": {
        "route_to": "Community Health Worker (CHW)",
        "fallback": "Registered Dietitian (if clinical nutrition need)",
        "urgency": "High",
        "rationale": "CHW can connect to local food banks, SNAP enrollment assistance, medically tailored meal programs.",
        "clinical_flags": ["Triggers dietitian consult for diabetic and post-surgical patients"],
    },
    "Transportation Barriers": {
        "route_to": "Community Health Worker (CHW)",
        "fallback": "Social Worker (if urgent medical transport)",
        "urgency": "Standard",
        "rationale": "CHW can arrange NEMT (Non-Emergency Medical Transportation) for appointments.",
        "clinical_flags": ["Triggers telehealth as alternative to in-person visit"],
    },
    "Domestic Violence / Intimate Partner Violence": {
        "route_to": "Licensed Social Worker",
        "fallback": "None - Licensed Social Worker ONLY",
        "urgency": "Immediate",
        "rationale": "Requires clinical assessment. Do not route to CHW or automated resources. Follow mandatory reporting obligations per state law.",
        "clinical_flags": ["Triggers safety screening at every future clinical encounter"],
    },
    "Mental Health / Behavioral Health (Social Context)": {
        "route_to": "Social Worker or Behavioral Health Navigator",
        "fallback": "N/A",
        "urgency": "Standard",
        "rationale": "Social isolation, grief, caregiver stress require social support, not clinical intervention.",
        "clinical_flags": [],
    },
    "Mental Health / Behavioral Health (Active Symptoms)": {
        "route_to": "Behavioral Health Clinician",
        "fallback": "N/A",
        "urgency": "High",
        "rationale": "Active depression, anxiety requires clinical BH intervention - not CHW.",
        "clinical_flags": [],
    },
    "Mental Health / Behavioral Health (Crisis)": {
        "route_to": "988 Suicide & Crisis Lifeline + Immediate Clinical Escalation",
        "fallback": "N/A",
        "urgency": "Immediate",
        "rationale": "Crisis / suicidal ideation requires immediate intervention.",
        "clinical_flags": [],
    },
    "Financial / Benefits - Medicaid/CHIP": {
        "route_to": "Community Health Worker (CHW) or Benefits Navigator",
        "fallback": "N/A",
        "urgency": "Standard",
        "rationale": "CHW or benefits navigator can assist with enrollment process.",
        "clinical_flags": [],
    },
    "Financial / Benefits - Disability (SSI/SSDI)": {
        "route_to": "Social Worker",
        "fallback": "N/A",
        "urgency": "Standard",
        "rationale": "Complex process requiring advocacy - not appropriate for CHW.",
        "clinical_flags": [],
    },
    "Financial / Benefits - Utility Assistance (LIHEAP)": {
        "route_to": "Community Health Worker (CHW)",
        "fallback": "N/A",
        "urgency": "Standard",
        "rationale": "CHW can connect to LIHEAP and local utility assistance programs.",
        "clinical_flags": [],
    },
    "Financial / Benefits - Medical Debt": {
        "route_to": "Financial Counselor",
        "fallback": "N/A",
        "urgency": "Standard",
        "rationale": "Medical debt/financial counseling - not CHW or clinical staff.",
        "clinical_flags": [],
    },
    "Immigration / Legal Status Concerns": {
        "route_to": "Social Worker with immigration experience or Legal Aid Referral",
        "fallback": "N/A",
        "urgency": "High",
        "rationale": "Do not ask about immigration status unless patient raises it. Undocumented patients are entitled to emergency Medicaid.",
        "clinical_flags": [],
    },
}

st.title("SDOH Patient Routing Tool")
st.markdown("Route patients with social determinants of health needs to the correct community and clinical resources.")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Patient & Screening Information")
    patient_id = st.text_input("Patient ID")
    screening_tool = st.selectbox("Screening Tool Used", SCREENING_TOOLS)
    screening_score = st.text_input("Screening Score / Result")
    need_type = st.selectbox("Identified Need", NEED_TYPES)
    patient_consent = st.checkbox("Patient consent obtained for sharing with community organizations")

with col2:
    st.subheader("Resource Availability")
    chw_available = st.radio("Is a CHW available on the patient's care team?", ["Yes", "No"])
    chw_at_capacity = False
    if chw_available == "Yes":
        chw_at_capacity = st.checkbox("CHW caseload at capacity?")
    is_urgent = st.checkbox("Is the need urgent? (Housing loss, food crisis, DV)")
    is_clinical = st.checkbox("Is the need clinical in nature?")

st.divider()

if st.button("Generate Routing Recommendation", type="primary"):
    if not patient_id:
        st.error("Please enter a Patient ID.")
    elif not screening_score:
        st.error("Please enter a Screening Score / Result.")
    else:
        rule = ROUTING_RULES[need_type]

        if is_clinical and need_type not in [
            "Domestic Violence / Intimate Partner Violence",
            "Mental Health / Behavioral Health (Active Symptoms)",
            "Mental Health / Behavioral Health (Crisis)",
        ]:
            final_route = "Clinical Staff (need is clinical in nature)"
            rationale = "Clinical needs should be routed to clinical staff, not CHW."
        elif chw_available == "No" or chw_at_capacity:
            if is_urgent:
                final_route = rule["route_to"] + " (ESCALATED - urgent, bypass capacity limits)"
                rationale = "Urgent need - escalate regardless of capacity. Do not waitlist."
            else:
                final_route = rule["fallback"] if rule["fallback"] != "N/A" else rule["route_to"] + " (waitlisted)"
                rationale = "CHW unavailable or at capacity. " + rule["rationale"]
        else:
            final_route = rule["route_to"]
            rationale = rule["rationale"]

        urgency = rule["urgency"]
        if is_urgent and urgency == "Standard":
            urgency = "High (escalated due to urgent flag)"

        st.success("Routing recommendation generated.")

        st.subheader("Routing Decision")

        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.markdown(f"**Patient ID:** {patient_id}")
            st.markdown(f"**Need Identified:** {need_type}")
            st.markdown(f"**Screening Tool:** {screening_tool}")
            st.markdown(f"**Screening Score:** {screening_score}")
        with res_col2:
            st.markdown(f"**Urgency Level:** {urgency}")
            st.markdown(f"**Route To:** {final_route}")
            st.markdown(f"**Rationale:** {rationale}")
            st.markdown(f"**Patient Consent:** {'Yes' if patient_consent else 'No'}")

        if rule["clinical_flags"]:
            st.subheader("Clinical Integration Flags")
            for flag in rule["clinical_flags"]:
                st.markdown(f"- {flag}")

        st.subheader("Documentation Checklist")
        st.markdown(f"""
| Item | Value |
|------|-------|
| Screening tool used | {screening_tool} |
| Score/Result | {screening_score} |
| Need identified | {need_type} |
| Resource routed to | {final_route} |
| Patient consent | {'Documented' if patient_consent else 'NOT documented - required before sharing'} |
| Follow-up date | _(Enter at next touchpoint)_ |
| Outcome | _(Document at follow-up)_ |
""")

st.divider()
with st.expander("Reference: SDOH Screening Tool Thresholds"):
    st.markdown("""
| Tool | Best For | Threshold for Routing |
|------|----------|----------------------|
| AHC-HRSN (CMS) | Medicare / Medicaid | 2+ positive screens = routing required |
| Hunger Vital Sign | Food insecurity only | Either question positive = food insecure |
| PRAPARE | Comprehensive SDOH | Any domain positive = assess and route |
| WE CARE | Pediatric populations | Any positive = family-level needs assessment |
""")
