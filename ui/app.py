"""
SQLidator Streamlit Application (Parser-Based)
----------------------------------------------
Features:
- Manual SQL input
- .sql file upload
- Parser-based validation
- Optional Groq AI suggestions
- Downloadable reports (TXT / JSON / CSV)
- Displays AST structure
- Full custom CSS — no prebuilt CSS frameworks
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from engine.validator import validate_query
from reports.text_report import generate_text_report
from reports.json_report import generate_json_report
from reports.csv_report import generate_csv_report

# ==========================================================
# Page Config
# ==========================================================
st.set_page_config(
    page_title="SQLidator",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# Custom CSS — All styling hand-written, zero prebuilt CSS
# ==========================================================
st.markdown("""
<style>
/* ── Google Font Import ─────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;500;600&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');

/* ── Design Tokens ──────────────────────────────────── */
:root {
    --bg-base:         #0d0d0d;
    --bg-surface:      #161616;
    --bg-elevated:     #1f1f1f;
    --bg-input:        #121212;
    --border-default:  #2a2a2a;
    --border-accent:   #3d3d3d;
    --text-primary:    #e8e8e8;
    --text-secondary:  #888888;
    --text-muted:      #555555;
    --accent:          #c8ff00;
    --accent-dim:      rgba(200, 255, 0, 0.08);
    --accent-mid:      rgba(200, 255, 0, 0.15);
    --error:           #ff4d4d;
    --error-dim:       rgba(255, 77, 77, 0.08);
    --success:         #c8ff00;
    --mono:            'IBM Plex Mono', monospace;
    --sans:            'IBM Plex Sans', sans-serif;
    --radius:          4px;
    --transition:      0.18s ease;
}

/* ── Global Reset ───────────────────────────────────── */
*, *::before, *::after {
    box-sizing: border-box;
}

html, body, [data-testid="stAppViewContainer"],
[data-testid="stApp"], .main {
    background-color: var(--bg-base) !important;
    font-family: var(--sans) !important;
    color: var(--text-primary) !important;
}

/* Remove default Streamlit padding */
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 4rem !important;
    max-width: 1200px !important;
}

/* ── Scrollbar ───────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-base); }
::-webkit-scrollbar-thumb { background: var(--border-accent); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }

/* ── Sidebar ─────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background-color: var(--bg-surface) !important;
    border-right: 1px solid var(--border-default) !important;
}

[data-testid="stSidebar"] .block-container {
    padding-top: 2.5rem !important;
}

[data-testid="stSidebar"] * {
    font-family: var(--mono) !important;
    font-size: 0.8rem !important;
    color: var(--text-primary) !important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] .stMarkdown p {
    color: var(--text-secondary) !important;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-size: 0.7rem !important;
    font-weight: 500;
}

/* Sidebar separator */
[data-testid="stSidebar"] hr {
    border-color: var(--border-default) !important;
    margin: 1.5rem 0 !important;
}

