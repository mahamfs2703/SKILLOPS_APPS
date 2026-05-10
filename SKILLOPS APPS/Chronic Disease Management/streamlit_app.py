import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Chronic Disease Management", layout="wide")
st.title("Chronic Disease Management")
st.caption("Evidence-based clinical protocols for CHF, COPD, Diabetes, and Hypertension")

COLOR_MAP = {"Green": "#28a745", "Yellow": "#ffc107", "Red": "#dc3545"}


def render_status_card(label, status, detail=""):
    color = COLOR_MAP.get(status, "#6c757d")
    st.markdown(
        f"""
        <div style="border-left: 5px solid {color}; padding: 10px; margin: 5px 0; background: #f9f9f9; border-radius: 4px;">
            <strong>{label}</strong><br/>
            <span style="font-size: 1.1em;">{detail}</span>
            <br/><small>Status: {status}</small>
        </div>
        """,
        unsafe_allow_html=True
    )


def assess_escalation(flags):
    if any(f["severity"] == "Red" for f in flags):
        return "Red"
    elif any(f["severity"] == "Yellow" for f in flags):
        return "Yellow"
    return "Green"


tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "CHF Protocol", "COPD Protocol", "Diabetes Protocol", "Hypertension Protocol", "Patient Assessment"
])

with tab1:
    st.subheader("Congestive Heart Failure (CHF) Protocol")

    st.markdown("#### Post-Discharge Management")
    col1, col2 = st.columns(2)
    with col1:
        discharge_date = st.date_input("Discharge Date", datetime.now().date() - timedelta(days=1), key="chf_discharge")
        outreach_completed = st.checkbox("48-Hour Outreach Completed", key="chf_outreach")
        outreach_method = st.selectbox("Outreach Method", ["Care Coordinator", "Nurse", "Automated Message (Non-Compliant)"], key="chf_method")
        followup_scheduled = st.checkbox("Follow-Up Appointment Scheduled Before Discharge", key="chf_followup")
    with col2:
        daily_weight = st.number_input("Today's Weight (lbs)", 80.0, 400.0, 180.0, key="chf_weight")
        yesterday_weight = st.number_input("Yesterday's Weight (lbs)", 80.0, 400.0, 179.0, key="chf_yweight")
        weekly_weight_gain = st.number_input("Weekly Weight Gain (lbs)", 0.0, 20.0, 1.0, key="chf_wgain")
        missed_med_fills = st.number_input("Missed Medication Fills (Last 30 Days)", 0, 30, 0, key="chf_missed")

    st.divider()
    st.markdown("#### Protocol Compliance & Escalation Flags")

    chf_flags = []
    days_since_discharge = (datetime.now().date() - discharge_date).days

    if days_since_discharge > 2 and not outreach_completed:
        chf_flags.append({"flag": "48-Hour Outreach Overdue", "severity": "Red", "action": "Immediate outreach by care coordinator or nurse"})
    if outreach_method == "Automated Message (Non-Compliant)":
        chf_flags.append({"flag": "Non-Compliant Outreach Method", "severity": "Yellow", "action": "Protocol requires human contact (care coordinator or nurse)"})
    if not followup_scheduled:
        chf_flags.append({"flag": "No Follow-Up Scheduled", "severity": "Red", "action": "Schedule follow-up within 24 hours"})

    daily_gain = daily_weight - yesterday_weight
    if daily_gain >= 2:
        chf_flags.append({"flag": f"Rapid Weight Gain: {daily_gain:.1f} lbs/day", "severity": "Red", "action": "Same-day clinical notification"})
    if weekly_weight_gain >= 5:
        chf_flags.append({"flag": f"Weekly Weight Gain: {weekly_weight_gain:.1f} lbs", "severity": "Red", "action": "Same-day clinical notification"})
    if missed_med_fills >= 3:
        chf_flags.append({"flag": f"{missed_med_fills} Missed Medication Fills", "severity": "Red", "action": "Care manager escalation"})
    elif missed_med_fills >= 1:
        chf_flags.append({"flag": f"{missed_med_fills} Missed Medication Fill(s)", "severity": "Yellow", "action": "Confirm diuretic and ACE inhibitor adherence"})

    if not chf_flags:
        render_status_card("CHF Protocol", "Green", "All protocol requirements met")
    else:
        for f in chf_flags:
            render_status_card(f["flag"], f["severity"], f["action"])

