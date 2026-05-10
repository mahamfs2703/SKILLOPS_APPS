---
name: tooluniverse-precision-medicine-stratification
description: Comprehensive patient stratification for precision medicine by integrating genomic, clinical, and therapeutic data. Given a disease/condition, genomic data (germline variants, somatic mutations, expression), and optional clinical parameters, performs multi-phase analysis across 9 phases covering disease disambiguation, genetic risk assessment, disease-specific molecular stratification, pharmacogenomic profiling, comorbidity/DDI risk, pathway analysis, clinical evidence and guideline mapping, clinical trial matching, and integrated outcome prediction. Generates a quantitative Precision Medicine Risk Score (0-100) with risk tier assignment (Low/Intermediate/High/Very High), treatment algorithm (1st/2nd/3rd line), pharmacogenomic guidance, clinical trial matches, and monitoring plan. Use when clinicians ask about patient risk stratification, treatment selection, prognosis prediction, or personalized therapeutic strategy across cancer, metabolic, cardiovascular, neurological, or rare diseases.
---

# Precision Medicine Patient Stratification

Transform patient genomic and clinical profiles into actionable risk stratification, treatment recommendations, and personalized therapeutic strategies. Integrates germline genetics, somatic alterations, pharmacogenomics, pathway biology, and clinical evidence to produce a quantitative risk score with tiered management recommendations.

**KEY PRINCIPLES**:
1. **PHI protection** - Mask and de-identify all patient data before processing
2. **Report-first approach** - Create report file FIRST, then populate progressively
3. **Disease-specific logic** - Cancer vs metabolic vs rare disease pipelines diverge at Phase 2
4. **Multi-level integration** - Germline + somatic + expression + clinical data layers
5. **Evidence-graded** - Every finding has an evidence tier (T1-T4)
6. **Quantitative output** - Precision Medicine Risk Score (0-100) with transparent components
7. **Pharmacogenomic guidance** - Drug selection AND dosing recommendations
8. **Guideline-concordant** - Reference NCCN, ACC/AHA, ADA, and other guidelines
9. **Source-referenced** - Every statement cites the tool/database source
10. **Completeness checklist** - Mandatory section showing data availability and analysis coverage
11. **English-first queries** - Always use English terms in tool calls. Respond in user's language

---

## PHI Protection Protocol

**BEFORE any analysis**, implement PHI masking:

### Step 0.1: Identify and Mask PHI
```python
# Mask direct identifiers
patient_data = mask_phi(raw_input)
# Replace: names -> [PATIENT], dates -> [DATE], MRN -> [ID]
# Keep: age ranges (e.g., "45-50"), disease info, genetic data
```

### Step 0.2: Generate De-identified Patient ID
```python
# Create anonymous identifier for report
patient_id = f"PM_{hash(timestamp)[:8]}"  # e.g., "PM_A7B3C9D2"
```

### Step 0.3: PHI-Safe Data Structure
```python
safe_profile = {
    'patient_id': patient_id,
    'age_range': extract_age_range(age),  # "40-50" instead of "47"
    'disease': disease_name,
    'genomic_data': genomic_variants,  # No patient identifiers
    'clinical_params': clinical_values,  # No dates/names
    'family_history': 'positive/negative',  # No relative names
}
```

### PHI Elements to Mask

| PHI Type | Examples | Replacement |
|----------|----------|-------------|
| Names | "John Smith", "Dr. Johnson" | [PATIENT], [PHYSICIAN] |
| Dates | "2023-05-15", "March 2022" | [DATE], [TIMEPOINT] |
| Identifiers | MRN, SSN, phone | [ID], [IDENTIFIER] |
| Locations | "Boston", "Mass General" | [CITY], [HOSPITAL] |
| Ages >89 | "92 years old" | ">89 years" |
| Rare combinations | Very specific phenotypes | Generalized terms |

---

## When to Use

Apply when user asks:
- "Stratify this breast cancer patient: ER+/HER2-, BRCA1 mutation, stage II"
- "What is the risk profile for this diabetes patient with HbA1c 8.5 and CYP2C19 poor metabolizer?"
- "NSCLC patient with EGFR L858R, stage IV, TMB 25 - treatment strategy?"
- "Predict prognosis and recommend treatment for this cardiovascular patient"
- "Patient has Marfan syndrome with FBN1 mutation - risk stratification"
- "Alzheimer's risk assessment: APOE e4/e4, family history positive"
- "Personalized treatment plan for type 2 diabetes with genetic risk factors"
- "Which therapy is best for this patient's molecular profile?"

