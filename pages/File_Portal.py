import streamlit as st
import pandas as pd
from module.ui_utils import apply_global_style
from module.loader import load_uploaded_file, validate_text_column

apply_global_style()

# Header Section
st.markdown("<p class='subtitle'>SELECT A DOCUMENT TO BEGIN PROCESSING</p>", unsafe_allow_html=True)

st.markdown('<div class="upload-card">', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload", type=["csv", "txt"], label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

if uploaded_file is not None:
    if st.session_state.get('uploaded_data_list') is None:
        with st.spinner("Analyzing dataset structure......."):
            df = load_uploaded_file(uploaded_file)
            
            if df is not None:
                st.markdown("---")
                st.markdown("### Data Preview")
                # This will now show the columns (Id, ProductId, etc.)
                st.dataframe(df.head(5), use_container_width=True)

                st.markdown("#### Select Configuration")
                target_col = st.selectbox("Select Text Column to Analyze", df.columns.tolist(), index=0)
                
                # Run your specific validation
                is_valid, message = validate_text_column(df, target_col)

                if not is_valid:
                    # error box for 'Id' or short text
                    st.error(message)
                else:
                    st.success(" Dataset structure validated.")
                    if st.button("CONFIRM DATASET"):
                        st.session_state.uploaded_data_list = df[target_col].dropna().astype(str).tolist()
                        st.rerun()

# Workspace Status
if st.session_state.get('uploaded_data_list'):
    st.markdown("---")
    st.info(f" Active Dataset: {len(st.session_state.uploaded_data_list):,} records loaded.")
    if st.button("CLEAR WORKSPACE"):
        st.session_state.uploaded_data_list = None
        st.rerun()