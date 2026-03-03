import streamlit as st
import json
import pathlib
import pandas as pd
from app.orchestrator import analyze_contacts

DB_PATH = pathlib.Path("contacts_db.json")

st.set_page_config(page_title="AI Networking Copilot", layout="wide")
st.title("AI Networking Copilot")

if "results" not in st.session_state:
    st.session_state["results"] = []

tone = st.selectbox("Tone", ["warm", "direct"])

raw_text = st.text_area(
    "Contacts (one per line: name | role_company | context | linkedin_url)",
    height=200,
)

if st.button("Analyze"):
    if not raw_text.strip():
        st.warning("Please enter at least one contact.")
    else:
        with st.spinner("Analyzing contacts..."):
            st.session_state["results"] = analyze_contacts(raw_text, tone)

if st.session_state["results"]:
    df = (
        pd.DataFrame([
            {
                "priority_score": r.priority_score,
                "persona": r.persona,
                "name": r.name,
                "role_company": r.role_company,
            }
            for r in st.session_state["results"]
        ])
        .sort_values("priority_score", ascending=False)
        .reset_index(drop=True)
    )
    st.dataframe(df, use_container_width=True)

    st.subheader("Contact Details")
    for r in sorted(st.session_state["results"], key=lambda x: x.priority_score, reverse=True):
        with st.expander(f"{r.name} — {r.role_company} (score: {r.priority_score})"):
            st.markdown("**Connection Note**")
            st.code(r.connection_note, language=None)
            st.markdown("**Follow-up DM**")
            st.code(r.follow_up_dm, language=None)
            st.markdown("**Reasoning**")
            for bullet in r.reasoning_bullets:
                st.markdown(f"- {bullet}")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Save to contacts_db.json"):
            raw = json.loads(DB_PATH.read_text()) if DB_PATH.exists() else []
            existing = raw if isinstance(raw, list) else []
            existing.extend([r.model_dump(mode="json") for r in st.session_state["results"]])
            DB_PATH.write_text(json.dumps(existing, indent=2))
            st.success(f"Saved {len(st.session_state['results'])} contact(s) to contacts_db.json")

    with col2:
        db_bytes = DB_PATH.read_bytes() if DB_PATH.exists() else b"[]"
        st.download_button(
            label="Download contacts_db.json",
            data=db_bytes,
            file_name="contacts_db.json",
            mime="application/json",
        )