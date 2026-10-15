"""Ticket validation and priority rules."""


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
