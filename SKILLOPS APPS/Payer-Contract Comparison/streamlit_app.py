import streamlit as st
import pandas as pd
from snowflake.snowpark.context import get_active_session

session = get_active_session()

st.set_page_config(page_title="Payer Contract Comparison", layout="wide")
st.title("Payer Contract Comparison Tool")
st.markdown("Compare multiple payer contracts to identify differences in pricing terms and coverage details.")

if "contracts" not in st.session_state:
    st.session_state.contracts = {}
if "comparison_result" not in st.session_state:
    st.session_state.comparison_result = None

st.sidebar.header("Contract Input")
num_contracts = st.sidebar.slider("Number of Contracts to Compare", min_value=2, max_value=5, value=2)

for i in range(1, num_contracts + 1):
    with st.sidebar.expander(f"Contract {i}", expanded=(i <= 2)):
        name = st.text_input(f"Contract Name", value=f"Contract {i}", key=f"name_{i}")

        st.subheader("Pricing Terms")
        premium = st.number_input("Monthly Premium ($)", min_value=0.0, step=50.0, key=f"premium_{i}")
        copay = st.number_input("Copayment ($)", min_value=0.0, step=5.0, key=f"copay_{i}")
        deductible = st.number_input("Annual Deductible ($)", min_value=0.0, step=100.0, key=f"deductible_{i}")
        coinsurance = st.number_input("Coinsurance (%)", min_value=0.0, max_value=100.0, step=5.0, key=f"coinsurance_{i}")
        oop_max = st.number_input("Out-of-Pocket Maximum ($)", min_value=0.0, step=500.0, key=f"oop_{i}")
        payment_terms = st.selectbox("Payment Terms", ["Monthly", "Quarterly", "Annual"], key=f"payment_{i}")

        st.subheader("Coverage Details")
        covered_services = st.multiselect(
            "Covered Services",
            ["Primary Care", "Specialist Visits", "Emergency", "Hospitalization",
             "Mental Health", "Prescription Drugs", "Preventive Care", "Rehab",
             "Lab/Diagnostics", "Telehealth"],
            key=f"services_{i}"
        )
        exclusions = st.text_area("Exclusions & Limitations", key=f"exclusions_{i}")
        prior_auth = st.multiselect(
            "Prior Authorization Required",
            ["Specialist Visits", "Imaging", "Surgery", "Prescription Drugs", "Mental Health", "Rehab"],
            key=f"prior_auth_{i}"
        )
        network = st.selectbox("Network Type", ["HMO", "PPO", "EPO", "POS"], key=f"network_{i}")
        geo_coverage = st.selectbox("Geographic Coverage", ["Local", "Regional", "National", "International"], key=f"geo_{i}")

        st.session_state.contracts[i] = {
            "name": name,
            "premium": premium,
            "copay": copay,
            "deductible": deductible,
            "coinsurance": coinsurance,
            "oop_max": oop_max,
            "payment_terms": payment_terms,
            "covered_services": covered_services,
            "exclusions": exclusions,
            "prior_auth": prior_auth,
            "network": network,
            "geo_coverage": geo_coverage,
        }