**NOT for** (use other skills instead):
- Single variant interpretation -> Use `tooluniverse-variant-interpretation` or `tooluniverse-cancer-variant-interpretation`
- Immunotherapy-specific prediction -> Use `tooluniverse-immunotherapy-response-prediction`
- Drug safety profiling only -> Use `tooluniverse-adverse-event-detection`
- Target validation -> Use `tooluniverse-drug-target-validation`
- Clinical trial search only -> Use `tooluniverse-clinical-trial-matching`
- Drug-drug interaction analysis only -> Use `tooluniverse-drug-drug-interaction`
- PRS calculation only -> Use `tooluniverse-polygenic-risk-score`

---

## Input Parsing

### Required Input
- **Disease/condition**: Free-text disease name (e.g., "breast cancer", "type 2 diabetes", "Marfan syndrome")
- **At least one of**: Germline variants, somatic mutations, gene list, or clinical biomarkers

### Strongly Recommended
- **Genomic data**: Specific variants (e.g., "BRCA1 c.68_69delAG", "EGFR L858R"), gene names, or expression changes
- **Clinical parameters**: Age, sex, disease stage, biomarkers (HbA1c, PSA, LDL-C)

### Optional (improves stratification)
- **Comorbidities**: Other conditions (e.g., "hypertension", "diabetes")
- **Prior treatments**: Previous therapies and responses
- **Family history**: Affected relatives, inheritance pattern
- **Ethnicity**: For population-specific risk calibration
- **Current medications**: For DDI and pharmacogenomic analysis
- **Stratification goal**: Risk assessment, treatment selection, prognosis, prevention

### Input Format Examples

| Format | Example | How to Parse |
|--------|---------|-------------|
| Cancer + mutations + stage | "Breast cancer, BRCA1 mut, ER+, HER2-, stage II" | disease=breast_cancer, mutations=[BRCA1], biomarkers={ER:+, HER2:-}, stage=II |
| Metabolic + biomarkers + PGx | "T2D, HbA1c 8.5, CYP2C19 *2/*2" | disease=T2D, biomarkers={HbA1c:8.5}, pgx={CYP2C19:poor_metabolizer} |
| CVD risk profile | "High LDL 190, SLCO1B1*5, family hx MI" | disease=CVD, biomarkers={LDL:190}, pgx={SLCO1B1:*5}, family_hx=positive |
| Rare disease + variant | "Marfan, FBN1 c.4082G>A" | disease=Marfan, mutations=[FBN1 c.4082G>A], disease_type=rare |
| Neuro risk | "Alzheimer risk, APOE e4/e4, age 55" | disease=AD, genotype={APOE:e4/e4}, clinical={age:55} |
| Cancer + comprehensive | "NSCLC, EGFR L858R, TMB 25, PD-L1 80%, stage IV" | disease=NSCLC, mutations=[EGFR L858R], biomarkers={TMB:25, PDL1:80}, stage=IV |

### Disease Type Classification

Classify the disease into one of these categories (determines Phase 2 routing):

| Category | Examples | Key Stratification Axes |
|----------|----------|------------------------|
| **CANCER** | Breast, lung, colorectal, melanoma, prostate | Stage, molecular subtype, TMB, driver mutations, hormone receptors |
| **METABOLIC** | Type 2 diabetes, obesity, metabolic syndrome, NAFLD | HbA1c, BMI, genetic risk, comorbidities, CYP genotypes |
| **CARDIOVASCULAR** | CAD, heart failure, atrial fibrillation, hypertension | ASCVD risk, LDL, genetic risk, statin PGx, anticoagulant PGx |
| **NEUROLOGICAL** | Alzheimer, Parkinson, epilepsy, multiple sclerosis | APOE status, genetic risk, age of onset, PGx for anticonvulsants |
| **RARE/MONOGENIC** | Marfan, CF, sickle cell, Huntington, PKU | Causal variant, penetrance, genotype-phenotype correlation |
| **AUTOIMMUNE** | RA, lupus, MS, Crohn's, ulcerative colitis | HLA associations, genetic risk, biologics PGx |

### Gene Symbol Normalization

| Common Alias | Official Symbol | Notes |
|-------------|----------------|-------|
| HER2 | ERBB2 | Breast cancer biomarker |
| PD-L1 | CD274 | Immunotherapy biomarker |
| EGFR | EGFR | Lung cancer driver |
| BRCA1/2 | BRCA1, BRCA2 | Hereditary cancer |
| CYP2D6 | CYP2D6 | Drug metabolism |
| CYP2C19 | CYP2C19 | Clopidogrel, PPIs |
| CYP3A4 | CYP3A4 | Major drug metabolism |
| VKORC1 | VKORC1 | Warfarin dosing |
| SLCO1B1 | SLCO1B1 | Statin myopathy |
| DPYD | DPYD | Fluoropyrimidine toxicity |
| UGT1A1 | UGT1A1 | Irinotecan toxicity |
| TPMT | TPMT | Thiopurine toxicity |

---

## Phase 0: Tool Parameter Reference (CRITICAL)

