"""Ticket lookup, validation, and priority rules."""


def get_ticket(tickets, ticket_id):
    """Return the matching ticket or raise ValueError for an unknown ID."""
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            return ticket
    raise ValueError(f"Unknown ticket ID: {ticket_id!r}")


def create_ticket(tickets, title, category, urgency, affected_users):
    """Validate inputs, append a new open ticket, and return it."""
    if not isinstance(title, str) or not title.strip():
        raise ValueError("Title must not be blank.")

    categories = ("Network", "Hardware", "Software", "Other")
    if not isinstance(category, str):
        raise ValueError("Category must be Network, Hardware, Software, or Other.")
    category = category.strip().capitalize()
    if category not in categories:
        raise ValueError("Category must be Network, Hardware, Software, or Other.")

    priority = calculate_priority(urgency, affected_users)
    next_number = max((int(ticket["id"][1:]) for ticket in tickets), default=0) + 1
    ticket = {
        "id": f"T{next_number:03d}",
        "title": title.strip(),
        "category": category,
        "urgency": urgency.strip().lower(),
        "affected_users": affected_users,
        "priority": priority,
        "status": "open",
        "assigned_to": None,
    }
    tickets.append(ticket)
    return ticket


def calculate_priority(urgency, affected_users):
    """Return the first matching priority after validating both inputs."""
    if not isinstance(urgency, str):
        raise ValueError("Urgency must be low, medium, or high.")
    urgency = urgency.strip().lower()
    if urgency not in ("low", "medium", "high"):
        raise ValueError("Urgency must be low, medium, or high.")

    if isinstance(affected_users, bool) or not isinstance(affected_users, int):
        raise ValueError("Affected users must be a positive integer.")
    if affected_users <= 0:
        raise ValueError("Affected users must be a positive integer.")

    if urgency == "high" and affected_users >= 10:
        return "critical"
    if urgency == "high" or affected_users >= 10:
        return "high"
    if urgency == "medium" or affected_users >= 3:
        return "medium"
    return "low"
