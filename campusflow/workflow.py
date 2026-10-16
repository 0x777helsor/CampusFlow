"""Ticket assignment and lifecycle operations."""

VALID_STATUSES = ("open", "in_progress", "resolved")


def assign_ticket(tickets, ticket_id, staff_name):
    """Assign a ticket to a staff member and return the updated ticket."""
    ticket = next((item for item in tickets if item["id"] == ticket_id), None)
    if ticket is None:
        raise ValueError(f"unknown ticket ID: {ticket_id!r}")
    if ticket["status"] == "resolved":
        raise ValueError(f"ticket {ticket_id} is resolved; reopen it first")
    if not isinstance(staff_name, str) or not staff_name.strip():
        raise ValueError("staff name must not be blank")

    ticket["assigned_to"] = staff_name.strip()
    return ticket


def change_status(tickets, ticket_id, new_status):
    """Move a ticket through the allowed lifecycle and return it."""
    ticket = next((item for item in tickets if item["id"] == ticket_id), None)
    if ticket is None:
        raise ValueError(f"unknown ticket ID: {ticket_id!r}")
    if new_status not in VALID_STATUSES:
        raise ValueError(f"invalid status: {new_status!r}")
    if ticket["status"] == "resolved":
        raise ValueError(f"ticket {ticket_id} is resolved; reopen it first")

    if ticket["status"] == "open" and new_status == "in_progress":
        if ticket["assigned_to"] is None:
            raise ValueError(f"ticket {ticket_id} must be assigned before it can start")
    elif ticket["status"] == "in_progress" and new_status == "resolved":
        pass
    else:
        raise ValueError(
            f"cannot move ticket {ticket_id} from {ticket['status']} to {new_status}"
        )

    ticket["status"] = new_status
    return ticket


def reopen_ticket(tickets, ticket_id):
    """Reopen a resolved ticket while retaining its assignment."""
    ticket = next((item for item in tickets if item["id"] == ticket_id), None)
    if ticket is None:
        raise ValueError(f"unknown ticket ID: {ticket_id!r}")
    if ticket["status"] != "resolved":
        raise ValueError(f"ticket {ticket_id} is not resolved")

    ticket["status"] = "open"
    return ticket
