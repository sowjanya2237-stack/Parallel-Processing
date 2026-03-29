import streamlit as st
import time
import plotly.express as px
from module.ui_utils import apply_global_style
from database.database import fetch_data, get_detailed_report_data, get_sentiment_distribution
from module.storage import prepare_csv_download, send_detailed_email

# 1. INITIALIZE THEME
apply_global_style()

# 2. HEADER SECTION
st.markdown("<h1 style='text-align: center;'>⚡ REPORT DISTRIBUTION</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>DISPATCH SYSTEM INTELLIGENCE</p>", unsafe_allow_html=True)

# --- 3. DATASET EXPORT SECTION ---
st.markdown("## 📥 Dataset Export")

if st.button("PREPARE ENTIRE VAULT FOR DOWNLOAD"):
    with st.status("Preparing data...", expanded=True) as status:
        try:
            # Fetch all records from the database
            df_full = fetch_data("All Records", limit=200000)
            
            if not df_full.empty:
                # Convert dataframe to CSV byte stream
                csv_bytes = prepare_csv_download(df_full)
                
                time.sleep(1.5)
                
                status.update(label="Export Ready!", state="complete")
                
                st.download_button(
                    label="📥 DOWNLOAD DATABASE",
                    data=csv_bytes,
                    file_name="review_database.csv",
                    mime="text/csv"
                )
            else:
                status.update(label="Export Failed: Vault is empty.", state="error")
        except Exception as e:
            status.update(label=f"System Error: {e}", state="error")

st.markdown("---")

# --- 4. DETAILED INTELLIGENCE EMAIL SECTION ---
st.markdown("## 📧 Detailed Intelligence Email")

st.write("Enter Destination Email Address")
receiver_email = st.text_input(
    "Enter Destination Email Address", 
    placeholder="client@example.com", 
    label_visibility="collapsed"
)

if st.button("DISPATCH REPORT"):
    if not receiver_email:
        st.error("Please provide a destination email address.")
    else:
        with st.status("Compiling Report......", expanded=True) as status:
            try:
                total, report_data = get_detailed_report_data()
                
                sample_df = fetch_data("All Records", limit=1000)
                
                df_counts = get_sentiment_distribution()
                
                color_map = {
                    'Positive': '#00ffcc', 'Neutral': '#888888', 'Negative': '#ff0066', 
                    'Abusive': '#ff0000', 'Spam': '#ffaa00', 'Suggestion': '#636efa', 'Urgent': '#ff4b4b'
                }
                
                fig = px.pie(
                    df_counts, values='count', names='sentiment', hole=0.6,
                    color='sentiment', color_discrete_map=color_map
                )
                
                chart_img_bytes = fig.to_image(format="png", engine="kaleido")

                success, msg = send_detailed_email(
                    receiver_email=receiver_email,
                    total=total,
                    report_data=report_data,
                    chart_bytes=chart_img_bytes,
                    csv_df=sample_df
                )
                
                if success:
                    status.update(label="Dispatch Successful!", state="complete")
                    st.success(f"Report sent to {receiver_email}")
                else:
                    status.update(label="Dispatch Failed", state="error")
                    st.error(msg)
                    
            except Exception as e:
                status.update(label="Critical System Error", state="error")
                st.error(f"Error compiling report: {str(e)}")

st.markdown("<br><br>", unsafe_allow_html=True)