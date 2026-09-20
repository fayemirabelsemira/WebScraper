from pathlib import Path
import os

from dotenv import load_dotenv


# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)


# ==========================================
# WEBSITE CONFIGURATION
# ==========================================

TARGET_URL = os.getenv(
    "TARGET_URL",
    "https://books.toscrape.com/"
)


# ==========================================
# HTTP CONFIGURATION
# ==========================================

REQUEST_TIMEOUT = int(
    os.getenv("REQUEST_TIMEOUT", "10")
)

MAX_RETRIES = int(
    os.getenv("MAX_RETRIES", "3")
)

RETRY_BACKOFF_FACTOR = float(
    os.getenv("RETRY_BACKOFF_FACTOR", "1")
)

RETRY_STATUS_CODES = [
    429,
    500,
    502,
    503,
    504,
]


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/140.0.0.0 Safari/537.36"
    )
}


# ==========================================
# DATABASE CONFIGURATION
# ==========================================

DATABASE_PATH = BASE_DIR / "data" / "books.db"


# ==========================================
# STORAGE DIRECTORIES
# ==========================================

DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"
REPORT_DIR = BASE_DIR / "reports"


# ==========================================
# OUTPUT FILES
# ==========================================

CSV_OUTPUT = DATA_DIR / "books.csv"
JSON_OUTPUT = DATA_DIR / "books.json"
REPORT_OUTPUT = REPORT_DIR / "scraper_report.txt"
DATABASE_CSV_OUTPUT = DATA_DIR / "database_books.csv"


# ==========================================
# SCRAPER CONFIGURATION
# ==========================================

DEFAULT_MAX_PAGES = int(
    os.getenv("DEFAULT_MAX_PAGES", "50")
)

DEFAULT_MIN_PRICE = None

DEFAULT_MAX_PRICE = None

DEFAULT_RATING = None


# ==========================================
# LOGGING CONFIGURATION
# ==========================================

LOG_FILE = LOG_DIR / "scraper.log"

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO"
)