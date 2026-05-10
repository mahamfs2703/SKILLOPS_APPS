import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date

st.set_page_config(page_title="HEDIS Measure Tracking", page_icon="🏥", layout="wide")

MEASURES = {
    "COL": {
        "name": "Colorectal Cancer Screening",
        "age_range": (45, 75),
        "product_lines": ["Commercial", "Medicaid", "Medicare"],
        "exclusions": [
            "Prior colectomy (Z90.49, Z90.5)",
            "Colorectal cancer diagnosis (active or historical)",
            "Colostomy",
        ],
        "numerator_criteria": [
            "FIT/FOBT in measurement year",
            "Flexible sigmoidoscopy in last 5 years",
            "Colonoscopy in last 10 years",
            "CT colonography in last 5 years",
        ],
        "inverted": False,
    },
    "BCS": {
        "name": "Breast Cancer Screening",
        "age_range": (50, 74),
        "product_lines": ["Commercial", "Medicaid", "Medicare"],
        "exclusions": [
            "Bilateral mastectomy (Z90.13)",
            "Unilateral mastectomy right + left (Z90.11, Z90.12)",
        ],
        "numerator_criteria": ["Mammogram in last 2 years"],
        "inverted": False,
    },
    "HPC": {
        "name": "HbA1c Poor Control (Diabetes)",
        "age_range": (18, 75),
        "product_lines": ["Commercial", "Medicaid", "Medicare"],
        "exclusions": [
            "Documented diabetes reversal/reclassification",
            "Gestational diabetes (O24.4x)",
        ],
        "numerator_criteria": ["HbA1c > 9.0% (LOWER rate = BETTER performance)"],
        "inverted": True,
    },
    "PDC": {
        "name": "Medication Adherence (PDC)",
        "age_range": (18, 99),
        "product_lines": ["Commercial", "Medicaid", "Medicare"],
        "exclusions": [
            "Death during measurement year",
            "Not continuously enrolled for required period",
        ],
        "numerator_criteria": ["Proportion of Days Covered >= 80%"],
        "inverted": False,
    },
    "FUH": {
        "name": "Follow-Up After Hospitalization for Mental Illness",
        "age_range": (6, 99),
        "product_lines": ["Commercial", "Medicaid", "Medicare"],
        "exclusions": [
            "Readmissions within follow-up window (do not count as follow-up)",
        ],
        "numerator_criteria": [
            "7-day follow-up visit (starts day after discharge)",
            "30-day follow-up visit (starts day after discharge)",
            "Telehealth visits qualify if coded as qualifying visit type",
        ],
        "inverted": False,
    },
}

NCQA_BENCHMARKS = {
    "COL": {"25th": 50.0, "50th": 58.0, "75th": 65.0, "90th": 72.0},
    "BCS": {"25th": 55.0, "50th": 63.0, "75th": 70.0, "90th": 77.0},
    "HPC": {"25th": 45.0, "50th": 38.0, "75th": 30.0, "90th": 22.0},
    "PDC": {"25th": 70.0, "50th": 76.0, "75th": 82.0, "90th": 88.0},
    "FUH": {"25th": 35.0, "50th": 45.0, "75th": 55.0, "90th": 65.0},
}


def get_percentile_rating(measure_code, rate):
    benchmarks = NCQA_BENCHMARKS.get(measure_code, {})
    if not benchmarks:
        return "N/A"
    is_inverted = MEASURES[measure_code]["inverted"]
    if is_inverted:
        if rate <= benchmarks["90th"]:
            return ">=90th Percentile"
        elif rate <= benchmarks["75th"]:
            return "75th-89th Percentile"
        elif rate <= benchmarks["50th"]:
            return "50th-74th Percentile"
        elif rate <= benchmarks["25th"]:
            return "25th-49th Percentile"
        else:
            return "<25th Percentile"
    else:
        if rate >= benchmarks["90th"]:
            return ">=90th Percentile"
        elif rate >= benchmarks["75th"]:
            return "75th-89th Percentile"
        elif rate >= benchmarks["50th"]:
            return "50th-74th Percentile"
        elif rate >= benchmarks["25th"]:
            return "25th-49th Percentile"
        else:
            return "<25th Percentile"


def generate_sample_data(measure_code, product_line, measurement_year):
    np.random.seed(hash(f"{measure_code}{product_line}{measurement_year}") % 2**32)
    measure = MEASURES[measure_code]
    eligible_pop = np.random.randint(800, 5000)
    exclusion_rate = np.random.uniform(0.03, 0.12)
    exclusions_applied = int(eligible_pop * exclusion_rate)
    denominator = eligible_pop - exclusions_applied
    if measure["inverted"]:
        compliance_rate = np.random.uniform(0.25, 0.50)
    else:
        compliance_rate = np.random.uniform(0.45, 0.80)
    numerator = int(denominator * compliance_rate)
    rate = (numerator / denominator) * 100 if denominator > 0 else 0
    gap_count = denominator - numerator
    return {
        "eligible_population": eligible_pop,
        "exclusions_applied": exclusions_applied,
        "denominator": denominator,
        "numerator": numerator,
        "rate": round(rate, 2),
        "gap_count": gap_count,
    }


st.title("HEDIS Measure Tracking Dashboard")
st.caption("Calculate and track HEDIS measure rates with NCQA technical specifications")

