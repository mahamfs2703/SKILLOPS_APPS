import streamlit as st
import pandas as pd
from datetime import date, timedelta

st.set_page_config(page_title="Denial Prevention", page_icon="🛡️", layout="wide")

st.title("🛡️ Claim Denial Prevention")
st.caption("Flag claims at high risk of denial before submission using payer behavior patterns and coding rules.")

PAYER_RULES = {
    "Medicare": [
        "Missing or insufficient documentation for medical necessity",
        "Therapy services: Functional improvement must be documented",
        "DME: Certificate of Medical Necessity (CMN) must be on file",
    ],
    "BCBS": [
        "Coordination of benefits (COB) — verify primary/secondary",
        "Out-of-network claims: Verify member benefits",
    ],
    "Medicaid": [
        "Timely filing: Most states have 90-day limit",
        "Provider enrollment: Rendering provider must be enrolled at time of service",
    ],
    "Commercial": [
        "Retroactive eligibility terminations: Verify eligibility on date of service",
    ],
}

EM_CODES = {
    "99213": {"level": 3, "mdm": "LOW", "time": 20},
    "99214": {"level": 4, "mdm": "MODERATE", "time": 30},
    "99215": {"level": 5, "mdm": "HIGH", "time": 40},
    "99202": {"level": 2, "mdm": "STRAIGHTFORWARD", "time": 15},
    "99203": {"level": 3, "mdm": "LOW", "time": 30},
    "99204": {"level": 4, "mdm": "MODERATE", "time": 45},
    "99205": {"level": 5, "mdm": "HIGH", "time": 60},
}


def mask_id(prefix, value):
    if value:
        return f"{prefix}-XXXX"
    return ""


def assess_risk(claim):
    risks = []
    risk_level = "LOW"

    cpt = claim.get("cpt_code", "")
    if cpt in EM_CODES:
        em_info = EM_CODES[cpt]
        if em_info["level"] >= 4:
            if not claim.get("mdm_documented"):
                risks.append(f"Missing MDM documentation for {cpt} (requires {em_info['mdm']} complexity)")
                risk_level = "HIGH"
            if claim.get("time_based") and not claim.get("time_documented"):
                risks.append(f"Time-based billing for {cpt} but total time not documented (requires ≥{em_info['time']} min)")
                risk_level = "HIGH"

    if not claim.get("auth_on_file") and claim.get("auth_required"):
        risks.append("Authorization required but not on file")
        risk_level = "HIGH"

    if claim.get("auth_expired"):
        risks.append("Authorization on file but expired")
        risk_level = "HIGH"

    payer = claim.get("payer", "")
    service_date = claim.get("service_date")
    if payer == "Medicaid" and service_date:
        days_since = (date.today() - service_date).days
        if days_since > 60:
            risks.append(f"Claim is {days_since} days old — Medicaid 90-day timely filing at risk")
            if days_since > 80:
                risk_level = "HIGH"
            elif risk_level != "HIGH":
                risk_level = "MEDIUM"

    if not claim.get("primary_dx_supports_necessity"):
        risks.append("Primary diagnosis may not support medical necessity for billed services")
        if risk_level != "HIGH":
            risk_level = "MEDIUM"

    if not claim.get("modifier_correct") and claim.get("modifier_needed"):
        risks.append("Required modifier missing (bilateral, assistant, or distinct service)")
        if risk_level != "HIGH":
            risk_level = "MEDIUM"

    if claim.get("global_period_conflict"):
        risks.append("Service within global surgical period — may be denied without modifier 24/25/79")
        if risk_level != "HIGH":
            risk_level = "MEDIUM"

    if not risks:
        risks.append("No specific risk factors identified")

    return risk_level, risks


def get_action(risk_level):
    actions = {
        "HIGH": "HOLD — Fix issues before submitting",
        "MEDIUM": "REVIEW — Correct or document justification before submission",
        "LOW": "SUBMIT — Minor issues noted for follow-up",
    }
    return actions.get(risk_level, "SUBMIT")


def get_denial_rate(risk_level):
    rates = {"HIGH": "60-85%", "MEDIUM": "25-45%", "LOW": "5-15%"}
    return rates.get(risk_level, "Unknown")


tab1, tab2, tab3 = st.tabs(["📋 Claim Review", "📊 Payer Rules Reference", "✅ Pre-Submission Checklist"])

