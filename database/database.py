import os
import sqlite3
import pandas as pd
from dotenv import load_dotenv

# --- 1. CONFIGURATION LOADING ---
load_dotenv()

DB_NAME = os.getenv("DB_NAME", "sentiment_results.db")

def get_connection():
    """
    Creates a connection to the SQLite database with high-performance 
    settings to handle parallel processing safely.
    """
    conn = sqlite3.connect(DB_NAME, timeout=30)
    
    # PERFORMANCE OPTIMIZATIONS
    conn.execute("PRAGMA journal_mode = WAL")      
    conn.execute("PRAGMA synchronous = OFF")     
    conn.execute("PRAGMA temp_store = MEMORY")   
    conn.execute("PRAGMA busy_timeout = 30000")  
    
    return conn

def init_db():
    """
    Initializes the database schema. 
    Call this in your main app.py on startup.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
            text TEXT,
            score INTEGER,
            sentiment TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_analysis_results(payload):
    """
    Clears old records and saves a fresh batch of analysis results.
    Used by the pipeline.py after processing is complete.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Resetting table for the new analysis session
    cursor.execute("DROP TABLE IF EXISTS results")
    cursor.execute("CREATE TABLE results (text TEXT, score INTEGER, sentiment TEXT, timestamp TEXT)")
    
    cursor.executemany("INSERT INTO results VALUES (?, ?, ?, ?)", payload)
    
    conn.commit()
    conn.close()

def fetch_data(filter_category="All Records", limit=500):
    """
    Retrieves records from the database based on UI filters.
    Returns a Pandas DataFrame for the Registry Vault.
    """
    conn = get_connection()
    
    if filter_category == "All Records":
        query = "SELECT * FROM results ORDER BY rowid DESC LIMIT ?"
        df = pd.read_sql_query(query, conn, params=(limit,))
    else:
        query = "SELECT * FROM results WHERE sentiment = ? ORDER BY rowid DESC LIMIT ?"
        df = pd.read_sql_query(query, conn, params=(filter_category, limit))
    
    conn.close()
    return df

def get_sentiment_distribution():
    """
    Aggregates sentiment counts for the Plotly charts.
    """
    conn = get_connection()
    query = "SELECT sentiment, COUNT(*) as count FROM results GROUP BY sentiment"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def clear_database():
    """
    Deletes the database file from the disk.
    """
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)

def get_detailed_report_data():
    """
    Fetches the total count, category counts, and text samples for the email report.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Get Total
    total = cursor.execute("SELECT COUNT(*) FROM results").fetchone()[0]
    
    order = ["Positive", "Negative", "Neutral", "Urgent", "Abusive", "Spam", "Suggestion"]
    
    report_structure = []
    
    for cat in order:
        count = cursor.execute("SELECT COUNT(*) FROM results WHERE sentiment=?", (cat,)).fetchone()[0]
        samples = cursor.execute("SELECT text FROM results WHERE sentiment=? LIMIT 3", (cat,)).fetchall()
        
        report_structure.append({
            "category": cat,
            "count": count,
            "samples": [s[0] for s in samples]
        })
        
    conn.close()
    return total, report_structure