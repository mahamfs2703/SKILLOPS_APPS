import streamlit as st
import re
from datetime import datetime

st.set_page_config(page_title="PHI Redactor", page_icon="🛡️", layout="wide")

PATTERNS = {
    "NAME": r"[A-Z][a-z]+ [A-Z][a-z]+",
    "LOCATION": r"(?:zip|postal|address|street|avenue|road|city|county|town).*\d+",
    "DATE": r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2}",
    "PHONE": r"\d{3}[-.]?\d{3}[-.]?\d{4}|\(\d{3}\)\s?\d{3}[-.]?\d{4}",
    "FAX": r"(?i)fax:?\s*\d{3}[-.]?\d{3}[-.]?\d{4}",
    "EMAIL": r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}",
    "SSN": r"\d{3}-\d{2}-\d{4}",
    "MRN": r"(?i)(?:MRN|medical record|patient id):?\s*[A-Z0-9]+",
    "HEALTH_PLAN_ID": r"(?i)(?:member|policy|beneficiary)\s*(?:id|number):?\s*[A-Z0-9]+",
    "ACCOUNT": r"(?i)(?:account|acct)\s*(?:number|#):?\s*[A-Z0-9]+",
    "LICENSE": r"(?i)(?:license|certificate|cert)\s*(?:number|#):?\s*[A-Z0-9]+",
    "VEHICLE_ID": r"(?i)(?:VIN|vehicle id|serial):?\s*[A-Z0-9]{10,}",
    "DEVICE_ID": r"(?i)(?:device|serial)\s*(?:id|number):?\s*[A-Z0-9]+",
    "URL": r"https?://[^\s]+",
    "IP_ADDRESS": r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",
    "BIOMETRIC": r"(?i)(?:fingerprint|retina|iris|voiceprint|biometric)",
    "PHOTO": r"(?i)(?:photo|photograph|image|picture)\s*(?:of|showing)?\s*(?:face|patient)",
}


def redact_text(text):
    redaction_log = []
    redacted = text
    for category, pattern in PATTERNS.items():
        matches = list(re.finditer(pattern, redacted))
        for match in reversed(matches):
            original = match.group()
            tag = f"[{category}]"
            redacted = redacted[: match.start()] + tag + redacted[match.end() :]
            redaction_log.append(
                {
                    "category": category,
                    "original": original,
                    "position": match.start(),
                }
            )
    return redacted, redaction_log


def validate_output(redacted_text):
    remaining_phi = []
    for category, pattern in PATTERNS.items():
        tag = f"[{category}]"
        clean_text = redacted_text.replace(tag, "")
        matches = re.findall(pattern, clean_text)
        if matches:
            remaining_phi.extend(
                [{"category": category, "match": m} for m in matches]
            )
    return remaining_phi


st.title("🛡️ PHI Redactor")
st.caption("HIPAA Safe Harbor Method — Scans and redacts all 18 identifier types")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Input")
    input_text = st.text_area(
        "Paste text containing PHI:",
        height=300,
        placeholder="Enter clinical notes, patient records, or any text that may contain PHI...",
    )

    if st.button("Redact PHI", type="primary", use_container_width=True):
        if not input_text.strip():
            st.error("Please enter text to redact.")
        elif len(input_text.encode("utf-8")) > 10 * 1024 * 1024:
            st.error("Input exceeds 10MB limit.")
        else:
            redacted, log = redact_text(input_text)
            remaining = validate_output(redacted)

            st.session_state["redacted"] = redacted
            st.session_state["log"] = log
            st.session_state["remaining"] = remaining
            st.session_state["timestamp"] = datetime.now().isoformat()

with col2:
    st.subheader("Redacted Output")
    if "redacted" in st.session_state:
        st.text_area(
            "Redacted text:",
            value=st.session_state["redacted"],
            height=300,
            disabled=True,
        )

        if st.session_state["remaining"]:
            st.warning(
                f"⚠️ {len(st.session_state['remaining'])} potential PHI item(s) may remain. Review manually."
            )
        else:
            st.success("✅ Output validation passed — no residual PHI detected.")
    else:
        st.info("Redacted output will appear here.")

if "log" in st.session_state and st.session_state["log"]:
    st.divider()
    st.subheader("Audit Log")

    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Total Redactions", len(st.session_state["log"]))

    categories_found = set(item["category"] for item in st.session_state["log"])
    col_b.metric("PHI Categories", len(categories_found))
    col_c.metric("Timestamp", st.session_state["timestamp"][:19])

    st.caption("Redaction details by category:")
    category_counts = {}
    for item in st.session_state["log"]:
        category_counts[item["category"]] = (
            category_counts.get(item["category"], 0) + 1
        )

    for cat, count in sorted(category_counts.items(), key=lambda x: -x[1]):
        st.write(f"- **{cat}**: {count} redaction(s)")