with tab1:
    st.subheader("Enter Claim Details")
    col1, col2 = st.columns(2)

    with col1:
        claim_id = st.text_input("Claim ID", placeholder="CLM-001")
        cpt_code = st.selectbox("CPT/Procedure Code", ["99213", "99214", "99215", "99202", "99203", "99204", "99205", "Other"])
        payer = st.selectbox("Payer", ["Medicare", "BCBS", "Medicaid", "Commercial"])
        service_date = st.date_input("Date of Service", value=date.today() - timedelta(days=5))

    with col2:
        mdm_documented = st.checkbox("MDM Complexity Documented", value=False)
        time_based = st.checkbox("Time-Based Billing", value=False)
        time_documented = st.checkbox("Total Time Documented", value=False)
        auth_required = st.checkbox("Prior Authorization Required", value=False)
        auth_on_file = st.checkbox("Authorization on File", value=False)
        auth_expired = st.checkbox("Authorization Expired", value=False)

    st.markdown("---")
    col3, col4 = st.columns(2)
    with col3:
        primary_dx_supports = st.checkbox("Primary Dx Supports Medical Necessity", value=True)
        modifier_needed = st.checkbox("Modifier Needed", value=False)
        modifier_correct = st.checkbox("Modifier Applied Correctly", value=False)
    with col4:
        global_period_conflict = st.checkbox("Service Within Global Surgical Period", value=False)

    if st.button("🔍 Assess Denial Risk", type="primary"):
        claim = {
            "claim_id": claim_id,
            "cpt_code": cpt_code if cpt_code != "Other" else "",
            "payer": payer,
            "service_date": service_date,
            "mdm_documented": mdm_documented,
            "time_based": time_based,
            "time_documented": time_documented,
            "auth_required": auth_required,
            "auth_on_file": auth_on_file,
            "auth_expired": auth_expired,
            "primary_dx_supports_necessity": primary_dx_supports,
            "modifier_needed": modifier_needed,
            "modifier_correct": modifier_correct,
            "global_period_conflict": global_period_conflict,
        }

        risk_level, risks = assess_risk(claim)
        action = get_action(risk_level)
        denial_rate = get_denial_rate(risk_level)

        st.markdown("---")
        st.subheader("Assessment Results")

        color_map = {"HIGH": "red", "MEDIUM": "orange", "LOW": "green"}
        st.markdown(f"### Risk Level: :{color_map[risk_level]}[{risk_level}]")

        st.markdown(f"**Claim ID (masked):** {mask_id('CLM', claim_id)}")
        st.markdown(f"**Estimated Denial Rate:** {denial_rate}")
        st.markdown(f"**Recommended Action:** {action}")

        st.markdown("**Risk Factors:**")
        for r in risks:
            st.markdown(f"- ⚠️ {r}")

with tab2:
    st.subheader("Payer-Specific Denial Patterns")
    for payer_name, rules in PAYER_RULES.items():
        with st.expander(f"**{payer_name}**"):
            for rule in rules:
                st.markdown(f"- {rule}")

    st.markdown("---")
    st.subheader("E&M Coding Requirements")
    em_df = pd.DataFrame([
        {"Code": code, "Level": info["level"], "MDM Required": info["mdm"], "Min Time (minutes)": info["time"]}
        for code, info in EM_CODES.items()
    ])
    st.dataframe(em_df, use_container_width=True, hide_index=True)

with tab3:
    st.subheader("Pre-Submission Checklist")

    st.markdown("#### Demographics & Eligibility")
    c1 = st.checkbox("Patient eligibility verified for date of service (not today)")
    c2 = st.checkbox("Correct insurance plan and group number")
    c3 = st.checkbox("Referral/authorization on file if required")

    st.markdown("#### Coding")
    c4 = st.checkbox("Primary diagnosis supports medical necessity for all services billed")
    c5 = st.checkbox("E&M level matches documentation (MDM or time documented)")
    c6 = st.checkbox("Modifiers applied correctly (bilateral, assistant, distinct service)")
    c7 = st.checkbox("No unbundling of services that should be billed together")

    st.markdown("#### Documentation")
    c8 = st.checkbox("Signed and dated note in chart")
    c9 = st.checkbox("For 99214/99215: MDM complexity or total time documented")
    c10 = st.checkbox("For procedures: Operative report complete and signed")
    c11 = st.checkbox("For ordered tests: Order in chart with diagnosis")

    all_checks = [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11]
    completed = sum(all_checks)
    total = len(all_checks)

    st.progress(completed / total)
    st.markdown(f"**{completed}/{total}** items completed")

    if completed == total:
        st.success("✅ All pre-submission checks passed. Claim is ready for submission.")
    elif completed >= total - 2:
        st.warning("⚠️ Almost complete — review remaining items before submission.")
    else:
        st.error("❌ Multiple checklist items incomplete — do not submit yet.")
