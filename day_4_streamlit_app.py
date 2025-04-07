import streamlit as st
import time
from email_summary_service import get_gmail_summaries
from calendar_summary_service import get_calendar_summary
from slack_notifier import send_email_summaries_to_slack
from smart_reply_generator import generate_reply  # ✅ NEW

st.set_page_config(page_title="📬 Daily Email & Calendar Summary", layout="centered")

st.title("📬 AI Personal Assistant Dashboard")
st.write("Welcome! Here's a summary of your latest emails and calendar events.")

# Buttons
col1, col2 = st.columns(2)
with col1:
    refresh = st.button("🔄 Refresh Summary")
with col2:
    send_to_slack = st.button("📤 Send to Slack")

# Email Summaries
st.subheader("📧 Latest Emails")
email_limit = 5 if refresh else 3

try:
    emails = get_gmail_summaries(limit=email_limit)
    if emails:
        for i, email in enumerate(emails, 1):
            st.markdown(f"### ✉️ Email #{i}")
            st.markdown(f"**From:** {email['from']}")
            st.markdown(f"**Subject:** {email['subject']}")
            st.markdown(f"**Summary:** {email['summary']}")

            with st.expander("💬 Generate Smart Reply"):
                if st.button(f"✉️ Generate Reply for Email #{i}"):
                    reply = generate_reply(email['summary'])
                    st.success(reply)

            st.markdown("---")
    else:
        st.info("No recent emails found.")
except Exception as e:
    st.error(f"❌ Failed to load email summaries: {e}")

# Send to Slack
if send_to_slack:
    try:
        send_email_summaries_to_slack(emails)
        st.success("✅ Email summaries sent to Slack!")
    except Exception as e:
        st.error(f"❌ Failed to send to Slack: {e}")

# Calendar Summary
st.subheader("🗓️ Today's Calendar Summary")
try:
    calendar_summary = get_calendar_summary()
    if calendar_summary:
        st.markdown(f"{calendar_summary}")
    else:
        st.info("No upcoming events found.")
except Exception as e:
    st.error(f"❌ Failed to load calendar summary: {e}")
