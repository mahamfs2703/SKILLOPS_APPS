---
name: quality-anomaly
description: Detect quality anomalies in sensor data
---
# Quality Anomaly Detector

## Input Validation and Data Sanitization
- Validate sensor data format (numeric values, timestamps)
- Check for null, infinite, or out-of-range values
- Sanitize input parameters to prevent injection attacks
- Verify data completeness (minimum 30 data points required)
- Validate timestamp sequences for chronological order

## Query Optimization and Limits
- Limit result sets to maximum 10,000 data points per query
- Use indexed timestamp ranges for efficient data retrieval
- Implement sliding window analysis (maximum 1000 points per window)
- Cache statistical calculations for repeated queries
- Batch process large datasets in 500-point chunks

## Instructions
1. Analyze against control limits
   - Calculate upper and lower control limits (UCL/LCL)
   - Identify points beyond 3-sigma limits
   - Flag sustained shifts in process mean

2. Apply Western Electric rules
   - Rule 1: Any point beyond 3-sigma control limits
   - Rule 2: Two of three consecutive points beyond 2-sigma on same side
   - Rule 3: Four of five consecutive points beyond 1-sigma on same side
   - Rule 4: Eight consecutive points on same side of center line
   - Rule 5: Six consecutive points steadily increasing or decreasing
   - Rule 6: Fifteen consecutive points within 1-sigma of center line
   - Rule 7: Fourteen consecutive points alternating up and down
   - Rule 8: Eight consecutive points beyond 1-sigma on both sides

## Error Handling and Fallback Procedures
- Return structured error messages with specific failure codes
- Implement graceful degradation when insufficient data available
- Fallback to basic statistical analysis if Western Electric rules fail
- Log anomalies with severity levels (LOW, MEDIUM, HIGH, CRITICAL)
- Provide alternative analysis methods when primary detection fails

## Resource Management
- Token usage budget: maximum 2000 tokens per analysis
- Query complexity threshold: O(n log n) maximum computational complexity
- Memory limit: 50MB per analysis session
- Timeout limit: 30 seconds per query execution

## Constraints
- Do not expose process parameters
- 80% confidence threshold
- Maximum processing time: 30 seconds per dataset
- Minimum data quality score: 85% for reliable analysis