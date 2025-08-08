import json
from datetime import datetime
from typing import List, Dict

from src.functions.environment import NOTES_FILE, setup_logger

logger = setup_logger()


# Loading all notes from the json file
def load_notes() -> List[Dict]:
    try:
        with NOTES_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("notes.json root is not a list")
            return data
    except FileNotFoundError:
        logger.warning("notes.json not found; creating a new empty list.")
        NOTES_FILE.write_text("[]", encoding="utf-8")
        return []
    # Additional Handler
    except json.JSONDecodeError:
        logger.exception("Failed to parse notes.json — backing it up and resetting.")
        # Backup corrupt file and start fresh
        ts = datetime.now().strftime("%Y%m%d%H%M%S")
        backup = NOTES_FILE.with_name(f"{NOTES_FILE.name}.corrupt.{ts}")
        try:
            NOTES_FILE.rename(backup)
            logger.info(f"Backed up corrupt notes.json to {backup}")
        except Exception:
            logger.exception("Failed to backup corrupt notes.json.")
        NOTES_FILE.write_text("[]", encoding="utf-8")
        return []
    except Exception:
        logger.exception("Unexpected error reading notes.json")
        return []


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