st.sidebar.header("Configuration")
measurement_year = st.sidebar.selectbox(
    "Measurement Year", options=[2026, 2025, 2024, 2023], index=0
)
methodology = st.sidebar.radio(
    "Methodology", options=["Administrative", "Hybrid", "Medical Record Only"]
)
selected_product_lines = st.sidebar.multiselect(
    "Product Lines",
    options=["Commercial", "Medicaid", "Medicare"],
    default=["Commercial", "Medicaid", "Medicare"],
)
selected_measures = st.sidebar.multiselect(
    "Measures",
    options=list(MEASURES.keys()),
    default=list(MEASURES.keys()),
    format_func=lambda x: f"{x} - {MEASURES[x]['name']}",
)

if methodology == "Administrative":
    st.sidebar.info(
        "Administrative rates may understate true performance due to services not captured in claims."
    )

tab1, tab2, tab3, tab4 = st.tabs(
    ["Rate Summary", "Measure Detail", "Gap Analysis", "Exclusion Reference"]
)

with tab1:
    st.subheader(f"HEDIS Rate Summary - {measurement_year}")
    summary_data = []
    for measure_code in selected_measures:
        for pl in selected_product_lines:
            if pl in MEASURES[measure_code]["product_lines"]:
                data = generate_sample_data(measure_code, pl, measurement_year)
                percentile = get_percentile_rating(measure_code, data["rate"])
                summary_data.append(
                    {
                        "Measure": measure_code,
                        "Measure Name": MEASURES[measure_code]["name"],
                        "Product Line": pl,
                        "Denominator": data["denominator"],
                        "Numerator": data["numerator"],
                        "Rate (%)": data["rate"],
                        "NCQA Percentile": percentile,
                        "Gaps": data["gap_count"],
                    }
                )
    if summary_data:
        df_summary = pd.DataFrame(summary_data)
        st.dataframe(df_summary, use_container_width=True, hide_index=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            avg_rate = df_summary["Rate (%)"].mean()
            st.metric("Average Rate", f"{avg_rate:.1f}%")
        with col2:
            total_gaps = df_summary["Gaps"].sum()
            st.metric("Total Care Gaps", f"{total_gaps:,}")
        with col3:
            total_denom = df_summary["Denominator"].sum()
            st.metric("Total Eligible Members", f"{total_denom:,}")

with tab2:
    st.subheader("Measure Detail")
    detail_measure = st.selectbox(
        "Select Measure",
        options=selected_measures,
        format_func=lambda x: f"{x} - {MEASURES[x]['name']}",
        key="detail_measure",
    )
    if detail_measure:
        measure_info = MEASURES[detail_measure]
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Age Range:** {measure_info['age_range'][0]} - {measure_info['age_range'][1]}")
            st.markdown(f"**Product Lines:** {', '.join(measure_info['product_lines'])}")
            if measure_info["inverted"]:
                st.warning("This is an INVERTED measure: LOWER rate = BETTER performance")
        with col2:
            st.markdown("**Numerator Criteria:**")
            for criteria in measure_info["numerator_criteria"]:
                st.markdown(f"- {criteria}")

        st.markdown("---")
        st.markdown("**Rates by Product Line:**")
        detail_data = []
        for pl in selected_product_lines:
            if pl in measure_info["product_lines"]:
                data = generate_sample_data(detail_measure, pl, measurement_year)
                detail_data.append({"Product Line": pl, **data})
        if detail_data:
            df_detail = pd.DataFrame(detail_data)
            df_detail.columns = [
                "Product Line",
                "Eligible Pop",
                "Exclusions",
                "Denominator",
                "Numerator",
                "Rate (%)",
                "Gaps",
            ]
            st.dataframe(df_detail, use_container_width=True, hide_index=True)

with tab3:
    st.subheader("Gap Analysis - Members Eligible for Outreach")
    gap_measure = st.selectbox(
        "Select Measure for Gap List",
        options=selected_measures,
        format_func=lambda x: f"{x} - {MEASURES[x]['name']}",
        key="gap_measure",
    )
    gap_pl = st.selectbox(
        "Product Line", options=selected_product_lines, key="gap_pl"
    )
    if gap_measure and gap_pl:
        data = generate_sample_data(gap_measure, gap_pl, measurement_year)
        st.metric("Members with Care Gaps", f"{data['gap_count']:,}")
        st.caption(
            "These members are in the denominator but have not met numerator criteria. "
            "They are eligible for outreach and gap closure activities."
        )
        st.markdown("---")
        st.markdown("**Outreach Prioritization Notes:**")
        st.markdown("- Verify exclusions before outreach (e.g., colectomy for COL, mastectomy for BCS)")
        st.markdown("- Confirm continuous enrollment is still active")
        st.markdown("- Check if services were rendered but not yet coded in claims")

with tab4:
    st.subheader("Clinical Exclusion Reference")
    st.caption("Critical exclusions that are frequently missed in HEDIS reporting")
    for code, measure in MEASURES.items():
        if code in selected_measures:
            with st.expander(f"{code} - {measure['name']}"):
                st.markdown("**Exclusions to Apply:**")
                for exc in measure["exclusions"]:
                    st.markdown(f"- {exc}")
                st.markdown("")
                st.markdown("**Denominator Requirements:**")
                st.markdown("1. Continuous enrollment (typically 11 of 12 months)")
                st.markdown(f"2. Age {measure['age_range'][0]}-{measure['age_range'][1]} during measurement year")
                st.markdown("3. Separate reporting by product line")

    st.markdown("---")
    st.markdown("**Governance Notes:**")
    st.markdown("- HEDIS specs update annually; review each January")
    st.markdown("- Colectomy exclusion for COL is the most frequently missed")
    st.markdown("- Mastectomy exclusion requires checking claims AND operative notes")
    st.markdown("- All rates for external reporting require Quality team validation")
