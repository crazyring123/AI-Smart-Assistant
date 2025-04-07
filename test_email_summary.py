from email_summary_service import get_gmail_summaries

print("🔍 Fetching email summaries...")

emails = get_gmail_summaries(limit=3)

for i, email in enumerate(emails, 1):
    print(f"\n📧 Email #{i}")
    print(f"From: {email['from']}")
    print(f"Subject: {email['subject']}")
    print(f"Summary: {email['summary']}")
