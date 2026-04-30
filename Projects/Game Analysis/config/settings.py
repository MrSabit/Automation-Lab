import os
import yaml
from pathlib import Path


# Base project directory (root)
BASE_DIR = Path(__file__).resolve().parent.parent


# Path to YAML config
CONFIG_PATH = BASE_DIR / "config" / "sources.yaml"


def load_config():
    """Load YAML configuration file safely."""
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Config file not found: {CONFIG_PATH}")

    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


# Load config once at startup
CONFIG = load_config()


# ======================
# STEAM CONFIG
# ======================
STEAM_ENABLED = CONFIG["steam"]["enabled"]
STEAM_URL = CONFIG["steam"]["base_url"]
STEAM_DELAY = CONFIG["steam"]["limits"]["request_delay_seconds"]
STEAM_MAX_PAGES = CONFIG["steam"]["limits"]["max_pages"]
STEAM_HEADERS = CONFIG["steam"]["headers"]


# ======================
# ITCH CONFIG
# ======================
ITCH_ENABLED = CONFIG["itch"]["enabled"]
ITCH_URL = CONFIG["itch"]["base_url"]
ITCH_DELAY = CONFIG["itch"]["limits"]["request_delay_seconds"]
ITCH_MAX_PAGES = CONFIG["itch"]["limits"]["max_pages"]
ITCH_HEADERS = CONFIG["itch"]["headers"]


# ======================
# SCRAPING CONFIG
# ======================
RETRY_ATTEMPTS = CONFIG["scraping"]["retry_attempts"]
TIMEOUT = CONFIG["scraping"]["timeout_seconds"]
SAVE_RAW_DATA = CONFIG["scraping"]["save_raw_data"]


# ======================
# DATA STORAGE
# ======================
RAW_DATA_PATH = BASE_DIR / CONFIG["data_storage"]["raw_path"]
PROCESSED_DATA_PATH = BASE_DIR / CONFIG["data_storage"]["processed_path"]
EXPORT_FORMAT = CONFIG["data_storage"]["export_format"]


# ======================
# ANALYSIS
# ======================
GENERATE_CHARTS = CONFIG["analysis"]["generate_charts"]
OUTPUT_REPORTS = CONFIG["analysis"]["output_reports"]
REPORT_FORMAT = CONFIG["analysis"]["report_format"]


# ======================
# LOGGING
# ======================
LOG_LEVEL = CONFIG["logging"]["level"]
LOG_FILE = BASE_DIR / CONFIG["logging"]["log_file"]
SAVE_LOGS = CONFIG["logging"]["save_logs"]


# ======================
# OPTIONAL ENV SUPPORT (.env future-proofing)
# ======================
def get_env(key, default=None):
    return os.getenv(key, default)