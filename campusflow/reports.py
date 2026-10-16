"""Queue ordering and summary reports for campus helpdesk tickets."""

STATUSES = ("open", "in_progress", "resolved")
PRIORITIES = ("critical", "high", "medium", "low")


def _numeric_ticket_id(ticket):
    """Return the integer portion of a ticket ID for tie breaking."""
    digits = "".join(character for character in ticket["id"] if character.isdigit())
    if not digits:
        raise ValueError(f"ticket ID has no numeric portion: {ticket['id']!r}")
    return int(digits)


def get_queue(tickets):
    """Return open tickets ordered by priority, then numeric ID."""
    priority_order = {priority: rank for rank, priority in enumerate(PRIORITIES)}
    queue = [ticket for ticket in tickets if ticket["status"] == "open"]
    return sorted(
        queue,
        key=lambda ticket: (priority_order[ticket["priority"]], _numeric_ticket_id(ticket)),
    )


def get_report(tickets):
    """Return total ticket count and counts for every status and priority."""
    by_status = {status: 0 for status in STATUSES}
    by_priority = {priority: 0 for priority in PRIORITIES}
    for ticket in tickets:
        by_status[ticket["status"]] += 1
        by_priority[ticket["priority"]] += 1

    return {
        "total": len(tickets),
        "by_status": by_status,
        "by_priority": by_priority,
    }