**BEFORE calling ANY tool**, verify parameters using this reference table.

### Verified Tool Parameters

| Tool | Parameters | Response Structure | Notes |
|------|-----------|-------------------|-------|
| `OpenTargets_get_disease_id_description_by_name` | `diseaseName` | `{data: {search: {hits: [{id, name, description}]}}}` | Disease to EFO ID |
| `OpenTargets_get_drug_id_description_by_name` | `drugName` | `{data: {search: {hits: [{id, name, description}]}}}` | Drug to ChEMBL ID |
| `OpenTargets_get_associated_drugs_by_disease_efoId` | `efoId`, `size` | `{data: {disease: {knownDrugs: {count, rows}}}}` | Drugs for disease |
| `OpenTargets_get_associated_targets_by_disease_efoId` | `efoId`, `size` | `{data: {disease: {associatedTargets: {count, rows}}}}` | Genetic associations |
| `OpenTargets_get_drug_mechanisms_of_action_by_chemblId` | `chemblId` | `{data: {drug: {mechanismsOfAction: {rows}}}}` | Drug MOA |
| `OpenTargets_get_approved_indications_by_drug_chemblId` | `chemblId` | Approved indications list | Check drug approvals |
| `OpenTargets_get_drug_adverse_events_by_chemblId` | `chemblId` | `{data: {drug: {adverseEvents: {count, rows}}}}` | Drug safety |
| `OpenTargets_get_associated_drugs_by_target_ensemblID` | `ensemblId`, `size` | Drug-target associations | Drugs targeting gene |
| `OpenTargets_get_target_safety_profile_by_ensemblID` | `ensemblId` | Safety profile data | Target safety |
| `OpenTargets_get_target_tractability_by_ensemblID` | `ensemblId` | Tractability assessment | Druggability |
| `OpenTargets_get_diseases_phenotypes_by_target_ensembl` | `ensemblId` | Disease-phenotype associations | Gene-disease links |
| `OpenTargets_target_disease_evidence` | `ensemblId`, `efoId`, `size` | Evidence for target-disease pair | Specific gene-disease evidence |
| `OpenTargets_search_gwas_studies_by_disease` | `diseaseIds` (array), `size` | `{data: {studies: {count, rows}}}` | GWAS studies |
| `OpenTargets_drug_pharmacogenomics_data` | `chemblId` | Pharmacogenomic data | Drug PGx |
| `MyGene_query_genes` | `query` (NOT `q`) | `{hits: [{_id, symbol, name, ensembl: {gene}}]}` | Gene resolution |
| `ensembl_lookup_gene` | `gene_id`, `species='homo_sapiens'` | `{data: {id, display_name, description, biotype}}` | REQUIRES species |
| `EnsemblVEP_annotate_rsid` | `variant_id` (NOT `rsid`) | VEP annotation with SIFT/PolyPhen | Variant impact |
| `EnsemblVEP_annotate_hgvs` | `hgvs_notation`, `species` | VEP annotation | HGVS variant annotation |
| `ensembl_get_variation` | `variant_id`, `species` | Variant details | rsID lookup |
| `clinvar_search_variants` | `gene`, `significance`, `limit` | Variant list | Search ClinVar |
| `clinvar_get_variant_details` | `variant_id` | Variant details with clinical significance | ClinVar details |
| `clinvar_get_clinical_significance` | `variant_id` | Clinical significance only | Quick pathogenicity |
| `civic_search_evidence_items` | `therapy_name`, `disease_name` | `{data: {evidenceItems: {nodes}}}` | Clinical evidence |
| `civic_search_variants` | `name`, `gene_name` | `{data: {variants: {nodes}}}` | Variant clinical significance |
| `civic_search_assertions` | `therapy_name`, `disease_name` | `{data: {assertions: {nodes}}}` | Clinical assertions |
| `cBioPortal_get_mutations` | `study_id`, `gene_list` (STRING, not array) | `{status, data: [{...}]}` | Somatic mutation data |
| `gwas_get_associations_for_trait` | `trait` | GWAS associations | Trait-SNP associations |
| `gwas_search_associations` | `query` | GWAS associations | Broad GWAS search |
| `gwas_get_snps_for_gene` | `gene` | SNPs associated with gene | Gene GWAS hits |
| `GWAS_search_associations_by_gene` | `gene_name` | Gene GWAS associations | Gene-trait links |
| `PharmGKB_get_clinical_annotations` | `query` | Clinical annotations | Drug-gene-phenotype |
| `PharmGKB_get_dosing_guidelines` | `query` | Dosing guidelines | PGx dosing |
| `PharmGKB_search_variants` | `query` | Variant PGx data | PGx variant search |
| `PharmGKB_get_gene_details` | `query` | Gene PGx details | PGx gene info |
| `PharmGKB_get_drug_details` | `query` | Drug PGx details | Drug