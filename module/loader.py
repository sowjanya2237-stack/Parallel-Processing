import pandas as pd
import streamlit as st

def load_uploaded_file(uploaded_file):
    try:
        filename = uploaded_file.name.lower()
        
        if filename.endswith('.csv'):
            return pd.read_csv(uploaded_file)
            
        elif filename.endswith('.txt'):
            try:
                df = pd.read_csv(uploaded_file, sep=None, engine='python')
                
                if len(df.columns) <= 1:
                    uploaded_file.seek(0) 
                    raw_text = uploaded_file.getvalue().decode("utf-8")
                    lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
                    return pd.DataFrame(lines, columns=["Text Content"])
                
                return df
            except Exception:
                uploaded_file.seek(0)
                raw_text = uploaded_file.getvalue().decode("utf-8")
                lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
                return pd.DataFrame(lines, columns=["Text Content"])
            
        return None
    except Exception as e:
        st.error(f"Loader Error: {e}")
        return None

def validate_text_column(df, column_name):
    """
    Validates based on your specific error requirement.
    """
    # Check if column is numeric (like 'Id')
    is_numeric = pd.api.types.is_numeric_dtype(df[column_name])
    
    # Check if text is too short
    sample = df[column_name].dropna().head(100).astype(str)
    avg_len = sample.str.len().mean() if not sample.empty else 0
    is_too_short = avg_len < 15

    if is_numeric or is_too_short:
        return False, f"INVALID SELECTION: '{column_name}' is numerical or too short."
    
    return True, "Success"