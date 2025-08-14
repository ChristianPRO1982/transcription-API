"""
Security and app configuration. Use env vars in production.
"""

import os
from datetime import timedelta
from dotenv import load_dotenv

# Load .env file
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "dev_only_change_me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MIN = int(os.getenv("ACCESS_TOKEN_EXPIRE_MIN", "30"))
ACCESS_TOKEN_EXPIRE_DELTA = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MIN)

DEMO_USERNAME = os.getenv("DEMO_USERNAME", "service")
DEMO_PASSWORD = os.getenv("DEMO_PASSWORD", "change_me")
