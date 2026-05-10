---
name: demand-forecaster
description: Forecast demand for inventory planning
---
# Demand Forecaster
## Instructions
1. Get 12 months history with date range filtering using indexed date columns
2. Apply data masking to customer identifiers, email addresses, phone numbers, and other PII fields
3. Implement data sampling (max 100K records) or daily/weekly aggregation to control processing costs
4. Perform seasonality decomposition on masked and filtered data
5. Generate forecast with validation against historical patterns

## Constraints
- Min 12 months for reliable forecast
- Query optimization: Use date range filters with proper indexing on date columns
- Data masking: Hash or anonymize customer_id, email, phone, address fields
- Cost control: Limit to 100K records via sampling or use aggregated daily/weekly data
- Output format: JSON with fields {period, forecasted_demand, confidence_interval, seasonality_factor}
- Validation: Forecast values must be non-negative, confidence intervals between 0-1

## Error Handling
- If <12 months available: Return error "Insufficient historical data - minimum 12 months required"
- If no data found: Return error "No historical data available for specified parameters"
- If data quality issues: Return warning with data completeness percentage