import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Paths
DATA_DIR = Path("../data")
LOGS_DIR = Path("../logs")
NOTES_FILE = DATA_DIR / "notes.json"
LOG_FILE = LOGS_DIR / "app.log"


# Set up environment for this project
def setup_environment():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    if not NOTES_FILE.exists():
        NOTES_FILE.write_text("[]", encoding="utf-8")


# set up of logger method
def setup_logger() -> logging.Logger:
    logger = logging.getLogger("main")

    logger.setLevel(logging.INFO)
    if not logger.handlers:
        log_file_handler = RotatingFileHandler(LOG_FILE, maxBytes=1_000_000, backupCount=3, encoding="utf-8")
        log_file_handler.setLevel(logging.INFO)
        fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        log_file_handler.setFormatter(fmt)
        logger.addHandler(log_file_handler)

        sh = logging.StreamHandler()
        sh.setLevel(logging.WARNING)
        sh.setFormatter(fmt)
        logger.addHandler(sh)
    return logger
