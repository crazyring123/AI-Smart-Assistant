from google.auth.transport.requests import Request
import os
import datetime
import time
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import cohere
from cohere.errors import TooManyRequestsError

# Define calendar read scope
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

# Load or refresh Google credentials
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

# Initialize clients
creds = load_credentials()
co = cohere.Client("SFPPbhQMlHl0AxctCLNmyzVyqC911eAtG5BVCwHb")  # ⚠️ Trial API key

# Main function used by Streamlit app
def get_calendar_summary(limit=5):
    service = build("calendar", "v3", credentials=creds)
    now = datetime.datetime.utcnow().isoformat() + "Z"

    events_result = service.events().list(
        calendarId="primary",
        timeMin=now,
        maxResults=limit,
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    events = events_result.get("items", [])
    if not events:
        return "No upcoming events found."

    summaries = []

    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        title = event.get("summary", "No Title")
        description = event.get("description", "")
        location = event.get("location", "No location")

        full_text = f"Title: {title}\nTime: {start}\nLocation: {location}\nDetails: {description}"

        try:
            response = co.summarize(text=full_text[:250])
            summary = response.summary if hasattr(response, "summary") else "Could not summarize."
        except TooManyRequestsError as e:
            summary = f"⚠️ Rate limit hit: {e}"
        except Exception as e:
            summary = f"❌ Unexpected error: {e}"

        summaries.append(f"📅 {start} — {title}\n{summary}")
        time.sleep(15)  # Avoid hitting rate limit

    return "\n\n".join(summaries)
