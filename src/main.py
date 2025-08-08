from typing import Optional

from src.functions.crud_operations import create_note, read_note, update_note, delete_note, list_notes
from src.functions.environment import setup_environment, setup_logger

setup_environment()
logger = setup_logger()


def _get_int(prompt: str) -> Optional[int]:
    s = input(prompt).strip()
    if not s:
        return None
    try:
        return int(s)
    except ValueError:
        print("Please enter a valid integer.")
        return None


def menu():
    menu = """
=== Personal Notes Manager ===
1. Create Note
2. Read Note
3. Update Note
4. Delete Note
5. List All Notes
6. Exit
"""

    while True:
        print(menu)
        choice = input("Enter your choice (1-6): ").strip()
        if choice == "1":
            title = input("Enter title: ").strip()
            content = input("Enter content: ").strip()
            try:
                nid = create_note(title, content)
                print(f"Note created successfully with ID: {nid}")
            except Exception:
                print("Failed to create note. See logs for details.")
        elif choice == "2":
            nid = _get_int("Enter note ID: ")
            if nid is None:
                continue
            try:
                n = read_note(nid)
                print("\nID:", n["id"])
                print("Title:", n["title"])
                print("Content:", n["content"])
                print("Timestamp:", n["timestamp"], "\n")
            except KeyError as e:
                print(e)
            except Exception:
                print("Error reading note. See logs.")
        elif choice == "3":
            nid = _get_int("Enter note ID: ")
            if nid is None:
                continue
            new_title = input("Enter new title: ").strip()
            new_content = input("Enter new content: ").strip()
            try:
                update_note(nid, new_title, new_content)
                print(f"Note with ID {nid} updated successfully.")
            except KeyError as e:
                print(e)
            except Exception:
                print("Error updating note. See logs.")
        elif choice == "4":
            nid = _get_int("Enter note ID: ")
            if nid is None:
                continue
            confirm = input(f"Are you sure you want to delete note {nid}? (Y/N): ").strip().lower()
            if confirm != "y":
                print("Delete cancelled.")
                continue
            try:
                delete_note(nid)
                print(f"Note with ID {nid} deleted successfully.")
            except KeyError as e:
                print(e)
            except Exception:
                print("Error deleting note. See logs.")
        elif choice == "5":
            notes = list_notes()
            if not notes:
                print("No notes found.")
            else:
                for n in notes:
                    print("ID:", n["id"])
                    print("Title:", n["title"])
                    print("Content:", n["content"])
                    print("Timestamp:", n["timestamp"])
                    print("-" * 30)
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Please choose a valid option (1-6).")


if __name__ == "__main__":
    menu()
