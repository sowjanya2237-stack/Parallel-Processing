import streamlit as st

def apply_global_style():
    st.markdown("""
        <style>
        /* 1. Global Theme */
        .stApp { 
            background: radial-gradient(circle at 50% -20%, #2b1055 0%, #050505 60%) !important; 
            color: #ffffff; 
        }

        /* 2. Title Styling */
        h1 { 
            font-size: 2.2rem !important; 
            letter-spacing: 2px !important;
            text-transform: uppercase;
            font-weight: 800 !important;
            text-align: center;
            margin-bottom: 0.8rem !important; /* INCREASED: Adds space below title */
            padding-bottom: 0rem !important;
        }

        /* 3. Subtitle Styling (with added space) */
        .subtitle { 
            text-align: center; 
            color: #888888; 
            font-size: 0.95rem; 
            letter-spacing: 3px; 
            margin-top: 0.5rem !important; /* CHANGED: Added positive space above subtitle */
            margin-bottom: 3rem !important; /* Space before the dashboard cards start */
            text-transform: uppercase;
        }

        /* 4. Sidebar & Cards */
        [data-testid="stSidebar"] { background-color: #080808; border-right: 1px solid #1f1f1f; }
        .card { background-color: #0c0c0c; border: 1px solid #1f1f1f; padding: 20px; border-radius: 12px; height: 100%; }
        
        /* 5. Buttons */
        div.stButton > button:first-child { 
            background: linear-gradient(180deg, #ffffff 0%, #e0e0e0 100%) !important; 
            color: #000000 !important; border-radius: 6px !important; font-weight: 800 !important;
        
        
        .upload-card {
            background-color: #0c0c0c; 
            border: 1px solid #1f1f1f; 
            border-radius: 15px; 
            padding: 50px 30px; /* Large padding to create the 'frame' look */
            margin-top: 20px;
        }

        /* Target the actual Streamlit File Uploader Widget */
        [data-testid="stFileUploader"] {
            background-color: #1a1b1e !important; /* Slightly lighter inner box */
            border: 1px solid #333 !important;
            border-radius: 10px !important;
            padding: 10px !important;
        }

        /* Target the 'Browse files' button inside the widget */
        [data-testid="stFileUploader"] button {
            background-color: #262730 !important;
            color: white !important;
            border: 1px solid #444 !important;
            border-radius: 8px !important;
        }
        
        /* Styling Warning (Yellow/Brown) Banners */
        [data-testid="stNotification"] {
            background-color: rgba(255, 165, 0, 0.1) !important;
            color: #e6a23c !important;
            border: 1px solid rgba(255, 165, 0, 0.2) !important;
            border-radius: 10px !important;
        }

        /* Specifically styling the 'Info' (Blue) Banners */
        .stAlert:has(div[aria-label="Info"]) {
        background-color: rgba(0, 102, 204, 0.1) !important;
        color: #409eff !important;
        border: 1px solid rgba(0, 102, 204, 0.2) !important;
        }

        /* Styling the Status/Success (Green) Banners */
            .stAlert:has(div[aria-label="Success"]) {
            background-color: rgba(0, 255, 100, 0.1) !important;
            color: #00ff64 !important;
            border: 1px solid rgba(0, 255, 100, 0.2) !important;
        }

        /* The White RUN Button */
        div.stButton > button:first-child { 
            background: linear-gradient(180deg, #ffffff 0%, #e0e0e0 100%) !important; 
            color: #000000 !important; 
            border-radius: 6px !important; 
            font-weight: 800 !important;
            padding: 0.8rem 2rem !important;
            width: auto !important; /* Makes it a square/rectangle button like your screen */
            box-shadow: 0 4px 15px rgba(255, 255, 255, 0.2);
        }
        
        /* This looks for the success alert inside the status widget */
        div[data-testid="stAlert"]:has(div[aria-label="Success"]) {
            background-color: #0c2014 !important; /* Very dark green background */
            border: 1px solid #1a3d2a !important; /* Subtle green border */
            border-radius: 10px !important;
            padding: 20px !important;
        }

        /* Styling the text inside that specific success box */
        div[data-testid="stAlert"]:has(div[aria-label="Success"]) div[data-testid="stMarkdownContainer"] p {
            color: #00ff66 !important; /* Vibrant neon green text */
            font-weight: 800 !important;
            font-size: 1.1rem !important;
            text-transform: uppercase !important; /* Makes it ALL CAPS */
            letter-spacing: 1px !important;
        }

        /* Styling the 'processing.......' status box header */
        [data-testid="stStatusWidget"] {
            background-color: #0c0c0c !important;
            border: 1px solid #1f1f1f !important;
            border-radius: 10px !important;
        }
        /* Specific styling for the Error Alert to match the screenshot */
        div[data-testid="stAlert"]:has(div[aria-label="Error"]) {
            background-color: #3d1a1a !important; /* Dark muted red */
            border: 1px solid #5c2626 !important; /* Slightly lighter border */
            color: #ffb3b3 !important; /* Light reddish text */
            border-radius: 8px !important;
        }

        div[data-testid="stAlert"]:has(div[aria-label="Error"]) p {
            font-weight: 600 !important;
        }
        </style>
        """, unsafe_allow_html=True)