"""Read-only ticket search with optional combined filters."""

CATEGORIES = ("Network", "Hardware", "Software", "Other")
STATUSES = ("open", "in_progress", "resolved")
PRIORITIES = ("critical", "high", "medium", "low")


def _optional_filter(value, allowed, name):
    """Normalize an optional enum filter or reject an unknown value."""
    if value is None or value == "":
        return None
    if not isinstance(value, str):
        raise ValueError(f"{name} filter must be text.")
    normalized = value.strip().casefold()
    if not normalized:
        return None
    for option in allowed:
        if option.casefold() == normalized:
            return option
    choices = ", ".join(allowed)
    raise ValueError(f"{name} filter must be one of: {choices}.")


def search_tickets(tickets, title="", category="", status="", priority=""):
    """Return matching tickets in numeric ID order without changing the input."""
    if title is None or title == "":
        title_fragment = ""
    elif isinstance(title, str):
        title_fragment = title.strip().casefold()
    else:
        raise ValueError("Title filter must be text.")

    category_filter = _optional_filter(category, CATEGORIES, "Category")
    status_filter = _optional_filter(status, STATUSES, "Status")
    priority_filter = _optional_filter(priority, PRIORITIES, "Priority")

    matches = []
    for ticket in tickets:
        if title_fragment and title_fragment not in ticket["title"].casefold():
            continue
        if category_filter and ticket["category"] != category_filter:
            continue
        if status_filter and ticket["status"] != status_filter:
            continue
        if priority_filter and ticket["priority"] != priority_filter:
            continue
        matches.append(ticket)

    return sorted(matches, key=_numeric_ticket_id)


def _numeric_ticket_id(ticket):
    """Return the number in an ID, so T2 sorts before T10."""
    digits = "".join(character for character in ticket["id"] if character.isdigit())
    if not digits:
        raise ValueError(f"ticket ID has no numeric portion: {ticket['id']!r}")
    return int(digits)
