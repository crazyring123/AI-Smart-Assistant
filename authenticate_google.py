from google_auth_oauthlib.flow import InstalledAppFlow
import pickle

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/calendar.readonly"
]

flow = InstalledAppFlow.from_client_secrets_file(
    "credentials.json", SCOPES
)
creds = flow.run_local_server(port=0)

# Save the token
with open("token.json", "w") as token:
    token.write(creds.to_json())

print("✅ New token.json generated with calendar + Gmail scopes.")
