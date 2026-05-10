---
name: phi-redactor
description: Redact PHI using HIPAA Safe Harbor
---
# PHI Redactor

## Instructions
1. Scan for 18 HIPAA identifiers using explicit patterns
2. Redact with category tags
3. Validate input and sanitize content
4. Log all redaction activities for audit compliance
5. Validate output to ensure no PHI leakage

## HIPAA Safe Harbor Identifiers

### 1. Names
- Pattern: `[A-Z][a-z]+ [A-Z][a-z]+`
- Redact as: `[NAME]`

### 2. Geographic subdivisions smaller than state
- Pattern: `(zip|postal|address|street|avenue|road|city|county|town).*d+`
- Redact as: `[LOCATION]`

### 3. Dates (except year)
- Pattern: `d{1,2}[/-]d{1,2}[/-]d{2,4}|(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* d{1,2}`
- Redact as: `[DATE]`

### 4. Telephone numbers
- Pattern: `d{3}[-.]?d{3}[-.]?d{4}|(d{3})s?d{3}[-.]?d{4}`
- Redact as: `[PHONE]`

### 5. Fax numbers
- Pattern: `fax:?s*d{3}[-.]?d{3}[-.]?d{4}`
- Redact as: `[FAX]`

### 6. Email addresses
- Pattern: `[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+.[A-Z|a-z]{2,}`
- Redact as: `[EMAIL]`

### 7. Social Security Numbers
- Pattern: `d{3}-?d{2}-?d{4}`
- Redact as: `[SSN]`

### 8. Medical record numbers
- Pattern: `(MRN|medical record|patient id):?s*[A-Z0-9]+`
- Redact as: `[MRN]`

### 9. Health plan beneficiary numbers
- Pattern: `(member|policy|beneficiary)s*(id|number):?s*[A-Z0-9]+`
- Redact as: `[HEALTH_PLAN_ID]`

### 10. Account numbers
- Pattern: `(account|acct)s*(number|#):?s*[A-Z0-9]+`
- Redact as: `[ACCOUNT]`

### 11. Certificate/license numbers
- Pattern: `(license|certificate|cert)s*(number|#):?s*[A-Z0-9]+`
- Redact as: `[LICENSE]`

### 12. Vehicle identifiers and serial numbers
- Pattern: `(VIN|vehicle id|serial):?s*[A-Z0-9]{10,}`
- Redact as: `[VEHICLE_ID]`

### 13. Device identifiers and serial numbers
- Pattern: `(device|serial)s*(id|number):?s*[A-Z0-9]+`
- Redact as: `[DEVICE_ID]`

### 14. Web URLs
- Pattern: `https?://[^s]+`
- Redact as: `[URL]`

### 15. Internet Protocol addresses
- Pattern: `d{1,3}.d{1,3}.d{1,3}.d{1,3}`
- Redact as: `[IP_ADDRESS]`

### 16. Biometric identifiers
- Pattern: `(fingerprint|retina|iris|voiceprint|biometric)`
- Redact as: `[BIOMETRIC]`

### 17. Full face photographs
- Pattern: `(photo|photograph|image|picture)s*(of|showing)?s*(face|patient)`
- Redact as: `[PHOTO]`

### 18. Other unique identifying numbers
- Pattern: `[A-Z0-9]{8,}` (context-dependent)
- Redact as: `[IDENTIFIER]`

## Input Validation
- Check file size limits (max 10MB per document)
- Validate file formats (txt, pdf, docx, html)
- Sanitize special characters that could cause parsing errors
- Reject files with suspicious extensions or embedded scripts

## Audit Logging
- Log timestamp, user ID, document hash, and redaction count
- Record specific PHI categories found and redacted
- Track processing time and token usage
- Generate compliance reports with redaction statistics
- Store logs in HIPAA-compliant encrypted storage

## Error Handling
- If pattern matching fails: Apply conservative blanket redaction
- If document too large: Process in chunks with overlap validation
- If unsupported format: Convert to plain text or reject with clear message
- If system error: Fail secure - do not output potentially unredacted content
- Implement retry logic with exponential backoff for transient failures

## Token Optimization
- Process documents in 4KB chunks to stay within token limits
- Use sliding window approach for context preservation
- Implement caching for repeated pattern matches
- Batch similar documents for efficiency
- Pre-filter obvious non-PHI content to reduce processing load

## Output Validation
- Scan redacted output against all 18 identifier patterns
- Verify no original PHI remains in final output
- Check that redaction tags are properly formatted
- Validate document structure integrity after redaction
- Generate confidence score for redaction completeness

## Constraints
- NEVER output PHI in logs or error messages
- Err on side of caution - over-redact rather than under-redact
- Requires HIPAA_COMPLIANT_ROLE for execution
- All processing must occur in secure, encrypted environment
- Implement automatic data purging after processing completion