/* ── Selectbox ───────────────────────────────────────── */
[data-testid="stSelectbox"] label {
    font-family: var(--mono) !important;
    font-size: 0.72rem !important;
    color: var(--text-muted) !important;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

[data-testid="stSelectbox"] > div > div {
    background-color: var(--bg-elevated) !important;
    border: 1px solid var(--border-default) !important;
    border-radius: var(--radius) !important;
    font-family: var(--mono) !important;
    font-size: 0.82rem !important;
    color: var(--text-primary) !important;
    transition: border-color var(--transition);
}

[data-testid="stSelectbox"] > div > div:hover {
    border-color: var(--border-accent) !important;
}

[data-testid="stSelectbox"] > div > div:focus-within {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 1px var(--accent) !important;
}

/* Dropdown options */
[data-testid="stSelectbox"] ul {
    background-color: var(--bg-elevated) !important;
    border: 1px solid var(--border-default) !important;
    border-radius: var(--radius) !important;
    font-family: var(--mono) !important;
    padding: 4px !important;
}

[data-testid="stSelectbox"] li {
    border-radius: 2px !important;
    font-size: 0.82rem !important;
}

[data-testid="stSelectbox"] li:hover {
    background-color: var(--accent-dim) !important;
    color: var(--accent) !important;
}

/* ── Radio Buttons ───────────────────────────────────── */
[data-testid="stRadio"] label {
    font-family: var(--mono) !important;
    font-size: 0.72rem !important;
    color: var(--text-muted) !important;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

[data-testid="stRadio"] > div {
    gap: 0.5rem !important;
}

[data-testid="stRadio"] > div > label {
    font-family: var(--mono) !important;
    font-size: 0.82rem !important;
    color: var(--text-primary) !important;
    text-transform: none !important;
    letter-spacing: 0 !important;
    background: var(--bg-elevated) !important;
    border: 1px solid var(--border-default) !important;
    border-radius: var(--radius) !important;
    padding: 0.5rem 1rem !important;
    transition: all var(--transition);
    cursor: pointer;
}

[data-testid="stRadio"] > div > label:hover {
    border-color: var(--border-accent) !important;
    background: var(--bg-elevated) !important;
}

/* Active radio */
[data-testid="stRadio"] > div > label:has(input:checked) {
    border-color: var(--accent) !important;
    background: var(--accent-dim) !important;
    color: var(--accent) !important;
}

/* ── Checkbox ─────────────────────────────────────────── */
[data-testid="stCheckbox"] > label {
    font-family: var(--mono) !important;
    font-size: 0.82rem !important;
    color: var(--text-primary) !important;
}

[data-testid="stCheckbox"] span[data-baseweb="checkbox"] {
    background-color: var(--bg-elevated) !important;
    border-color: var(--border-accent) !important;
}

[data-testid="stCheckbox"] input:checked + span {
    background-color: var(--accent) !important;
    border-color: var(--accent) !important;
}

/* ── Text Area ────────────────────────────────────────── */
[data-testid="stTextArea"] label {
    font-family: var(--mono) !important;
    font-size: 0.72rem !important;
    color: var(--text-muted) !important;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

[data-testid="stTextArea"] textarea {
    background-color: var(--bg-input) !important;
    border: 1px solid var(--border-default) !important;
    border-radius: var(--radius) !important;
    color: var(--text-primary) !important;
    font-family: var(--mono) !important;
    font-size: 0.88rem !important;
    line-height: 1.7 !important;
    padding: 1rem !important;
    caret-color: var(--accent) !important;
    transition: border-color var(--transition);
    resize: vertical;
}

[data-testid="stTextArea"] textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 1px var(--accent-mid), 0 0 16px rgba(200, 255, 0, 0.04) !important;
    outline: none !important;
}

[data-testid="stTextArea"] textarea::placeholder {
    color: var(--text-muted) !important;
    font-style: italic;
}

/* ── File Uploader ────────────────────────────────────── */
[data-testid="stFileUploader"] label {
    font-family: var(--mono) !important;
    font-size: 0.72rem !important;
    color: var(--text-muted) !important;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

[data-testid="stFileUploadDropzone"] {
    background-color: var(--bg-input) !important;
    border: 1px dashed var(--border-accent) !important;
    border-radius: var(--radius) !important;
    transition: all var(--transition);
}

[data-testid="stFileUploadDropzone"]:hover {
    border-color: var(--accent) !important;
    background-color: var(--accent-dim) !important;
}

[data-testid="stFileUploadDropzone"] span {
    font-family: var(--mono) !important;
    font-size: 0.82rem !important;
    color: var(--text-secondary) !important;
}

/* ── Primary Button ───────────────────────────────────── */
[data-testid="stButton"] > button[kind="primary"],
[data-testid="stButton"] > button {
    background-color: var(--accent) !important;
    color: #0d0d0d !important;
    border: none !important;
    border-radius: var(--radius) !important;
    font-family: var(--mono) !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 0.65rem 2rem !important;
    cursor: pointer;
    transition: all var(--transition);
    box-shadow: none !important;
}

[data-testid="stButton"] > button:hover {
    background-color: #d4ff1a !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 16px rgba(200, 255, 0, 0.2) !important;
}

[data-testid="stButton"] > button:active {
    transform: translateY(0);
}

/* ── Download Buttons ─────────────────────────────────── */
[data-testid="stDownloadButton"] > button {
    background-color: transparent !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-default) !important;
    border-radius: var(--radius) !important;
    font-family: var(--mono) !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    width: 100% !important;
    padding: 0.6rem 1rem !important;
    transition: all var(--transition);
}

[data-testid="stDownloadButton"] > button:hover {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
    background: var(--accent-dim) !important;
}

/* ── Alert Boxes ──────────────────────────────────────── */
/* Success */
[data-testid="stAlert"][data-baseweb="notification"]:has([data-testid="stMarkdownContainer"]),
.element-container:has([data-testid="stAlert"]) {
    border-radius: var(--radius) !important;
}

div[data-testid="stAlert"] {
    border-radius: var(--radius) !important;
    border: none !important;
    font-family: var(--mono) !important;
    font-size: 0.85rem !important;
}

/* Streamlit success */
.stAlert > div[data-testid="stAlert-success"],
.stSuccess > div {
    background-color: var(--accent-dim) !important;
    border-left: 3px solid var(--accent) !important;
    color: var(--accent) !important;
    border-radius: var(--radius) !important;
}

/* Streamlit error */
.stAlert > div[data-testid="stAlert-error"],
.stError > div {
    background-color: var(--error-dim) !important;
    border-left: 3px solid var(--error) !important;
    color: var(--error) !important;
    border-radius: var(--radius) !important;
}

/* Streamlit warning */
.stAlert > div[data-testid="stAlert-warning"],
.stWarning > div {
    background-color: rgba(255, 180, 0, 0.06) !important;
    border-left: 3px solid #ffb400 !important;
    color: #ffb400 !important;
    border-radius: var(--radius) !important;
}

/* Streamlit info */
.stAlert > div[data-testid="stAlert-info"],
.stInfo > div {
    background-color: rgba(90, 160, 255, 0.06) !important;
    border-left: 3px solid #5aa0ff !important;
    color: #5aa0ff !important;
    border-radius: var(--radius) !important;
}

/* ── Code blocks ──────────────────────────────────────── */
.stCodeBlock pre,
[data-testid="stCode"] pre,
code {
    background-color: var(--bg-input) !important;
    border: 1px solid var(--border-default) !important;
    border-radius: var(--radius) !important;
    font-family: var(--mono) !important;
    font-size: 0.83rem !important;
    color: var(--text-primary) !important;
    line-height: 1.7 !important;
    padding: 1rem 1.2rem !important;
}

/* Code toolbar */
[data-testid="stCode"] > div {
    background-color: var(--bg-input) !important;
}

/* ── Spinner ──────────────────────────────────────────── */
[data-testid="stSpinner"] > div {
    border-top-color: var(--accent) !important;
}

[data-testid="stSpinner"] p {
    font-family: var(--mono) !important;
    font-size: 0.8rem !important;
    color: var(--text-secondary) !important;
}

/* ── Markdown Typography ──────────────────────────────── */
.stMarkdown h1 {
    font-family: var(--mono) !important;
    font-size: 1.6rem !important;
    font-weight: 600 !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.02em;
    margin-bottom: 0.15rem !important;
}

.stMarkdown h2 {
    font-family: var(--mono) !important;
    font-size: 1.1rem !important;
    font-weight: 400 !important;
    color: var(--text-secondary) !important;
    letter-spacing: 0.01em;
    margin-top: 0 !important;
}

.stMarkdown h3 {
    font-family: var(--mono) !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    color: var(--text-muted) !important;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    margin-top: 2rem !important;
    margin-bottom: 0.8rem !important;
}

.stMarkdown p {
    font-family: var(--sans) !important;
    font-size: 0.9rem !important;
    color: var(--text-secondary) !important;
    line-height: 1.6 !important;
}

.stMarkdown strong {
    color: var(--text-primary) !important;
    font-weight: 600 !important;
}

/* ── Horizontal Rule ──────────────────────────────────── */
hr {
    border: none !important;
    border-top: 1px solid var(--border-default) !important;
    margin: 2rem 0 !important;
}

/* ── Caption / Footer ─────────────────────────────────── */
.stCaption,
[data-testid="stCaptionContainer"] {
    font-family: var(--mono) !important;
    font-size: 0.7rem !important;
    color: var(--text-muted) !important;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

/* ── Columns ──────────────────────────────────────────── */
[data-testid="column"] {
    gap: 0.8rem !important;
}

/* ── Custom Header Card ───────────────────────────────── */
.sqlidator-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0 0 1.5rem 0;
}

.sqlidator-logo {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 2.2rem;
    font-weight: 600;
    color: #e8e8e8;
    line-height: 1;
    letter-spacing: -0.04em;
}

.sqlidator-logo span {
    color: #c8ff00;
}

.sqlidator-tag {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    color: #555;
    text-transform: uppercase;
    letter-spacing: 0.16em;
    margin-top: 0.35rem;
}

/* ── Result Card ──────────────────────────────────────── */
.result-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-default);
    border-radius: var(--radius);
    padding: 1.2rem 1.4rem;
    margin: 1rem 0;
}

