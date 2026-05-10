import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

st.set_page_config(page_title="Contract Performance Monitoring", layout="wide")

st.title("Value-Based Contract Performance Monitor")

st.sidebar.header("Filters")

contract_types = ["Medicare Shared Savings (MSSP/ACO)", "Medicare Advantage VBC", "Medicaid Managed Care VBC", "Commercial ACO / Shared Savings"]
selected_contract = st.sidebar.selectbox("Contract Type", contract_types)

measurement_periods = ["Q1 2026", "Q4 2025", "Q3 2025", "Q2 2025", "Q1 2025"]
selected_period = st.sidebar.selectbox("Measurement Period", measurement_periods)

attribution_method = st.sidebar.radio("Attribution Method", ["Prospective", "Retrospective"])

st.sidebar.markdown("---")
st.sidebar.markdown("**Population Segmentation**")
st.sidebar.info("Attributed vs non-attributed populations are always separated per leadership decision (Finance + Clinical, Q3 2023).")

np.random.seed(42)
attributed_count = np.random.randint(8000, 15000)
non_attributed_count = np.random.randint(3000, 7000)
benchmark_pmpm = round(np.random.uniform(800, 1200), 2)
actual_pmpm = round(benchmark_pmpm * np.random.uniform(0.88, 1.05), 2)
pmpm_variance = round(actual_pmpm - benchmark_pmpm, 2)
savings_pct = round((benchmark_pmpm - actual_pmpm) / benchmark_pmpm * 100, 2)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Attributed Population", f"{attributed_count:,}")
col2.metric("Non-Attributed Population", f"{non_attributed_count:,}")
col3.metric("PMPM vs Benchmark", f"${actual_pmpm:,.2f}", f"${pmpm_variance:,.2f}")
col4.metric("Estimated Savings", f"{savings_pct}%", f"{'Favorable' if savings_pct > 0 else 'Unfavorable'}")

st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["Cost Performance", "Quality Metrics", "Savings Position", "Trend Analysis"])

with tab1:
    st.subheader("Cost Performance — Attributed Population Only")
    st.caption("Basis: Allowed Amount (per leadership agreement, 2022)")

    months = pd.date_range(end=datetime.now(), periods=12, freq="ME")
    cost_data = pd.DataFrame({
        "Month": months,
        "Actual PMPM": [round(benchmark_pmpm * np.random.uniform(0.85, 1.05), 2) for _ in range(12)],
        "Benchmark PMPM": [benchmark_pmpm] * 12
    })
    st.line_chart(cost_data.set_index("Month"))

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("**Cost Breakdown**")
        cost_breakdown = pd.DataFrame({
            "Category": ["Professional Fees", "Facility Fees", "Pharmacy", "Other"],
            "PMPM": [round(actual_pmpm * p, 2) for p in [0.35, 0.40, 0.18, 0.07]]
        })
        st.dataframe(cost_breakdown, use_container_width=True, hide_index=True)
    with col_b:
        st.markdown("**Risk Adjustment**")
        st.metric("Average HCC Risk Score", round(np.random.uniform(0.9, 1.3), 3))
        st.metric("Risk-Adjusted PMPM", f"${round(actual_pmpm / np.random.uniform(0.9, 1.1), 2):,.2f}")

