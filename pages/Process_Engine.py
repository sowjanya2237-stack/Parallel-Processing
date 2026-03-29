import streamlit as st
import time
from module.ui_utils import apply_global_style
from pipeline import run_processing_pipeline

apply_global_style()

st.markdown("<p class='subtitle'>INITIALIZE ANALYSIS SEQUENCE</p>", unsafe_allow_html=True)

if 'uploaded_data_list' in st.session_state and st.session_state.uploaded_data_list:
    data = st.session_state.uploaded_data_list
    
    st.info(f"Target Workload: {len(data):,} entries.")
    
    if st.button("RUN"):
        start_time = time.time()
        
        with st.status("processing.......", expanded=True) as status:
            try:
                # Run the actual calculation
                count = run_processing_pipeline(data)
                
                duration = time.time() - start_time
                
                st.success(f"PROCESSED {count:,} RECORDS IN {duration:.2f}s")
                
                status.update(label="processing.......", state="complete")
                
            except Exception as e:
                status.update(label="❌ error", state="error")
                st.error(str(e))
else:
    st.warning("PLEASE UPLOAD A FILE")