import streamlit as st
import json
from snowflake.snowpark.context import get_active_session

session = get_active_session()

st.set_page_config(page_title="Precision Medicine Stratification", layout="wide")
st.title("Precision Medicine Patient Stratification")
st.markdown("Stratify patients based on genomic, clinical, and pharmacogenomic data to generate personalized treatment recommendations.")

with st.sidebar:
    st.header("Patient Input")
    disease = st.text_input("Disease / Condition", placeholder="e.g., Non-Small Cell Lung Cancer")
    age = st.number_input("Age", min_value=0, max_value=120, value=55)
    sex = st.selectbox("Sex", ["Male", "Female", "Other"])

    st.subheader("Genomic Data")
    germline_variants = st.text_area("Germline Variants (one per line)", placeholder="e.g., BRCA1 c.5266dupC\nTP53 R175H")
    somatic_mutations = st.text_area("Somatic Mutations (one per line)", placeholder="e.g., EGFR L858R\nKRAS G12C")
    tumor_mutational_burden = st.number_input("Tumor Mutational Burden (mut/Mb)", min_value=0.0, value=0.0, step=0.1)

    st.subheader("Clinical Parameters")
    biomarkers = st.text_area("Biomarkers (name: value, one per line)", placeholder="e.g., PD-L1 TPS: 80%\nHER2 IHC: 3+")
    medications = st.text_area("Current Medications (one per line)", placeholder="e.g., Metformin\nWarfarin")
    comorbidities = st.text_area("Comorbidities (one per line)", placeholder="e.g., Type 2 Diabetes\nHypertension")
    family_history = st.text_area("Family History (one per line)", placeholder="e.g., Mother: Breast cancer age 45\nFather: Colon cancer age 60")

    run_analysis = st.button("Run Stratification", type="primary", use_container_width=True)

def parse_lines(text):
    return [line.strip() for line in text.strip().split("\n") if line.strip()] if text.strip() else []

def compute_risk_score(disease, germline, somatic, tmb, biomarkers_list, comorbidities_list):
    score = 20
    high_risk_genes = ["BRCA1", "BRCA2", "TP53", "KRAS", "EGFR", "ALK", "BRAF", "PIK3CA", "PTEN", "RB1"]
    for variant in germline + somatic:
        for gene in high_risk_genes:
            if gene.lower() in variant.lower():
                score += 8
    if tmb > 10:
        score += 10
    elif tmb > 5:
        score += 5
    score += len(comorbidities_list) * 3
    score += len(biomarkers_list) * 2
    return min(score, 100)

def get_risk_tier(score):
    if score < 25:
        return "Low", "success"
    elif score < 50:
        return "Intermediate", "warning"
    elif score < 75:
        return "High", "error"
    else:
        return "Very High", "error"

def get_pharmacogenomic_guidance(medications_list, germline_list):
    guidance = []
    pgx_map = {
        "warfarin": {"gene": "CYP2C9/VKORC1", "action": "Consider genotype-guided dosing; reduced dose if *2/*3 carriers"},
        "clopidogrel": {"gene": "CYP2C19", "action": "Poor metabolizers: consider prasugrel/ticagrelor"},
        "metformin": {"gene": "SLC22A1", "action": "Reduced transporter function may decrease efficacy"},
        "tamoxifen": {"gene": "CYP2D6", "action": "Poor metabolizers: consider aromatase inhibitor"},
        "codeine": {"gene": "CYP2D6", "action": "Ultra-rapid metabolizers: avoid due to toxicity risk"},
        "fluorouracil": {"gene": "DPYD", "action": "DPYD deficiency: reduce dose 50% or use alternative"},
        "irinotecan": {"gene": "UGT1A1", "action": "UGT1A1*28 homozygotes: reduce starting dose"},
        "mercaptopurine": {"gene": "TPMT/NUDT15", "action": "Poor metabolizers: reduce dose significantly"},
    }
    for med in medications_list:
        med_lower = med.lower().strip()
        if med_lower in pgx_map:
            entry = pgx_map[med_lower]
            guidance.append({"medication": med, "gene": entry["gene"], "recommendation": entry["action"]})
    if not guidance:
        guidance.append({"medication": "N/A", "gene": "N/A", "recommendation": "No known pharmacogenomic interactions with current medications"})
    return guidance

def get_treatment_algorithm(disease, somatic_list, biomarkers_list, score):
    treatments = {"first_line": [], "second_line": [], "third_line": []}
    disease_lower = disease.lower()

    if "lung" in disease_lower or "nsclc" in disease_lower:
        for mut in somatic_list:
            if "egfr" in mut.lower():
                treatments["first_line"].append("Osimertinib (EGFR TKI)")
                treatments["second_line"].append("Platinum-based chemotherapy + Pemetrexed")
            if "alk" in mut.lower():
                treatments["first_line"].append("Alectinib (ALK inhibitor)")
                treatments["second_line"].append("Lorlatinib")
            if "kras g12c" in mut.lower():
                treatments["first_line"].append("Sotorasib (KRAS G12C inhibitor)")
        for bio in biomarkers_list:
            if "pd-l1" in bio.lower() and any(x in bio for x in ["80", "90", "100", "70", "60", "50"]):
                treatments["first_line"].append("Pembrolizumab (anti-PD-1)")
        if not treatments["first_line"]:
            treatments["first_line"].append("Platinum doublet chemotherapy + Pembrolizumab")
        treatments["third_line"].append("Docetaxel +/- Ramucirumab")

    elif "breast" in disease_lower:
        for mut in somatic_list:
            if "her2" in mut.lower() or any("her2" in b.lower() and "3+" in b for b in biomarkers_list):
                treatments["first_line"].append("Trastuzumab + Pertuzumab + Docetaxel")
                treatments["second_line"].append("T-DM1 (Ado-trastuzumab emtansine)")
            if "brca" in mut.lower():
                treatments["first_line"].append("Olaparib (PARP inhibitor)")
        if not treatments["first_line"]:
            treatments["first_line"].append("Endocrine therapy (Letrozole + CDK4/6 inhibitor)")
        treatments["third_line"].append("Capecitabine or Eribulin")

    else:
        treatments["first_line"].append("Standard-of-care per NCCN guidelines for " + disease)
        treatments["second_line"].append("Clinical trial enrollment recommended")
        treatments["third_line"].append("Best supportive care / palliative options")

    return treatments

