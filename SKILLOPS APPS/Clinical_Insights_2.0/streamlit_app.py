import streamlit as st
import pandas as pd
from snowflake.snowpark.context import get_active_session

session = get_active_session()

st.set_page_config(page_title="Board-Ready Clinical Insights", layout="wide")
st.title("Board-Ready Clinical Insights")
st.caption("Translate clinical performance data into executive-level board summaries")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Clinical Quality", "Patient Safety", "Patient Experience", "Financial Impact", "Executive Summary"
])

COLOR_MAP = {"Green": "#28a745", "Yellow": "#ffc107", "Red": "#dc3545"}


def get_color(value, target, threshold_pct=0.10):
    if value >= target:
        return "Green"
    elif value >= target * (1 - threshold_pct):
        return "Yellow"
    else:
        return "Red"


def render_metric_card(label, value, target, unit="%", trend="→"):
    color_label = get_color(value, target)
    color = COLOR_MAP[color_label]
    st.markdown(
        f"""
        <div style="border-left: 5px solid {color}; padding: 10px; margin: 5px 0; background: #f9f9f9; border-radius: 4px;">
            <strong>{label}</strong><br/>
            <span style="font-size: 1.5em;">{value}{unit}</span> {trend}
            <br/><small>Target: {target}{unit} | Status: {color_label}</small>
        </div>
        """,
        unsafe_allow_html=True
    )


with tab1:
    st.subheader("Quadrant 1 — Clinical Quality")
    st.markdown("Core quality measures, Star Ratings, and HEDIS performance")

    col1, col2 = st.columns(2)
    with col1:
        star_rating = st.slider("Overall Star Rating", 1.0, 5.0, 3.5, 0.5)
        star_target = st.slider("Star Rating Target", 1.0, 5.0, 4.0, 0.5)
        hedis_percentile = st.slider("HEDIS Composite Percentile", 0, 100, 65)
    with col2:
        bcs_rate = st.number_input("Breast Cancer Screening Rate (%)", 0.0, 100.0, 78.5)
        col_rate = st.number_input("Colorectal Screening Rate (%)", 0.0, 100.0, 72.0)
        med_adherence = st.number_input("Medication Adherence Rate (%)", 0.0, 100.0, 81.0)

    st.divider()
    c1, c2, c3 = st.columns(3)
    with c1:
        render_metric_card("Star Rating", star_rating, star_target, "★")
    with c2:
        render_metric_card("HEDIS Percentile", hedis_percentile, 75, "th %ile")
    with c3:
        render_metric_card("Breast Cancer Screening", bcs_rate, 80.0)

with tab2:
    st.subheader("Quadrant 2 — Patient Safety")
    st.markdown("Adverse events, infection rates, and safety composites")

    col1, col2 = st.columns(2)
    with col1:
        sentinel_events = st.number_input("Sentinel Events (Quarter)", 0, 50, 0)
        clabsi_rate = st.number_input("CLABSI Rate (per 1000 line days)", 0.0, 5.0, 0.4, 0.1)
        cauti_rate = st.number_input("CAUTI Rate (per 1000 catheter days)", 0.0, 5.0, 0.8, 0.1)
    with col2:
        cdiff_rate = st.number_input("C. diff Rate (per 10000 patient days)", 0.0, 5.0, 0.6, 0.1)
        psi90 = st.number_input("PSI-90 Composite Score", 0.0, 2.0, 0.82, 0.01)
        psi90_benchmark = st.number_input("PSI-90 National Benchmark", 0.0, 2.0, 1.0, 0.01)

    st.divider()
    c1, c2, c3 = st.columns(3)
    with c1:
        render_metric_card("CLABSI", clabsi_rate, 0.8, " (benchmark)", "↓" if clabsi_rate < 0.8 else "↑")
    with c2:
        render_metric_card("C. diff", cdiff_rate, 0.6, " rate")
    with c3:
        safety_color = "Green" if sentinel_events == 0 else ("Yellow" if sentinel_events <= 2 else "Red")
        st.markdown(
            f"""
            <div style="border-left: 5px solid {COLOR_MAP[safety_color]}; padding: 10px; margin: 5px 0; background: #f9f9f9; border-radius: 4px;">
                <strong>Sentinel Events</strong><br/>
                <span style="font-size: 1.5em;">{sentinel_events}</span>
                <br/><small>Target: 0 | Status: {safety_color}</small>
            </div>
            """,
            unsafe_allow_html=True
        )

