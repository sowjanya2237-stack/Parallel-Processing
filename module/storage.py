import os
import io
import csv
import smtplib
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# --- 1. CONFIGURATION ---
load_dotenv()
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

def prepare_csv_download(df):
    """
    Converts a pandas DataFrame into a CSV byte stream for Streamlit download buttons.
    This is required by the 'Dataset Export' section.
    """
    try:
        output = io.StringIO()
        df.to_csv(output, index=False)
        return output.getvalue().encode('utf-8')
    except Exception as e:
        print(f"Export Error: {e}")
        return None

def send_detailed_email(receiver_email, total, report_data, chart_bytes, csv_df):
    """
    Compiles and dispatches the high-intelligence report via email.
    Includes the numbered list, text samples, PNG chart, and CSV database.
    """
    try:
        # Create Message Container
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = receiver_email
        msg['Subject'] = f"Full System Intelligence Report - {datetime.now().strftime('%Y-%m-%d')}"

        # --- 2.EMAIL BODY ---
        body = "SYSTEM ANALYSIS OVERVIEW:\n"
        body += "-------------------------\n"
        body += "We have successfully processed the entire dataset stored in the vault.\n"
        body += f"Here are the findings from the total of {total:,} records:\n\n"

        for i, item in enumerate(report_data, 1):
            perc = (item['count'] / total * 100) if total > 0 else 0
            body += f"{i}. {item['category'].upper()} REVIEWS/ALERTS: {item['count']:,} ({perc:.1f}%)\n"
            body += "Sample Highlights:\n"
            
            if item['samples']:
                for sample in item['samples']:
                    clean_sample = (sample[:150] + '...') if len(sample) > 150 else sample
                    body += f"- {clean_sample}\n"
            else:
                body += "- No samples detected in this vault.\n"
            body += "\n"

        body += "CONCLUSION:\n"
        body += "A visual distribution chart is attached. A sample CSV database is also attached."
        
        msg.attach(MIMEText(body, 'plain'))

        # --- 3. ATTACH THE CHART  ---
        if chart_bytes:
            part_img = MIMEBase('application', 'octet-stream')
            part_img.set_payload(chart_bytes)
            encoders.encode_base64(part_img)
            part_img.add_header('Content-Disposition', 'attachment; filename="sentiment_chart.png"')
            msg.attach(part_img)

        # --- 4. ATTACH THE CSV DATABASE ---
        if not csv_df.empty:
            csv_part = MIMEBase('application', 'octet-stream')
            csv_part.set_payload(csv_df.to_csv(index=False).encode('utf-8'))
            encoders.encode_base64(csv_part)
            csv_part.add_header('Content-Disposition', 'attachment; filename="Review_dataset.csv"')
            msg.attach(csv_part)

        # --- 5. DISPATCH ---
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        return True, "Dispatch Successful!"
    
    except Exception as e:
        return False, str(e)