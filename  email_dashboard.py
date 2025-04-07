import sqlite3
import streamlit as st
from datetime import datetime

DB_FILE = "emails.db"

def get_emails():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT subject, sender, body, summary, timestamp FROM emails ORDER BY timestamp DESC")
    emails = c.fetchall()
    conn.close()
    return emails

st.set_page_config(page_title="Email Summary Dashboard", layout="wide")
st.title("📬 Email Summary Viewer")

search_query = st.text_input("🔍 Search subject/sender/summary")

emails = get_emails()

if not emails:
    st.info("No emails found. Run `email_service.py` first.")
else:
    for subject, sender, body, summary, timestamp in emails:
        if search_query.lower() in (subject or "").lower() or \
           search_query.lower() in (sender or "").lower() or \
           search_query.lower() in (summary or "").lower():

            with st.expander(f"📨 {subject} | From: {sender}"):
                st.markdown(f"**Summary:** {summary or '❌ No summary'}")
                if st.checkbox("Show full body", key=subject):
                    st.text_area("Email Body", body, height=200)