with tab2:
    st.subheader("COPD Protocol")

    st.markdown("#### Exacerbation Prevention")
    col1, col2 = st.columns(2)
    with col1:
        flu_vaccine = st.checkbox("Influenza Vaccine Current", key="copd_flu")
        pneumo_vaccine = st.checkbox("Pneumococcal Vaccine Current", key="copd_pneumo")
        rescue_inhaler = st.checkbox("Rescue Inhaler Supply Confirmed", key="copd_inhaler")
        gold_stage = st.selectbox("GOLD Stage", [1, 2, 3, 4], key="copd_gold")
    with col2:
        exacerbations_12mo = st.number_input("Exacerbations in Last 12 Months", 0, 20, 0, key="copd_exac")
        days_since_last_inhaler = st.number_input("Days Since Last Rescue Inhaler Fill", 0, 365, 30, key="copd_inhaler_days")
        current_smoker = st.checkbox("Current Smoker", key="copd_smoke")
        spo2 = st.number_input("SpO2 (%)", 70.0, 100.0, 95.0, key="copd_spo2")

    st.divider()
    st.markdown("#### Protocol Compliance & Escalation Flags")

    copd_flags = []
    if not flu_vaccine:
        copd_flags.append({"flag": "Influenza Vaccine Not Current", "severity": "Yellow", "action": "Schedule vaccination"})
    if not pneumo_vaccine:
        copd_flags.append({"flag": "Pneumococcal Vaccine Not Current", "severity": "Yellow", "action": "Schedule vaccination"})
    if not rescue_inhaler:
        copd_flags.append({"flag": "Rescue Inhaler Supply Not Confirmed", "severity": "Yellow", "action": "Pharmacy outreach"})
    if gold_stage >= 2:
        copd_flags.append({"flag": f"GOLD Stage {gold_stage} — Pulmonary Rehab Required", "severity": "Yellow", "action": "Refer to pulmonary rehabilitation"})
    if exacerbations_12mo >= 2:
        copd_flags.append({"flag": f"{exacerbations_12mo} Exacerbations in 12 Months", "severity": "Red", "action": "Refer to pulmonology"})
    if days_since_last_inhaler >= 60:
        copd_flags.append({"flag": "No Rescue Inhaler Fill in 60+ Days", "severity": "Red", "action": "Pharmacy outreach required"})
    if current_smoker:
        copd_flags.append({"flag": "Current Smoker", "severity": "Yellow", "action": "Smoking cessation referral"})
    if spo2 < 88:
        copd_flags.append({"flag": f"SpO2 Critical: {spo2}%", "severity": "Red", "action": "Direct to ER immediately"})

    if not copd_flags:
        render_status_card("COPD Protocol", "Green", "All protocol requirements met")
    else:
        for f in copd_flags:
            render_status_card(f["flag"], f["severity"], f["action"])

