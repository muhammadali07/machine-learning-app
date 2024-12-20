import os
from dotenv import load_dotenv

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
    raise EnvironmentError("Pastikan semua variabel GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, dan GOOGLE_REDIRECT_URI diatur di file .env.")
