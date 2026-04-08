from dotenv import load_dotenv
import os
from loguru import logger
load_dotenv()


GOOGLE_SHEETS_URL = os.getenv("GOOGLE_SHEETS_URL")
SERVICE_ACCOUNT_PATH = os.getenv("SERVICE_ACCOUNT_PATH")
GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")

GOOGLE_SHEETS_URL = os.getenv("GOOGLE_SHEETS_URL")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
SEARCH_URL_CRAIGSLIST = os.getenv("SEARCH_URL_CRAIGSLIST")
SEARCH_URL_RIGHTMOVE = os.getenv("SEARCH_URL_RIGHTMOVE")


required_vars = {
    "GOOGLE_SHEETS_URL": GOOGLE_SHEETS_URL,
    "SERVICE_ACCOUNT_PATH": SERVICE_ACCOUNT_PATH,
    "GMAIL_ADDRESS": GMAIL_ADDRESS,
    "GMAIL_APP_PASSWORD": GMAIL_APP_PASSWORD,
    "SEARCH_URL_CRAIGSLIST": SEARCH_URL_CRAIGSLIST,
    "SEARCH_URL_RIGHTMOVE": SEARCH_URL_RIGHTMOVE,
}

missing_vars = [key for key, value in required_vars.items() if not value]
if missing_vars:
    raise ValueError(
        f"The following environment variables are missing from .env: {', '.join(missing_vars)}")


logger.add(
    "logs/app.log",
    rotation="1 week",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {module} | {message}"
)
