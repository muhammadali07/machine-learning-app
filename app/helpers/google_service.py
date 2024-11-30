import os
from dotenv import load_dotenv

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Load variabel lingkungan dari .env
load_dotenv()

# Ambil variabel dari lingkungan
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

# Constants for Google OAuth
GOOGLE_AUTH_URI = os.getenv("GOOGLE_AUTH_URI")
GOOGLE_TOKEN_URI = os.getenv("GOOGLE_TOKEN_URI")
GOOGLE_USERINFO_URI = os.getenv("GOOGLE_USERINFO_URI")

# Validasi jika variabel tidak ditemukan
if not all([GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI]):
    raise EnvironmentError(
        "Pastikan semua variabel GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, dan GOOGLE_REDIRECT_URI diatur di file .env.")

# add data google calender
# Scopes required for Google Calendar
SCOPES = ['https://www.googleapis.com/auth/calendar.events']


async def get_google_calendar_service():
    """Authenticate and get Google Calendar service."""
    creds = None
    token_path = 'token.json'
    credentials_path = 'credentials.json'

    # Load token if exists
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    # Authenticate and save token if not exists
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save token for future use
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    return build('calendar', 'v3', credentials=creds)