if st.button("Compare Contracts", type="primary"):
    contracts = st.session_state.contracts

    st.header("Comparison Report")

    st.subheader("Executive Summary")
    names = [contracts[i]["name"] for i in range(1, num_contracts + 1)]
    premiums = [contracts[i]["premium"] for i in range(1, num_contracts + 1)]
    lowest_premium_idx = premiums.index(min(premiums))
    highest_premium_idx = premiums.index(max(premiums))

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Lowest Premium", f"${min(premiums):,.0f}/mo", delta=names[lowest_premium_idx])
    with col2:
        st.metric("Highest Premium", f"${max(premiums):,.0f}/mo", delta=names[highest_premium_idx])
    with col3:
        premium_diff = max(premiums) - min(premiums)
        st.metric("Premium Spread", f"${premium_diff:,.0f}/mo")

    st.subheader("Pricing Comparison")
    pricing_data = {
        "Metric": ["Monthly Premium", "Copayment", "Annual Deductible", "Coinsurance (%)", "Out-of-Pocket Max", "Payment Terms"],
    }
    for i in range(1, num_contracts + 1):
        c = contracts[i]
        pricing_data[c["name"]] = [
            f"${c['premium']:,.2f}",
            f"${c['copay']:,.2f}",
            f"${c['deductible']:,.2f}",
            f"{c['coinsurance']:.1f}%",
            f"${c['oop_max']:,.2f}",
            c["payment_terms"],
        ]
    st.dataframe(pd.DataFrame(pricing_data), use_container_width=True, hide_index=True)

    st.subheader("Coverage Comparison Matrix")
    all_services = set()
    for i in range(1, num_contracts + 1):
        all_services.update(contracts[i]["covered_services"])
    all_services = sorted(all_services)

    if all_services:
        coverage_data = {"Service": all_services}
        for i in range(1, num_contracts + 1):
            c = contracts[i]
            coverage_data[c["name"]] = ["✅" if svc in c["covered_services"] else "❌" for svc in all_services]
        st.dataframe(pd.DataFrame(coverage_data), use_container_width=True, hide_index=True)
    else:
        st.info("No services selected for comparison.")

    st.subheader("Network & Authorization Comparison")
    network_data = {
        "Attribute": ["Network Type", "Geographic Coverage", "Prior Auth Requirements"],
    }
    for i in range(1, num_contracts + 1):
        c = contracts[i]
        network_data[c["name"]] = [
            c["network"],
            c["geo_coverage"],
            ", ".join(c["prior_auth"]) if c["prior_auth"] else "None",
        ]
    st.dataframe(pd.DataFrame(network_data), use_container_width=True, hide_index=True)

    st.subheader("Risk Assessment")
    for i in range(1, num_contracts + 1):
        c = contracts[i]
        risks = []
        if c["oop_max"] > 10000:
            risks.append("⚠️ High out-of-pocket maximum may expose members to significant costs")
        if c["coinsurance"] > 30:
            risks.append("⚠️ High coinsurance rate increases member cost-sharing burden")
        if len(c["covered_services"]) < 5:
            risks.append("⚠️ Limited covered services may leave gaps in care")
        if len(c["prior_auth"]) > 3:
            risks.append("⚠️ Extensive prior authorization requirements may delay care access")
        if c["network"] == "HMO" and c["geo_coverage"] == "Local":
            risks.append("⚠️ Restrictive network with limited geographic coverage")

        with st.expander(f"Risks: {c['name']}", expanded=True):
            if risks:
                for r in risks:
                    st.markdown(r)
            else:
                st.markdown("✅ No significant risks identified")

    st.subheader("Recommendations")
    best_value_idx = None
    best_score = -1
    for i in range(1, num_contracts + 1):
        c = contracts[i]
        score = len(c["covered_services"]) * 10 - c["coinsurance"] - (c["deductible"] / 1000) - (c["oop_max"] / 5000)
        if score > best_score:
            best_score = score
            best_value_idx = i

    if best_value_idx:
        best = contracts[best_value_idx]
        st.success(f"**Best Overall Value:** {best['name']} — offers the strongest combination of coverage breadth and cost-sharing terms.")

    st.markdown("**Negotiation Points:**")
    for i in range(1, num_contracts + 1):
        c = contracts[i]
        points = []
        if c["premium"] == max(premiums):
            points.append("Negotiate lower premium given market alternatives")
        if c["coinsurance"] > 20:
            points.append("Request reduced coinsurance percentage")
        if len(c["prior_auth"]) > 2:
            points.append("Negotiate fewer prior authorization requirements")
        if points:
            st.markdown(f"**{c['name']}:** " + "; ".join(points))