def get_clinical_trials(disease, somatic_list):
    trials = []
    disease_lower = disease.lower()
    if "lung" in disease_lower:
        trials.append({"id": "NCT04685135", "title": "EGFR TKI Combination Study", "phase": "Phase III", "match_reason": "Disease match"})
    if any("kras" in m.lower() for m in somatic_list):
        trials.append({"id": "NCT05132075", "title": "KRAS G12C Inhibitor + Immunotherapy", "phase": "Phase II", "match_reason": "Molecular match (KRAS)"})
    if any("brca" in m.lower() for m in somatic_list):
        trials.append({"id": "NCT03286842", "title": "PARP Inhibitor + Checkpoint Inhibitor", "phase": "Phase I/II", "match_reason": "Molecular match (BRCA)"})
    if not trials:
        trials.append({"id": "N/A", "title": "Search ClinicalTrials.gov for " + disease, "phase": "N/A", "match_reason": "General disease match"})
    return trials

if run_analysis and disease:
    germline_list = parse_lines(germline_variants)
    somatic_list = parse_lines(somatic_mutations)
    biomarkers_list = parse_lines(biomarkers)
    medications_list = parse_lines(medications)
    comorbidities_list = parse_lines(comorbidities)
    family_list = parse_lines(family_history)

    risk_score = compute_risk_score(disease, germline_list, somatic_list, tumor_mutational_burden, biomarkers_list, comorbidities_list)
    risk_tier, tier_color = get_risk_tier(risk_score)

    st.divider()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Precision Medicine Risk Score", f"{risk_score}/100")
    with col2:
        st.metric("Risk Tier", risk_tier)
    with col3:
        st.metric("Variants Identified", len(germline_list) + len(somatic_list))

    st.divider()

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Treatment Algorithm", "Pharmacogenomics", "Clinical Trials", "Risk Summary", "Monitoring Plan"])

    with tab1:
        st.subheader("Personalized Treatment Algorithm")
        treatments = get_treatment_algorithm(disease, somatic_list, biomarkers_list, risk_score)
        for line, meds in treatments.items():
            label = line.replace("_", " ").title()
            st.markdown(f"**{label}:**")
            for med in meds:
                st.markdown(f"- {med}")

    with tab2:
        st.subheader("Pharmacogenomic Guidance")
        pgx = get_pharmacogenomic_guidance(medications_list, germline_list)
        for entry in pgx:
            st.markdown(f"**{entry['medication']}** ({entry['gene']}): {entry['recommendation']}")

    with tab3:
        st.subheader("Clinical Trial Matches")
        trials = get_clinical_trials(disease, somatic_list)
        for trial in trials:
            st.markdown(f"- **{trial['id']}** — {trial['title']} ({trial['phase']}) | *{trial['match_reason']}*")

    with tab4:
        st.subheader("Risk Factor Summary")
        st.markdown(f"**Disease:** {disease}")
        st.markdown(f"**Age:** {age} | **Sex:** {sex}")
        if germline_list:
            st.markdown("**Germline Variants:** " + ", ".join(germline_list))
        if somatic_list:
            st.markdown("**Somatic Mutations:** " + ", ".join(somatic_list))
        if tumor_mutational_burden > 0:
            st.markdown(f"**TMB:** {tumor_mutational_burden} mut/Mb")
        if comorbidities_list:
            st.markdown("**Comorbidities:** " + ", ".join(comorbidities_list))
        if family_list:
            st.markdown("**Family History:** " + ", ".join(family_list))

    with tab5:
        st.subheader("Recommended Monitoring Plan")
        if risk_score >= 75:
            interval = "Every 4-6 weeks"
        elif risk_score >= 50:
            interval = "Every 8-12 weeks"
        else:
            interval = "Every 12-16 weeks"
        st.markdown(f"**Follow-up Interval:** {interval}")
        st.markdown("**Recommended Assessments:**")
        st.markdown("- Imaging (CT/PET) per treatment protocol")
        st.markdown("- Circulating tumor DNA (ctDNA) monitoring")
        st.markdown("- Complete blood count + metabolic panel")
        st.markdown("- Pharmacogenomic re-evaluation if medications change")
        if comorbidities_list:
            st.markdown("- Comorbidity-specific labs: " + ", ".join(comorbidities_list))

elif run_analysis and not disease:
    st.error("Please enter a disease/condition to proceed.")
else:
    st.info("Enter patient data in the sidebar and click **Run Stratification** to begin analysis.")
