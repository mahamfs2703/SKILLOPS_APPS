---
name: contract-performance-monitoring
description: Analyze value-based contract performance using correct population segmentation and methodology agreed upon by leadership. Use this skill whenever analyzing VBC performance, calculating shared savings, reviewing quality metric performance against contracts, or building contract performance dashboards. Always use this skill when the request involves "value-based", "VBC", "shared savings", "attributed population", "contract performance", "ACO", or "risk contract". Methodology decisions made by leadership must be applied consistently.
---

# Contract Performance Monitoring

## Purpose
Monitor and analyze performance against value-based care contracts using standardized methodology, correct population segmentation, and leadership-approved definitions.

## Core Principle
**Attributed vs non-attributed populations must always be separated.** Mixing these populations produces misleading performance numbers and invalid contract calculations. This was a formal decision made by Finance and Clinical leadership in 2023 — it must be applied consistently across all analyses.

---

## Data Security and Access Controls

### PHI Protection Requirements
- **Always mask patient identifiers** in contract performance reports — use encrypted patient keys or aggregate data only
- **Never include** patient names, DOB, SSN, or addresses in performance dashboards
- Attribution lists must be stored in HIPAA-compliant secure databases with encryption at rest and in transit
- Apply minimum necessary standard — only include patient-level data when required for specific calculations

### Role-Based Access Controls
- **Contract Analysts**: Read access to aggregate performance data only
- **Finance Leadership**: Full access to cost and savings calculations
- **Clinical Leadership**: Access to quality metrics and patient attribution lists
- **Executive Team**: Dashboard access with summary metrics only
- All access must be logged and reviewed quarterly

### Audit Logging Requirements
- Log all queries accessing patient attribution data with user ID, timestamp, and purpose
- Track all contract performance report generation and distribution
- Maintain audit trail for benchmark calculations and methodology changes
- Quarterly access reviews required for all users with contract data permissions

---

## Query Optimization and Performance Guidelines

### Large Population Analysis Standards
- **Limit initial queries** to 50,000 attributed patients maximum per execution
- Use indexed fields for attribution lookups (patient ID, contract ID, measurement period)
- Implement pagination for reports covering multiple contracts or extended time periods
- Cache frequently accessed benchmark data to reduce database load

### Result Set Limits
- **Dashboard queries**: Maximum 10,000 rows per visualization
- **Detailed reports**: Maximum 100,000 patient records per export
- **Trend analysis**: Limit to 24 months of historical data unless specifically requested
- Implement automatic query timeout at 5 minutes for performance monitoring

### Data Retention and Secure Handling

#### Retention Policies
- **Contract performance reports**: Retain for 7 years per regulatory requirements
- **Patient attribution lists**: Retain for contract term plus 3 years
- **Benchmark calculations**: Retain supporting data for 5 years
- **Audit logs**: Retain for 6 years minimum

#### Secure Handling Procedures
- All contract performance files must be encrypted and access-controlled
- Use secure file transfer protocols (SFTP) for payer report transmission
- Implement automatic deletion of temporary analysis files after 30 days
- Require two-factor authentication for access to contract performance systems

---

## Population Segmentation Rules — Non-Negotiable

### Attributed Population
- Patients formally attributed to your organization under the contract terms
- Attribution methodology varies by contract — always check the specific contract's attribution logic:
  - **Plurality of visits**: Patient attributed to provider with most primary care visits in measurement period
  - **Voluntary attribution**: Patient self-selected your organization as their PCP
  - **Geographic attribution**: Patient attributed based on geography (rare — Medicaid ACOs)
- **Never include non-attributed patients in attributed performance calculations**

### Non-Attributed Population
- Patients your organization serves but who are NOT formally attributed
- Track separately — performance on this population affects future attribution and growth
- Do not include in shared savings calculations

### Prospective vs Retrospective Attribution
- Some contracts use prospective attribution (fixed list at start of year)
- Others use retrospective (determined at year-end based on actual utilization)
- **Always confirm which method applies before running any performance report**

---

## Key Performance Metrics by Contract Type

### Medicare Shared Savings Program (MSSP / ACO)
- Benchmark: CMS-calculated expenditure benchmark
- Quality gate: Must meet minimum quality performance to share in savings
- Key metrics: Total cost of care PMPM, ACO-11 through ACO-54 quality measures
- Always use **aligned beneficiary** list from CMS — do not use internal attribution

### Medicare Advantage Value-Based Contracts
- Shared savings / risk corridor thresholds vary by contract — load from contract terms
- Quality metrics typically mirror Star Rating measures
- Separate medical loss ratio (MLR) from administrative costs before calculating savings

### Medicaid Managed Care VBC
- Outcome-based incentives: Often tied to specific conditions (diabetes, hypertension, maternity)
- Report by HEDIS measurement year — not plan year unless contract specifies otherwise

### Commercial ACO / Shared Savings
- Benchmark typically set at contract inception — verify baseline year
- Trend adjustment may apply — check contract for inflation/trend factor

---

## Reporting Methodology Standards

### Cost Calculations
- Use **allowed amount** as the basis for cost comparisons — not paid amount or billed charges
- Separate professional fees from facility fees unless contract bundles them
- Exclude outlier cases only if contract explicitly defines outlier methodology

### Quality Score Calculations
- Use **administrative data** for rate calculations unless contract specifies hybrid or medical record review
- Apply HEDIS technical specifications for measure-specific exclusions
- Do not count pending or in-process services as completed for rate calculations

### Benchmark Comparisons
- Always compare to the contract-specific benchmark — not national averages
- Risk-adjust cost comparisons where contract requires (HCC risk scores)
- Document risk adjustment methodology used in every report

---

## Dashboard Requirements

Every contract performance report must include:
1. **Contract name and measurement period**
2. **Attributed population count** (separate from total panel)
3. **Performance vs benchmark** for cost and quality
4. **Shared savings / shared risk position** (estimated)
5. **Quality gate status** — are minimum quality thresholds met?
6. **Trend vs prior period** — are we improving or deteriorating?

---

## Output Format
For each contract performance analysis:
1. **Contract** name, payer, measurement period
2. **Population**: Attributed count, non-attributed count (separate)
3. **Cost performance**: PMPM vs benchmark, variance, trend
4. **Quality performance**: Score vs threshold for each measure
5. **Savings/risk position**: Estimated shared savings or risk exposure

---

## Governance Notes
- Attributed vs non-attributed separation is a formal leadership decision (Finance + Clinical, Q3 2023) — do not deviate
- Allowed amount basis for cost calculations was agreed upon with all major payers in 2022 contract negotiations
- Contract performance reports require sign-off from CFO and VP of Population Health before sharing with payers