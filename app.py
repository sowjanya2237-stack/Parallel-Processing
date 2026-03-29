import streamlit as st
import multiprocessing
from module.ui_utils import apply_global_style
from database.database import init_db

# Page Setup
st.set_page_config(page_title="Parallel System Pro", page_icon="⚡", layout="wide")
apply_global_style()
init_db()

# --- HEADER SECTION ---
st.markdown("<h1>  PARALLEL SYSTEM PRO</h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='subtitle'>SENTIMENT & DATA INTELLIGENCE ENGINE</p>",
    unsafe_allow_html=True,
)

st.markdown("---")

# --- DASHBOARD SECTION ---
col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        <div class='card'>
            <h3 style='color:#ffffff;'>SYSTEM WORKFLOW</h3>
            <p style='color:#bbbbbb; font-size: 0.9rem;'>1. <b>File Portal:</b> Upload and validate CSV/TXT datasets.</p>
            <p style='color:#bbbbbb; font-size: 0.9rem;'>2. <b>Process Engine:</b> Initialize multi-core parallel analysis.</p>
            <p style='color:#bbbbbb; font-size: 0.9rem;'>3. <b>Registry Vault:</b> Explore results and sentiment insights.</p>
            <p style='color:#bbbbbb; font-size: 0.9rem;'>4. <b>Report Distribution:</b> Export data and dispatch email reports.</p>
        </div>
    """,
        unsafe_allow_html=True,
    )


st.markdown("<br>", unsafe_allow_html=True)
st.info("👈 **Select a stage from the sidebar to begin.**")
