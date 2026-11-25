"""Central environment configuration.

Loads the .env next to this file once and exposes plain constants that the
rest of the app imports. Real environment variables take precedence over .env
values (``load_dotenv`` does not override them by default).
"""
import os
from pathlib import Path

from dotenv import load_dotenv

ENV_FILE = Path(__file__).resolve().parent / ".env"
load_dotenv(ENV_FILE)

JWT_SECRET = os.getenv("JWT_SECRET")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin").strip()
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
SESSION_SECRET = os.getenv("SESSION_SECRET")
SESSION_HTTPS_ONLY = os.getenv("SESSION_HTTPS_ONLY", "false").lower() in {"1","true"}
CRYPTID_SQLITE_DB = os.getenv("CRYPTID_SQLITE_DB")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv(
    "GOOGLE_REDIRECT_URI", "http://localhost:8000/auth/google/callback"
)

if not JWT_SECRET:
    raise RuntimeError("JWT_SECRET environment variable is not set")
if not SESSION_SECRET:
    raise RuntimeError("SESSION_SECRET environment variable is not set")
if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
    raise RuntimeError(
        "GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET environment variables are not set"
    )