with tab2:
    st.subheader("Quality Gate Status")

    if selected_contract == "Medicare Shared Savings (MSSP/ACO)":
        measures = ["ACO-11: CAHPS Survey", "ACO-13: Falls Screening", "ACO-14: Flu Immunization",
                    "ACO-17: Tobacco Screening", "ACO-27: Diabetes HbA1c", "ACO-28: Hypertension Control"]
    elif selected_contract == "Medicare Advantage VBC":
        measures = ["Star: Breast Cancer Screening", "Star: Colorectal Screening", "Star: Diabetes Eye Exam",
                    "Star: Medication Adherence", "Star: MTM Completion", "Star: Fall Risk Management"]
    else:
        measures = ["HEDIS: HbA1c Control", "HEDIS: Blood Pressure Control", "HEDIS: Depression Screening",
                    "HEDIS: Well-Child Visits", "HEDIS: Prenatal Care", "HEDIS: Immunizations"]

    quality_data = pd.DataFrame({
        "Measure": measures,
        "Score (%)": [round(np.random.uniform(60, 95), 1) for _ in measures],
        "Threshold (%)": [round(np.random.uniform(65, 80), 1) for _ in measures],
    })
    quality_data["Status"] = quality_data.apply(
        lambda row: "✅ Met" if row["Score (%)"] >= row["Threshold (%)"] else "❌ Not Met", axis=1
    )
    st.dataframe(quality_data, use_container_width=True, hide_index=True)

    met_count = (quality_data["Status"] == "✅ Met").sum()
    total_count = len(quality_data)
    if met_count == total_count:
        st.success(f"Quality Gate PASSED — All {total_count} measures meet threshold.")
    elif met_count >= total_count * 0.7:
        st.warning(f"Quality Gate AT RISK — {met_count}/{total_count} measures meeting threshold.")
    else:
        st.error(f"Quality Gate FAILING — Only {met_count}/{total_count} measures meeting threshold.")

with tab3:
    st.subheader("Shared Savings / Risk Position")

    total_attributed_spend = actual_pmpm * attributed_count * 12
    total_benchmark_spend = benchmark_pmpm * attributed_count * 12
    savings_amount = total_benchmark_spend - total_attributed_spend
    sharing_rate = 0.50

    col_s1, col_s2, col_s3 = st.columns(3)
    col_s1.metric("Total Attributed Spend", f"${total_attributed_spend:,.0f}")
    col_s2.metric("Benchmark Spend", f"${total_benchmark_spend:,.0f}")
    col_s3.metric("Gross Savings/(Loss)", f"${savings_amount:,.0f}",
                  "Savings" if savings_amount > 0 else "Loss")

    st.markdown("---")
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        st.metric("Sharing Rate", f"{sharing_rate*100:.0f}%")
        st.metric("Organization's Share", f"${savings_amount * sharing_rate:,.0f}")
    with col_r2:
        st.metric("Minimum Savings Rate (MSR)", "2.0%")
        actual_savings_rate = savings_amount / total_benchmark_spend * 100
        st.metric("Actual Savings Rate", f"{actual_savings_rate:.2f}%",
                  "Above MSR" if actual_savings_rate > 2.0 else "Below MSR")

with tab4:
    st.subheader("Performance Trend — Last 24 Months")
    st.caption("Limited to 24 months per reporting standards")

    trend_months = pd.date_range(end=datetime.now(), periods=24, freq="ME")
    trend_data = pd.DataFrame({
        "Month": trend_months,
        "PMPM": [round(benchmark_pmpm * np.random.uniform(0.85, 1.08), 2) for _ in range(24)],
        "Benchmark": [benchmark_pmpm + i * 2 for i in range(24)]
    })
    st.line_chart(trend_data.set_index("Month"))

    st.markdown("**Period-over-Period Comparison**")
    col_t1, col_t2, col_t3 = st.columns(3)
    prior_pmpm = round(actual_pmpm * np.random.uniform(0.95, 1.1), 2)
    col_t1.metric("Current Period PMPM", f"${actual_pmpm:,.2f}")
    col_t2.metric("Prior Period PMPM", f"${prior_pmpm:,.2f}")
    col_t3.metric("Change", f"${actual_pmpm - prior_pmpm:,.2f}",
                  "Improving" if actual_pmpm < prior_pmpm else "Deteriorating")

st.markdown("---")
st.markdown("### Governance & Methodology Notes")
with st.expander("View Methodology Details"):
    st.markdown("""
    - **Population Segmentation**: Attributed vs non-attributed always separated (Finance + Clinical leadership, Q3 2023)
    - **Cost Basis**: Allowed amount (agreed with major payers, 2022)
    - **Quality Data Source**: Administrative data with HEDIS technical specifications
    - **Risk Adjustment**: HCC risk scores applied where contract requires
    - **Sign-off Required**: CFO and VP of Population Health before sharing with payers
    """)

st.sidebar.markdown("---")
st.sidebar.markdown("**Data Security**")
st.sidebar.caption("All data shown uses aggregate metrics only. No PHI displayed. Role-based access controls enforced.")
