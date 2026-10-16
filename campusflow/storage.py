"""Validate, load, and safely save JSON ticket collections."""

import json
import os
from pathlib import Path
import re
import tempfile

from campusflow.tickets import calculate_priority


TICKET_FIELDS = {
    "id", "title", "category", "urgency", "affected_users",
    "priority", "status", "assigned_to",
}


def _validate_ticket(ticket):
    """Check one stored record and return its numeric ID."""
    if not isinstance(ticket, dict) or set(ticket) != TICKET_FIELDS:
        raise ValueError("Each ticket must contain exactly the eight required fields.")

    ticket_id = ticket["id"]
    if not isinstance(ticket_id, str) or not re.fullmatch(r"T[0-9]{3,}", ticket_id):
        raise ValueError("Ticket IDs must have the form T001, T002, ...")
    number = int(ticket_id[1:])
    if number < 1 or ticket_id != f"T{number:03d}":
        raise ValueError(f"Invalid ticket ID: {ticket_id!r}")

    title = ticket["title"]
    if not isinstance(title, str) or not title.strip() or title != title.strip():
        raise ValueError(f"Ticket {ticket_id} must have a trimmed, non-empty title.")
    if ticket["category"] not in ("Network", "Hardware", "Software", "Other"):
        raise ValueError(f"Ticket {ticket_id} has an invalid category.")
    if ticket["urgency"] not in ("low", "medium", "high"):
        raise ValueError(f"Ticket {ticket_id} has an invalid urgency.")
    priority = calculate_priority(ticket["urgency"], ticket["affected_users"])
    if ticket["priority"] != priority:
        raise ValueError(f"Ticket {ticket_id} has an inconsistent priority.")
    if ticket["status"] not in ("open", "in_progress", "resolved"):
        raise ValueError(f"Ticket {ticket_id} has an invalid status.")

    staff_name = ticket["assigned_to"]
    if staff_name is not None:
        if (not isinstance(staff_name, str) or not staff_name.strip()
                or staff_name != staff_name.strip()):
            raise ValueError(f"Ticket {ticket_id} has an invalid staff name.")
    if ticket["status"] != "open" and staff_name is None:
        raise ValueError(f"Ticket {ticket_id} must be assigned before progressing.")
    return number


def _validate_tickets(tickets):
    """Reject invalid collections and duplicate IDs without changing records."""
    if not isinstance(tickets, list):
        raise ValueError("Ticket data must be a JSON list.")
    seen_ids = set()
    for ticket in tickets:
        number = _validate_ticket(ticket)
        if number in seen_ids:
            raise ValueError(f"Duplicate ticket ID: {ticket['id']}")
        seen_ids.add(number)


def load_tickets(path):
    """Return validated tickets, or an empty list when the file is missing."""
    path = Path(path)
    try:
        with path.open("r", encoding="utf-8") as source:
            tickets = json.load(source)
    except FileNotFoundError:
        return []
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        raise ValueError(f"Cannot load tickets from {path}: invalid JSON ({error}).") from error

    try:
        _validate_tickets(tickets)
    except ValueError as error:
        raise ValueError(f"Cannot load tickets from {path}: {error}") from error
    return tickets


def save_tickets(tickets, path):
    """Validate and replace the destination only after writing successfully."""
    _validate_tickets(tickets)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent,
            prefix=f".{path.name}.", suffix=".tmp", delete=False,
        ) as destination:
            temporary_path = Path(destination.name)
            json.dump(tickets, destination, indent=2, ensure_ascii=False, allow_nan=False)
            destination.write("\n")
            destination.flush()
            os.fsync(destination.fileno())
        os.replace(temporary_path, path)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
