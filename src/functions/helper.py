import json
from typing import List, Dict

from src.functions.environment import NOTES_FILE, setup_logger

logger = setup_logger()


# Additional for temporary file
def save_notes(notes: List[Dict]):
    tmp = NOTES_FILE.with_suffix(".tmp")
    try:
        with tmp.open("w", encoding="utf-8") as f:
            json.dump(notes, f, ensure_ascii=False, indent=2)
        tmp.replace(NOTES_FILE)
    except Exception:
        logger.exception("Failed to save notes to disk.")
        raise