.result-card.success {
    border-left: 3px solid var(--accent);
    background: var(--accent-dim);
}

.result-card.error {
    border-left: 3px solid var(--error);
    background: var(--error-dim);
}

.result-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: #555;
    margin-bottom: 0.3rem;
}

.result-value {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.88rem;
    color: #e8e8e8;
}

.result-status-ok  { color: #c8ff00; font-weight: 600; }
.result-status-err { color: #ff4d4d; font-weight: 600; }

/* ── Meta Row ─────────────────────────────────────────── */
.meta-row {
    display: flex;
    gap: 2rem;
    margin: 1rem 0;
    flex-wrap: wrap;
}

.meta-item {
    display: flex;
    flex-direction: column;
    gap: 0.2rem;
}

.meta-key {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    color: #555;
    text-transform: uppercase;
    letter-spacing: 0.12em;
}

.meta-val {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.85rem;
    color: #e8e8e8;
}

/* ── Section heading pill ─────────────────────────────── */
.section-heading {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: #555;
    border-bottom: 1px solid #2a2a2a;
    padding-bottom: 0.6rem;
    width: 100%;
    margin: 1.8rem 0 1rem 0;
}

.section-heading::before {
    content: '';
    display: inline-block;
    width: 6px;
    height: 6px;
    background: #c8ff00;
    border-radius: 50%;
}

/* ── Sidebar label style ──────────────────────────────── */
.sidebar-section-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    color: #555;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    margin-bottom: 0.8rem;
    margin-top: 1.2rem;
    display: block;
}

/* ── Hide Streamlit chrome ────────────────────────────── */
#MainMenu { visibility: hidden; }
header[data-testid="stHeader"] { display: none; }
footer { display: none !important; }

/* ── Tooltip / Help icon ──────────────────────────────── */
.stTooltipIcon {
    color: var(--text-muted) !important;
}

/* ── Spinner wrapper ──────────────────────────────────── */
[data-testid="stStatusWidget"] {
    font-family: var(--mono) !important;
    color: var(--text-secondary) !important;
    font-size: 0.8rem !important;
}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# Custom Header
# ==========================================================
st.markdown("""
<div class="sqlidator-header">
  <div>
    <div class="sqlidator-logo">SQL<span>idator</span></div>
    <div class="sqlidator-tag">Parser-Based SQL Validation Engine</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr>', unsafe_allow_html=True)


# ==========================================================
# Sidebar
# ==========================================================
with st.sidebar:
    st.markdown('<span class="sidebar-section-label">Dialect</span>', unsafe_allow_html=True)
    dialect = st.selectbox(
        "SQL Dialect",
        ["postgres", "mysql", "plsql"],
        label_visibility="collapsed"
    )

    st.markdown('<span class="sidebar-section-label">Input Mode</span>', unsafe_allow_html=True)
    input_mode = st.radio(
        "Input Mode",
        ["Manual Query", "Upload .sql File"],
        label_visibility="collapsed"
    )

    st.markdown('<hr>', unsafe_allow_html=True)

    st.markdown('<span class="sidebar-section-label">AI</span>', unsafe_allow_html=True)
    enable_ai = st.checkbox("Enable AI Suggestions (Groq)")

    st.markdown('<hr>', unsafe_allow_html=True)

    st.markdown("""
    <div style="font-family:'IBM Plex Mono',monospace; font-size:0.68rem; color:#444; line-height:1.8;">
    SUPPORTED DIALECTS<br>
    <span style="color:#666">postgres / mysql / plsql</span><br><br>
    REPORT FORMATS<br>
    <span style="color:#666">TXT / JSON / CSV</span>
    </div>
    """, unsafe_allow_html=True)


# ==========================================================
# Query Input
# ==========================================================
st.markdown('<div class="section-heading">SQL Query Input</div>', unsafe_allow_html=True)

query = ""

if input_mode == "Manual Query":
    query = st.text_area(
        "SQL QUERY",
        height=220,
        placeholder="-- Write your SQL here\nSELECT id, name FROM users WHERE active = true;",
        label_visibility="visible"
    )

elif input_mode == "Upload .sql File":
    uploaded_file = st.file_uploader(
        "SQL FILE",
        type=["sql"],
        label_visibility="visible"
    )
    if uploaded_file is not None:
        try:
            query = uploaded_file.read().decode("utf-8")
            st.markdown('<div class="section-heading">File Preview</div>', unsafe_allow_html=True)
            st.code(query, language="sql")
        except Exception:
            st.error("Unable to read the uploaded file.")


# ==========================================================
# Validate Button
# ==========================================================
st.markdown("<div style='margin-top:1.2rem;'>", unsafe_allow_html=True)
run = st.button("Run Validation", type="primary")
st.markdown("</div>", unsafe_allow_html=True)


# ==========================================================
# Validation Logic
# ==========================================================
if run:
    if not query.strip():
        st.warning("No query provided — enter SQL or upload a file.")
    else:
        with st.spinner("Parsing query..."):
            result = validate_query(query, dialect)

        ai_result = None

        # ── AI Suggestions ──────────────────────────────────
        if enable_ai:
            from ai.groq_suggester import get_ai_suggestion
            with st.spinner("Fetching AI suggestions via Groq..."):
                ai_result = get_ai_suggestion(query, result)

        st.markdown('<hr>', unsafe_allow_html=True)

        # ── Validation Result ────────────────────────────────
        status = result.get("status")
        is_ok  = status == "success"

        card_class    = "success" if is_ok else "error"
        status_class  = "result-status-ok" if is_ok else "result-status-err"
        status_label  = "✓ PARSED SUCCESSFULLY" if is_ok else "✗ SYNTAX ERROR"

        st.markdown(f"""
        <div class="result-card {card_class}">
          <div class="result-label">Validation Result</div>
          <div class="result-value {status_class}">{status_label}</div>
        </div>
        """, unsafe_allow_html=True)

        # Meta row
        error_type_html = ""
        if not is_ok:
            error_type_html = f"""
            <div class="meta-item">
                <span class="meta-key">Error Type</span>
                <span class="meta-val" style="color:#ff4d4d;">{result.get("type", "—")}</span>
            </div>
            """

        st.markdown(f"""
        <div class="meta-row">
            <div class="meta-item">
                <span class="meta-key">Dialect</span>
                <span class="meta-val">{result.get("dialect", "—")}</span>
            </div>
            <div class="meta-item">
                <span class="meta-key">Message</span>
                <span class="meta-val">{result.get("message", "—")}</span>
            </div>
            {error_type_html}
        </div>
        """, unsafe_allow_html=True)

        # ── AST Display ─────────────────────────────────────
        if is_ok:
            st.markdown('<div class="section-heading">Parsed AST</div>', unsafe_allow_html=True)
            ast = result.get("ast")
            if isinstance(ast, list):
                for i, stmt in enumerate(ast, 1):
                    st.markdown(
                        f'<div class="result-label" style="margin-top:0.8rem;">Statement {i}</div>',
                        unsafe_allow_html=True
                    )
                    st.code(str(stmt), language="python")
            else:
                st.code(str(ast), language="python")

        # ── AI Output ───────────────────────────────────────
        if enable_ai and ai_result:
            st.markdown('<div class="section-heading">AI Suggestions</div>', unsafe_allow_html=True)
            ai_status = ai_result.get("ai_status")
            ai_msg    = ai_result.get("ai_message", "")

            if ai_status == "success":
                st.info(ai_msg)
            elif ai_status == "disabled":
                st.warning(ai_msg)
            else:
                st.error(ai_msg)

        # ── Reports ─────────────────────────────────────────
        text_report = generate_text_report(query, result, ai_result)
        json_report = generate_json_report(query, result, ai_result)
        csv_report  = generate_csv_report(query, result, ai_result)

        st.markdown('<div class="section-heading">Download Report</div>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.download_button(
                label="↓ TXT Report",
                data=text_report,
                file_name="sqlidator_report.txt",
                mime="text/plain"
            )
        with col2:
            st.download_button(
                label="↓ JSON Report",
                data=json_report,
                file_name="sqlidator_report.json",
                mime="application/json"
            )
        with col3:
            st.download_button(
                label="↓ CSV Report",
                data=csv_report,
                file_name="sqlidator_report.csv",
                mime="text/csv"
            )


# ==========================================================
# Footer
# ==========================================================
st.markdown('<hr>', unsafe_allow_html=True)
st.caption("SQLidator — A SQL Validation Engine with Groq AI Suggestions | Developed by HufflePuff Group 3")