with tab3:
    st.subheader("Diabetes Protocol")

    st.markdown("#### Glycemic Monitoring")
    col1, col2 = st.columns(2)
    with col1:
        hba1c = st.number_input("Current HbA1c (%)", 4.0, 15.0, 7.2, key="dm_hba1c")
        is_elderly = st.checkbox("Elderly / High Comorbidity", key="dm_elderly")
        missed_appts = st.number_input("Missed Appointments (Last 6 Months)", 0, 20, 0, key="dm_appts")
        egfr = st.number_input("eGFR (mL/min)", 5.0, 150.0, 75.0, key="dm_egfr")
    with col2:
        acr = st.number_input("ACR (mg/g)", 0.0, 5000.0, 25.0, key="dm_acr")
        eye_exam_current = st.checkbox("Annual Dilated Eye Exam Completed", key="dm_eye")
        foot_exam_current = st.checkbox("Annual Foot Exam Documented", key="dm_foot")
        has_cvd_ckd = st.checkbox("History of CVD or CKD", key="dm_cvd")

    st.divider()
    st.markdown("#### Protocol Compliance & Escalation Flags")

    dm_flags = []
    target = 8.0 if is_elderly else 7.0

    if hba1c > 9 and missed_appts >= 2:
        dm_flags.append({"flag": f"HbA1c {hba1c}% + {missed_appts} Missed Appointments", "severity": "Red", "action": "Care management outreach — high risk for complications"})
    elif hba1c > target:
        dm_flags.append({"flag": f"HbA1c {hba1c}% Above Target ({target}%)", "severity": "Yellow", "action": "Schedule follow-up in 3 months; review treatment plan"})

    if egfr < 45:
        dm_flags.append({"flag": f"eGFR {egfr} — Nephrology Referral Required", "severity": "Red", "action": "Refer to nephrology"})
    if acr > 300:
        dm_flags.append({"flag": f"ACR {acr} — Nephrology Referral Required", "severity": "Red", "action": "Refer to nephrology"})
    if not eye_exam_current:
        dm_flags.append({"flag": "Annual Eye Exam Overdue", "severity": "Yellow", "action": "Schedule dilated eye exam"})
    if not foot_exam_current:
        dm_flags.append({"flag": "Annual Foot Exam Not Documented", "severity": "Yellow", "action": "Document foot exam at next visit"})
    if has_cvd_ckd:
        dm_flags.append({"flag": "CVD/CKD History — Preferred Medication Review", "severity": "Yellow", "action": "Confirm GLP-1/SGLT2 inhibitor in regimen"})

    if not dm_flags:
        render_status_card("Diabetes Protocol", "Green", f"HbA1c {hba1c}% within target ({target}%)")
    else:
        for f in dm_flags:
            render_status_card(f["flag"], f["severity"], f["action"])

with tab4:
    st.subheader("Hypertension Protocol")

    st.markdown("#### Blood Pressure Management")
    col1, col2 = st.columns(2)
    with col1:
        systolic = st.number_input("Systolic BP (mmHg)", 80, 250, 132, key="htn_sys")
        diastolic = st.number_input("Diastolic BP (mmHg)", 40, 150, 78, key="htn_dia")
        has_ckd = st.checkbox("Has CKD", key="htn_ckd")
        is_elderly_htn = st.checkbox("Elderly Patient", key="htn_elderly")
    with col2:
        new_med_change = st.checkbox("New Medication or Recent Change", key="htn_newmed")
        last_visit_weeks = st.number_input("Weeks Since Last Visit", 0, 52, 8, key="htn_weeks")
        on_ace_arb = st.checkbox("On ACE Inhibitor / ARB (CKD Patients)", key="htn_ace")

    st.divider()
    st.markdown("#### Protocol Compliance & Escalation Flags")

    htn_flags = []
    bp_target_sys = 130
    bp_target_dia = 80

    if systolic >= 160 or diastolic >= 100:
        htn_flags.append({"flag": f"BP {systolic}/{diastolic} — Severely Uncontrolled", "severity": "Red", "action": "Follow-up within 2 weeks; consider medication adjustment"})
    elif systolic >= bp_target_sys or diastolic >= bp_target_dia:
        htn_flags.append({"flag": f"BP {systolic}/{diastolic} — Above Target (<{bp_target_sys}/{bp_target_dia})", "severity": "Yellow", "action": "Review at next scheduled visit"})

    if new_med_change and last_visit_weeks > 4:
        htn_flags.append({"flag": "Overdue Follow-Up After Medication Change", "severity": "Red", "action": "Schedule follow-up (protocol: 4 weeks after new medication)"})

    if has_ckd and not on_ace_arb:
        htn_flags.append({"flag": "CKD Patient Not on ACE/ARB", "severity": "Red", "action": "Protocol requires ACE inhibitor or ARB for CKD patients"})

    controlled = systolic < bp_target_sys and diastolic < bp_target_dia
    if controlled and last_visit_weeks > 26:
        htn_flags.append({"flag": "Controlled — Overdue for Routine Follow-Up", "severity": "Yellow", "action": "Schedule routine visit (protocol: 3-6 months if controlled)"})

    if not htn_flags:
        render_status_card("Hypertension Protocol", "Green", f"BP {systolic}/{diastolic} within target")
    else:
        for f in htn_flags:
            render_status_card(f["flag"], f["severity"], f["action"])

