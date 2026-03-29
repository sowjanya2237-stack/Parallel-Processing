import streamlit as st
import pandas as pd
import plotly.express as px
from module.ui_utils import apply_global_style
from database.database import fetch_data, get_sentiment_distribution

# 1. INITIALIZE THEME
apply_global_style()

# 2. HEADER SECTION
st.markdown("<p class='subtitle' style='margin-top: 2rem;'>CENTRAL REGISTRY RECORDS</p>", unsafe_allow_html=True)

# 3. REGISTRY FILTER SECTION
st.markdown("## 🔍 Registry Filter")
st.write("Select results")

categories = [
    "All Records", "Positive", "Negative", "Neutral", 
    "Spam", "Abusive", "Urgent", "Suggestion"
]

selected_filter = st.selectbox(
    "Select results", 
    options=categories, 
    label_visibility="collapsed"
)

st.markdown("---")

# 4. REGISTRY MATRIX 
st.markdown(f"## Registry Matrix ({selected_filter})")

try:
    # Fetch data from database based on the selected dropdown filter
    df = fetch_data(selected_filter, limit=1000)
    
    if not df.empty:
        st.dataframe(df, use_container_width=True, height=450)
    else:
        st.info("No records found for this category.")

except Exception as e:
    st.error(f"Vault Access Error: {e}")

st.markdown("---")

# 5. SENTIMENT DISTRIBUTION ANALYSIS (CHART)
st.markdown("## Sentiment Distribution Analysis")

# Fetch counts from DB for the chart
df_counts = get_sentiment_distribution()

if not df_counts.empty:
    color_map = {
        'Positive': '#00ffcc',   # Cyan
        'Neutral': '#888888',    # Gray
        'Negative': '#ff0066',   # Pink/Magenta
        'Abusive': '#ff0000',    # Red
        'Spam': '#ffaa00',       # Orange
        'Suggestion': '#636efa', # Blue
        'Urgent': '#ff4b4b'      # Coral/Light Red
    }

    # Create the Chart
    fig = px.pie(
        df_counts, 
        values='count', 
        names='sentiment', 
        hole=0.6,
        color='sentiment',
        color_discrete_map=color_map
    )

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        margin=dict(t=20, b=20, l=0, r=0),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5
        )
    )
    
    # Display Chart
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("Run the Process Engine to generate distribution data.")