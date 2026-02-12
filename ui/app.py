"""
SQLidator Streamlit Application
--------------------------------
Features:
- Manual SQL input
- .sql file upload
- Offline validation
- Optional Groq AI suggestions
- Downloadable reports (TXT / JSON / CSV)
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import streamlit as st
from engine.validator import validate_query
from reports.text_report import generate_text_report
from reports.json_report import generate_json_report
from reports.csv_report import generate_csv_report


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="SQLidator",
    page_icon="🚀",
    layout="wide"
)


# --------------------------------------------------
# Header
# --------------------------------------------------
st.markdown(
    """
    # 🚀 SQLidator  
    ### Modular SQL Validation Engine
    """
)

st.markdown("---")


# --------------------------------------------------
# Sidebar Configuration
# --------------------------------------------------
st.sidebar.header("⚙️ Configuration")

dialect = st.sidebar.selectbox(
    "Select SQL Dialect",
    ["mysql", "postgres", "plsql"]
)

input_mode = st.sidebar.radio(
    "Input Mode",
    ["Manual Query", "Upload .sql File"]
)

enable_ai = st.sidebar.checkbox("Enable AI Suggestions (Online Mode)")


# --------------------------------------------------
# Main Input Section
# --------------------------------------------------
query = ""

if input_mode == "Manual Query":

    query = st.text_area(
        "Enter SQL Query",
        height=250,
        placeholder="Example:\nSELECT * FROM users;"
    )

elif input_mode == "Upload .sql File":

    uploaded_file = st.file_uploader(
        "Upload SQL File",
        type=["sql"]
    )

    if uploaded_file is not None:
        try:
            query = uploaded_file.read().decode("utf-8")
            st.code(query, language="sql")
        except Exception:
            st.error("Unable to read file.")


# --------------------------------------------------
# Validate Button
# --------------------------------------------------
if st.button("Validate Query"):

    if not query.strip():
        st.warning("Please provide a SQL query.")
    else:

        with st.spinner("Validating query..."):
            result = validate_query(query, dialect)

        ai_result = None

        # ---------------------------
        # AI Suggestions (Optional)
        # ---------------------------
        if enable_ai:
            from ai.groq_suggester import get_ai_suggestion

            with st.spinner("Getting AI suggestions..."):
                ai_result = get_ai_suggestion(query, result)

        st.markdown("---")

        # ---------------------------
        # Display Validation Result
        # ---------------------------
        if result.get("status") == "success":
            st.success("✅ Validation Successful")
        else:
            st.error("❌ Validation Failed")

        st.write("**Dialect:**", result.get("dialect"))
        st.write("**Message:**", result.get("message"))

        if result.get("status") == "error":
            st.write("**Error Type:**", result.get("type"))

        # ---------------------------
        # Display AI Suggestions
        # ---------------------------
        if enable_ai and ai_result:
            st.markdown("### 🤖 AI Suggestions")

            if ai_result.get("ai_status") == "success":
                st.info(ai_result.get("ai_message"))
            elif ai_result.get("ai_status") == "disabled":
                st.warning(ai_result.get("ai_message"))
            else:
                st.error(ai_result.get("ai_message"))

        # ---------------------------
        # Generate Reports
        # ---------------------------
        text_report = generate_text_report(query, result, ai_result)
        json_report = generate_json_report(query, result, ai_result)
        csv_report = generate_csv_report(query, result, ai_result)

        st.markdown("### 📥 Download Report")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.download_button(
                label="Download TXT",
                data=text_report,
                file_name="sqlidator_report.txt",
                mime="text/plain"
            )

        with col2:
            st.download_button(
                label="Download JSON",
                data=json_report,
                file_name="sqlidator_report.json",
                mime="application/json"
            )

        with col3:
            st.download_button(
                label="Download CSV",
                data=csv_report,
                file_name="sqlidator_report.csv",
                mime="text/csv"
            )


# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown("---")
st.caption("SQLidator • Offline + AI Hybrid • Secure • Modular")