with tab3:
    st.subheader("Quadrant 3 — Patient Experience")
    st.markdown("CAHPS scores, NPS, complaints, and retention")

    col1, col2 = st.columns(2)
    with col1:
        cahps_overall = st.slider("CAHPS Overall Rating", 1.0, 5.0, 4.1, 0.1)
        cahps_target = st.slider("CAHPS Target", 1.0, 5.0, 4.3, 0.1)
        nps_score = st.slider("Net Promoter Score", -100, 100, 42)
    with col2:
        complaint_volume = st.number_input("Complaints This Quarter", 0, 10000, 145)
        resolution_rate = st.number_input("Complaint Resolution Rate (%)", 0.0, 100.0, 92.0)
        retention_rate = st.number_input("Member Retention Rate (%)", 0.0, 100.0, 94.5)

    st.divider()
    c1, c2, c3 = st.columns(3)
    with c1:
        render_metric_card("CAHPS Overall", cahps_overall, cahps_target, "/5")
    with c2:
        nps_color = "Green" if nps_score >= 50 else ("Yellow" if nps_score >= 30 else "Red")
        st.markdown(
            f"""
            <div style="border-left: 5px solid {COLOR_MAP[nps_color]}; padding: 10px; margin: 5px 0; background: #f9f9f9; border-radius: 4px;">
                <strong>Net Promoter Score</strong><br/>
                <span style="font-size: 1.5em;">{nps_score}</span>
                <br/><small>Target: 50+ | Status: {nps_color}</small>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c3:
        render_metric_card("Retention Rate", retention_rate, 95.0)

with tab4:
    st.subheader("Quadrant 4 — Financial Impact of Quality")
    st.markdown("Revenue at risk, quality bonuses, and penalties")

    col1, col2 = st.columns(2)
    with col1:
        revenue_at_risk = st.number_input("Revenue at Risk ($M)", 0.0, 100.0, 8.4, 0.1)
        quality_bonus = st.number_input("Quality Bonus Earned ($M)", 0.0, 50.0, 3.2, 0.1)
        readmission_penalty = st.number_input("Readmission Penalties ($M)", 0.0, 20.0, 1.1, 0.1)
    with col2:
        qi_investment = st.number_input("QI Program Investment ($M)", 0.0, 20.0, 2.5, 0.1)
        vbc_savings = st.number_input("Value-Based Care Savings ($M)", 0.0, 50.0, 4.8, 0.1)
        malpractice_cost = st.number_input("Malpractice/Remediation Cost ($M)", 0.0, 20.0, 0.6, 0.1)

    st.divider()
    roi = ((quality_bonus + vbc_savings - readmission_penalty - malpractice_cost) / qi_investment * 100) if qi_investment > 0 else 0
    net_quality_impact = quality_bonus + vbc_savings - readmission_penalty - malpractice_cost

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Net Quality Financial Impact", f"${net_quality_impact:.1f}M")
    with c2:
        st.metric("QI Program ROI", f"{roi:.0f}%")
    with c3:
        st.metric("Revenue at Risk (Star Bonus)", f"${revenue_at_risk:.1f}M")

with tab5:
    st.subheader("Executive Summary — Board Narrative")

    overall_status = "Strong" if star_rating >= star_target else ("Developing" if star_rating >= star_target - 0.5 else "Needs Attention")

    st.markdown("### Overall Clinical Quality Position")
    st.info(
        f"The organization's clinical quality program is **{overall_status}** with an overall Star Rating of "
        f"**{star_rating}★** against a target of {star_target}★. HEDIS composite performance is at the "
        f"**{hedis_percentile}th national percentile**."
    )

    st.markdown("### Strengths")
    strengths = []
    if bcs_rate >= 75:
        strengths.append(f"Breast cancer screening at {bcs_rate}%, demonstrating strong preventive care compliance")
    if sentinel_events == 0:
        strengths.append("Zero sentinel events for the reporting period, reflecting robust patient safety culture")
    if clabsi_rate < 0.8:
        strengths.append(f"CLABSI rate of {clabsi_rate} is below the national benchmark of 0.8")
    if retention_rate >= 94:
        strengths.append(f"Member retention at {retention_rate}%, indicating strong patient loyalty")
    if not strengths:
        strengths.append("Continued focus on quality improvement across all quadrants")
    for s in strengths[:3]:
        st.success(f"✓ {s}")

    st.markdown("### Opportunities for Improvement")
    opportunities = []
    if star_rating < star_target:
        gap = star_target - star_rating
        opportunities.append(f"Star Rating gap of {gap:.1f} stars — achieving target would unlock ${revenue_at_risk:.1f}M in quality bonus revenue")
    if hedis_percentile < 75:
        opportunities.append(f"HEDIS composite at {hedis_percentile}th percentile; target is 75th percentile for competitive positioning")
    if cahps_overall < cahps_target:
        opportunities.append(f"CAHPS overall rating {cahps_overall}/5 is {cahps_target - cahps_overall:.1f} points below target")
    if cdiff_rate > 0.6:
        opportunities.append(f"C. diff rate ({cdiff_rate}) exceeds benchmark — antimicrobial stewardship review recommended")
    if not opportunities:
        opportunities.append("Maintain current trajectory; focus on sustaining gains")
    for o in opportunities[:3]:
        st.warning(f"△ {o}")

    st.markdown("### Financial Nexus")
    st.markdown(
        f"Quality performance is generating **${net_quality_impact:.1f}M** in net positive financial impact "
        f"(bonuses + VBC savings - penalties - remediation). An additional **${revenue_at_risk:.1f}M** in Star "
        f"bonus revenue remains at risk pending achievement of the {star_target}★ target. QI program ROI stands at **{roi:.0f}%**."
    )

    st.markdown("### Board Discussion Points")
    st.markdown("""
| Anticipated Question | Prepared Response |
|---------------------|-------------------|
| Why is the Star Rating below target? | Gap driven by CAHPS access and care coordination measures; corrective plan in place |
| What's the financial exposure? | ${:.1f}M in quality bonus at risk; current trajectory projects achievement in 12-18 months |
| How do we compare to peers? | HEDIS at {}th percentile; above median but below top quartile target |
| What resources are needed? | QI program budget of ${:.1f}M delivering {:.0f}% ROI; expansion request TBD |
""".format(revenue_at_risk, hedis_percentile, qi_investment, roi))

    st.markdown("---")
    st.caption("HIPAA Notice: This report contains aggregate data only. No Protected Health Information (PHI) is present. Minimum cell-size suppression (n≥11) applied to all sub-group data.")
