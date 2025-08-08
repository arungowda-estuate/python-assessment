from datetime import datetime
from typing import Dict, List

from src.functions.environment import setup_logger
from src.functions.helper import load_notes, save_notes

logger = setup_logger()


# Creating the notes
def create_note(title: str, content: str) -> int:
    notes = load_notes()
    next_id = max((n.get("id", 0) for n in notes), default=0) + 1
    ts = datetime.now().isoformat()
    note = {"id": next_id, "title": title, "content": content, "timestamp": ts}
    notes.append(note)
    save_notes(notes)
    logger.info("CREATE - note_id=%s", next_id)
    return next_id


# Reading the notes
def read_note(note_id: int) -> Dict:
    notes = load_notes()
    for n in notes:
        if n.get("id") == note_id:
            logger.info("READ - note_id=%s", note_id)
            return n
    logger.warning("READ FAILED - note_id=%s not found", note_id)
    raise KeyError(f"Note with ID {note_id} not found")


# Updating notes
def update_note(note_id: int, new_title: str, new_content: str) -> None:
    notes = load_notes()
    for n in notes:
        if n.get("id") == note_id:
            n["title"] = new_title
            n["content"] = new_content
            n["timestamp"] = datetime.now().isoformat()
            save_notes(notes)
            logger.info("UPDATE - note_id=%s", note_id)
            return
    logger.warning("UPDATE FAILED - note_id=%s not found", note_id)
    raise KeyError(f"Note with ID {note_id} not found")


# Delete notes
def delete_note(note_id: int) -> None:
    notes = load_notes()
    new_notes = [n for n in notes if n.get("id") != note_id]
    if len(new_notes) == len(notes):
        logger.warning("DELETE FAILED - note_id=%s not found", note_id)
        raise KeyError(f"Note with ID {note_id} not found")
    save_notes(new_notes)
    logger.info("DELETE - note_id=%s", note_id)


def list_notes() -> List[Dict]:
    notes = load_notes()
    logger.info("LIST - total=%s", len(notes))
    return notes
