from google.auth.transport.requests import Request
import base64
import os
import time
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import cohere
from cohere.errors import TooManyRequestsError  # ✅ Correct import for rate-limit handling

# Define Gmail + Calendar scopes
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/calendar.readonly"
]

# Load or refresh credentials
def load_credentials():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token_file:
            token_file.write(creds.to_json())
    return creds

# Initialize credentials and Cohere client
creds = load_credentials()
co = cohere.Client("SFPPbhQMlHl0AxctCLNmyzVyqC911eAtG5BVCwHb")  # ⚠️ Replace with production key when needed

# Function to fetch and summarize Gmail messages
def get_gmail_summaries(limit=3):
    print("⚠️ Using Cohere trial API key: limited to 5 summarizations per minute.")

    service = build("gmail", "v1", credentials=creds)
    results = service.users().messages().list(userId="me", maxResults=limit).execute()
    messages = results.get("messages", [])

    email_summaries = []

    for msg in messages:
        msg_data = service.users().messages().get(userId="me", id=msg["id"]).execute()
        payload = msg_data.get("payload", {})
        headers = payload.get("headers", [])

        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "No Subject")
        sender = next((h["value"] for h in headers if h["name"] == "From"), "Unknown Sender")

        parts = payload.get("parts", [])
        body = ""
        if parts:
            for part in parts:
                if part.get("mimeType") == "text/plain":
                    data = part.get("body", {}).get("data", "")
                    body = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
                    break

        if not body:
            body = "(No content found)"

        # Summarize using Cohere (with error handling)
        try:
            response = co.summarize(text=body[:250])
            summary = response.summary if hasattr(response, "summary") else "Could not summarize."
        except TooManyRequestsError as e:
            summary = f"⚠️ Rate limit hit: {e}"
        except Exception as e:
            summary = f"❌ Unexpected error: {e}"

        email_summaries.append({
        "subject": subject,
        "from": sender,
        "summary": summary,
        "body": body  # 👈 Add this line
        })


        time.sleep(15)  # Wait to avoid hitting Cohere rate limits

    return email_summaries
