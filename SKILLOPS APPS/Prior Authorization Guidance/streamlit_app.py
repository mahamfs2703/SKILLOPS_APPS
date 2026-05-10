import streamlit as st

st.set_page_config(page_title="Prior Authorization Guidance", page_icon="🏥", layout="wide")

PAYER_RULES = {
    "Blue Cross Blue Shield (BCBS)": {
        "Biologics": [
            "Always check step therapy requirements",
            "Patient must have documented failure of at least 2 conventional DMARDs before biologic approval for inflammatory conditions",
            "Adalimumab biosimilars are preferred over reference product",
            "Specialty pharmacy requirement: Most biologics routed through Accredo or CVS Specialty",
        ],
        "Imaging (MRI/CT)": [
            "RadMD prior auth required for outpatient advanced imaging",
        ],
        "Surgical Procedures": [
            "Clinical notes from last 90 days required",
        ],
    },
    "UnitedHealthcare (UHC)": {
        "Behavioral Health": [
            "Separate PA process through Optum — do not submit through medical PA portal",
        ],
        "Home Health": [
            "Require face-to-face documentation within 90 days of order",
        ],
        "Oncology": [
            "Site-of-care review required for infused chemotherapy",
        ],
    },
    "Aetna": {
        "Musculoskeletal": [
            "Conservative therapy (PT, chiro) required before advanced imaging or surgical authorization",
        ],
        "Sleep Studies": [
            "Home sleep test required before PSG for most members",
        ],
        "Specialty Drugs": [
            "Check CVS Caremark formulary — many exclusions apply",
        ],
    },
    "Medicaid (State-specific)": {
        "Brand Drugs": [
            "Most states require PA for any brand drug when a generic is available",
        ],
        "Behavioral Health": [
            "Often requires separate authorization through BH carve-out",
        ],
    },
    "Medicare Advantage": {
        "General": [
            "PA requirements vary significantly by plan — always check individual plan's coverage determination",
        ],
        "Emergency Admissions": [
            "No PA required at admission — concurrent review begins within 24 hours",
        ],
        "SNF Stays": [
            "PA required after day 20 for most plans",
        ],
    },
}

DENIAL_REASONS = [
    {"reason": "Step therapy not met", "prevention": "Document all prior therapy failures before submitting"},
    {"reason": "Missing clinical notes", "prevention": "Always attach notes from last 90 days"},
    {"reason": "Wrong PA portal used", "prevention": "Verify payer portal — BH and medical are often separate"},
    {"reason": "Diagnosis code mismatch", "prevention": "ICD-10 on PA must match claim — verify before submitting"},
    {"reason": "Non-preferred drug requested", "prevention": "Check formulary for preferred alternatives"},
    {"reason": "Expired authorization", "prevention": "Check PA expiration date before scheduling service"},
]

STEP_THERAPY_CHECKLIST = [
    "Has the patient tried and failed first-line therapy? (Document drug name, dose, duration, reason for failure)",
    "Is the failure documented in clinical notes — not just the PA form?",
    "Does the payer require failure of a specific drug (not just drug class)?",
    "Is the requested biologic on the payer's preferred specialty list?",
    "Has the patient been on the current plan for >90 days?",
    "Is there a medical necessity exception applicable?",
]

st.title("Prior Authorization Guidance")
st.caption("Payer-specific PA guidance to reduce denials and ensure complete submissions")

st.warning("**Reminder:** Payer rules change constantly. Always verify against the payer portal before submission.")

tab1, tab2, tab3, tab4 = st.tabs(["PA Lookup", "Step Therapy Checklist", "Denial Prevention", "Assessment"])

with tab1:
    st.header("Payer-Specific Requirements")
    col1, col2 = st.columns(2)
    with col1:
        selected_payer = st.selectbox("Select Payer", list(PAYER_RULES.keys()))
    with col2:
        categories = list(PAYER_RULES[selected_payer].keys())
        selected_category = st.selectbox("Select Category", categories)

    st.subheader(f"{selected_payer} — {selected_category}")
    rules = PAYER_RULES[selected_payer][selected_category]
    for rule in rules:
        st.markdown(f"- {rule}")

with tab2:
    st.header("Step Therapy Checklist")
    st.info("Complete this checklist before submitting any biologic or specialty medication PA.")
    checklist_status = {}
    for i, item in enumerate(STEP_THERAPY_CHECKLIST):
        checklist_status[i] = st.checkbox(item, key=f"step_{i}")

    completed = sum(checklist_status.values())
    total = len(STEP_THERAPY_CHECKLIST)
    st.progress(completed / total)
    if completed == total:
        st.success("All step therapy requirements verified. Ready to submit PA.")
    elif completed > 0:
        st.warning(f"{completed}/{total} items complete. Address remaining items before submission.")
    else:
        st.error("No items checked. Complete the checklist before PA submission.")

with tab3:
    st.header("Common PA Denial Reasons & Prevention")
    for item in DENIAL_REASONS:
        with st.expander(f"**{item['reason']}**"):
            st.markdown(f"**Prevention:** {item['prevention']}")

with tab4:
    st.header("PA Submission Assessment")
    st.markdown("Enter case details below to get a quick assessment.")

    col1, col2 = st.columns(2)
    with col1:
        assess_payer = st.selectbox("Payer", list(PAYER_RULES.keys()), key="assess_payer")
        drug_or_procedure = st.text_input("Drug / Procedure Name")
        icd10_code = st.text_input("ICD-10 Diagnosis Code")
    with col2:
        has_clinical_notes = st.checkbox("Clinical notes from last 90 days attached?")
        has_step_therapy = st.checkbox("Step therapy documented?")
        is_preferred = st.checkbox("Drug/procedure is on preferred list?")

    if st.button("Generate Assessment"):
        if not drug_or_procedure:
            st.error("Please enter a drug or procedure name.")
        else:
            st.divider()
            st.subheader("Assessment Results")

            score = sum([has_clinical_notes, has_step_therapy, is_preferred])

            st.markdown(f"**1. PA Required?** Verify — check {assess_payer} portal for `{drug_or_procedure}`")

            st.markdown(f"**2. Payer-specific requirements:**")
            payer_cats = PAYER_RULES[assess_payer]
            for cat, rules in payer_cats.items():
                st.markdown(f"  *{cat}:*")
                for r in rules:
                    st.markdown(f"  - {r}")

            st.markdown("**3. Checklist Status:**")
            st.markdown(f"  - Clinical notes: {'Complete' if has_clinical_notes else 'MISSING'}")
            st.markdown(f"  - Step therapy: {'Complete' if has_step_therapy else 'MISSING'}")
            st.markdown(f"  - Preferred list: {'Yes' if is_preferred else 'Not confirmed'}")

            if score == 3:
                st.success("**4. Anticipated Approval Likelihood: HIGH** — All key requirements met.")
            elif score == 2:
                st.warning("**4. Anticipated Approval Likelihood: MEDIUM** — Address missing items to improve chances.")
            else:
                st.error("**4. Anticipated Approval Likelihood: LOW** — Multiple requirements not met. Consider alternatives.")

            st.markdown("**5. If denial is likely:** Check formulary for preferred alternatives, consider site-of-care changes, or pursue medical necessity exception pathway.")