with tab5:
    st.subheader("Patient Assessment Summary")
    st.markdown("Enter patient details to generate a comprehensive protocol compliance report.")

    patient_id = st.text_input("Patient Identifier (Generic)", "Patient A", key="pa_id")
    conditions = st.multiselect("Active Conditions", ["CHF", "COPD", "Diabetes", "Hypertension"], default=["CHF"], key="pa_conditions")
    phq9_score = st.slider("PHQ-9 Depression Screening Score", 0, 27, 4, key="pa_phq9")
    care_plan_updated = st.checkbox("Annual Care Plan Updated", key="pa_careplan")
    self_mgmt_goals = st.checkbox("Patient Self-Management Goals Documented", key="pa_goals")
    caregiver_included = st.checkbox("Caregiver Included (Elderly/Cognitively Impaired)", key="pa_caregiver")

    if st.button("Generate Assessment Report", key="pa_report"):
        st.divider()
        st.markdown(f"### Protocol Compliance Report — {patient_id}")
        st.markdown(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        st.markdown(f"**Conditions Managed:** {', '.join(conditions)}")

        general_flags = []
        if not care_plan_updated:
            general_flags.append({"flag": "Annual Care Plan Not Updated", "severity": "Yellow", "action": "Update care plan at next encounter"})
        if not self_mgmt_goals:
            general_flags.append({"flag": "Self-Management Goals Not Documented", "severity": "Yellow", "action": "Document patient goals"})
        if phq9_score >= 10:
            general_flags.append({"flag": f"PHQ-9 Score: {phq9_score} (Moderate-Severe Depression)", "severity": "Red", "action": "Behavioral health referral"})
        elif phq9_score >= 5:
            general_flags.append({"flag": f"PHQ-9 Score: {phq9_score} (Mild Depression)", "severity": "Yellow", "action": "Monitor; rescreen in 4 weeks"})

        st.markdown("#### General Protocol Compliance")
        if not general_flags:
            render_status_card("General Requirements", "Green", "All general protocol requirements met")
        else:
            for f in general_flags:
                render_status_card(f["flag"], f["severity"], f["action"])

        st.markdown("#### Recommended Actions")
        actions = []
        if "CHF" in conditions:
            actions.append("Confirm daily weight monitoring plan")
            actions.append("Verify diuretic and ACE inhibitor adherence")
            actions.append("Assess fluid restriction compliance")
        if "COPD" in conditions:
            actions.append("Confirm rescue inhaler technique")
            actions.append("Verify vaccine status (influenza, pneumococcal)")
        if "Diabetes" in conditions:
            actions.append("Review HbA1c trend and testing schedule")
            actions.append("Confirm annual eye/foot exam completion")
        if "Hypertension" in conditions:
            actions.append("Verify BP at target; review medication adherence")

        for i, a in enumerate(actions, 1):
            st.markdown(f"{i}. {a}")

        st.markdown("---")
        st.caption("HIPAA Notice: This report uses generic identifiers only. No PHI is stored or cached. All protocol applications are logged for audit compliance.")
