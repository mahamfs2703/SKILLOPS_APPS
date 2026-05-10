import streamlit as st

st.set_page_config(page_title="Brand Color CSS Generator", page_icon="🎨", layout="wide")

BRAND_COLORS = {
    "Primary Blue": "#4FA4DC",
    "Yellow": "#F0D457",
    "Green": "#7BC043",
    "Orange": "#F79A2E",
    "Black": "#000000",
    "White": "#FFFFFF",
}

COLOR_USAGE = {
    "Primary Blue": "primary UI, buttons, highlights",
    "Yellow": "accents, highlights, positive alerts",
    "Green": "success states, confirmations",
    "Orange": "secondary accents, callouts",
    "Black": "backgrounds",
    "White": "text",
}

st.title("Brand Color CSS Generator")
st.markdown("Generate consistent CSS using your approved brand palette.")

st.subheader("Brand Palette")
cols = st.columns(len(BRAND_COLORS))
for i, (name, hex_val) in enumerate(BRAND_COLORS.items()):
    with cols[i]:
        border = "1px solid #ccc" if hex_val in ("#FFFFFF",) else "none"
        st.markdown(
            f'<div style="background-color:{hex_val};width:100%;height:80px;border-radius:8px;border:{border};"></div>',
            unsafe_allow_html=True,
        )
        st.caption(f"**{name}**\n\n`{hex_val}`\n\n{COLOR_USAGE[name]}")

st.divider()

st.subheader("Generate CSS")

output_options = st.multiselect(
    "What CSS do you need?",
    ["CSS Custom Properties", "Utility Classes", "Button Styles", "Alert/Status Styles", "Card Styles"],
    default=["CSS Custom Properties"],
)

css_parts = []

if "CSS Custom Properties" in output_options:
    css_parts.append(""":root {
  --color-primary: #4FA4DC;
  --color-accent-yellow: #F0D457;
  --color-success: #7BC043;
  --color-accent-orange: #F79A2E;
  --color-dark: #000000;
  --color-light: #FFFFFF;
}""")

if "Utility Classes" in output_options:
    css_parts.append(""".text-primary { color: var(--color-primary); }
.text-success { color: var(--color-success); }
.text-warning { color: var(--color-accent-yellow); }
.text-accent { color: var(--color-accent-orange); }
.text-dark { color: var(--color-dark); }
.text-light { color: var(--color-light); }

.bg-primary { background-color: var(--color-primary); }
.bg-success { background-color: var(--color-success); }
.bg-warning { background-color: var(--color-accent-yellow); }
.bg-accent { background-color: var(--color-accent-orange); }
.bg-dark { background-color: var(--color-dark); }
.bg-light { background-color: var(--color-light); }""")

if "Button Styles" in output_options:
    css_parts.append(""".btn-primary {
  background-color: var(--color-primary);
  color: var(--color-light);
  border: none;
  padding: 0.625rem 1.25rem;
  border-radius: 4px;
  cursor: pointer;
  transition: opacity 0.2s ease;
}
.btn-primary:hover { opacity: 0.85; }

.btn-success {
  background-color: var(--color-success);
  color: var(--color-dark);
  border: none;
  padding: 0.625rem 1.25rem;
  border-radius: 4px;
  cursor: pointer;
  transition: opacity 0.2s ease;
}
.btn-success:hover { opacity: 0.85; }

.btn-warning {
  background-color: var(--color-accent-orange);
  color: var(--color-dark);
  border: none;
  padding: 0.625rem 1.25rem;
  border-radius: 4px;
  cursor: pointer;
  transition: opacity 0.2s ease;
}
.btn-warning:hover { opacity: 0.85; }""")

if "Alert/Status Styles" in output_options:
    css_parts.append(""".alert-success {
  background-color: var(--color-success);
  color: var(--color-dark);
  padding: 1rem;
  border-radius: 4px;
}

.alert-warning {
  background-color: var(--color-accent-yellow);
  color: var(--color-dark);
  padding: 1rem;
  border-radius: 4px;
}

.alert-info {
  background-color: var(--color-primary);
  color: var(--color-light);
  padding: 1rem;
  border-radius: 4px;
}""")

if "Card Styles" in output_options:
    css_parts.append(""".card {
  background-color: var(--color-light);
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.card-dark {
  background-color: var(--color-dark);
  color: var(--color-light);
  border-radius: 8px;
  padding: 1.5rem;
}

.card-highlight {
  background-color: var(--color-dark);
  border-left: 4px solid var(--color-primary);
  color: var(--color-light);
  border-radius: 8px;
  padding: 1.5rem;
}""")

generated_css = "\n\n".join(css_parts)

if generated_css:
    st.code(generated_css, language="css")
else:
    st.info("Select at least one option above to generate CSS.")

st.divider()
st.subheader("Accessibility Notes")
st.markdown("""
| Combination | Contrast Ratio | WCAG AA |
|---|---|---|
| White text on Primary Blue (#4FA4DC) | ~3.2:1 | ⚠️ Large text only |
| White text on Black (#000000) | 21:1 | ✅ Pass |
| Black text on Yellow (#F0D457) | ~14.5:1 | ✅ Pass |
| Black text on Green (#7BC043) | ~8.5:1 | ✅ Pass |
| Black text on Orange (#F79A2E) | ~5.8:1 | ✅ Pass |
""")
