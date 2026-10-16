"""Command-line interface for the CampusFlow helpdesk."""

from pathlib import Path

from campusflow.reports import get_queue, get_report
from campusflow.storage import load_tickets, save_tickets
from campusflow.tickets import create_ticket, get_ticket
from campusflow.workflow import assign_ticket, change_status, reopen_ticket


DATA_PATH = Path(__file__).resolve().parent / "data" / "tickets.json"
MENU = (
    "\nCampusFlow\n1. Create ticket\n2. List tickets\n3. View ticket"
    "\n4. Assign ticket\n5. Change status\n6. Reopen ticket"
    "\n7. Work queue\n8. Reports\n0. Exit"
)


def display_ticket(ticket):
    """Show all eight ticket fields."""
    print(f"\nID: {ticket['id']}")
    print(f"Title: {ticket['title']}")
    print(f"Category: {ticket['category']}")
    print(f"Urgency: {ticket['urgency']}")
    print(f"Affected users: {ticket['affected_users']}")
    print(f"Priority: {ticket['priority']}")
    print(f"Status: {ticket['status']}")
    print(f"Assigned to: {ticket['assigned_to'] or 'Unassigned'}")


def save_change(tickets, path, operation, *arguments):
    """Apply an operation to copies, save, then update the active collection."""
    pending_tickets = [ticket.copy() for ticket in tickets]
    ticket = operation(pending_tickets, *arguments)
    save_tickets(pending_tickets, path)
    tickets[:] = pending_tickets
    return ticket


def create_from_prompt(tickets, path):
    """Collect inputs and save before adding a ticket to the active collection."""
    title = input("Title: ")
    category = input("Category (Network/Hardware/Software/Other): ")
    urgency = input("Urgency (low/medium/high): ")
    try:
        affected_users = int(input("Affected users: ").strip())
    except ValueError as error:
        raise ValueError("Affected users must be a positive whole number.") from error

    ticket = save_change(
        tickets, path, create_ticket, title, category, urgency, affected_users,
    )
    print(f"Created {ticket['id']} with {ticket['priority']} priority.")


def update_from_prompt(tickets, path, choice):
    """Collect workflow inputs and persist the chosen update."""
    ticket_id = input("Ticket ID: ").strip().upper()
    if choice == "4":
        staff_name = input("Staff name: ")
        ticket = save_change(tickets, path, assign_ticket, ticket_id, staff_name)
    elif choice == "5":
        status = input("New status (in_progress/resolved): ").strip().lower()
        ticket = save_change(tickets, path, change_status, ticket_id, status)
    else:
        ticket = save_change(tickets, path, reopen_ticket, ticket_id)
    print(f"Updated {ticket['id']}.")
    display_ticket(ticket)


def display_collection(tickets, empty_message="No tickets yet."):
    """Display all supplied records or a useful message for an empty list."""
    if not tickets:
        print(empty_message)
    for ticket in tickets:
        display_ticket(ticket)


def display_report(tickets):
    """Display totals from the agreed report structure."""
    report = get_report(tickets)
    print(f"Total tickets: {report['total']}")
    print("By status:")
    for status, count in report["by_status"].items():
        print(f"  {status}: {count}")
    print("By priority:")
    for priority, count in report["by_priority"].items():
        print(f"  {priority}: {count}")


def main(path=DATA_PATH):
    """Run until exit; refuse to start when stored data cannot be loaded."""
    try:
        tickets = load_tickets(path)
    except (ValueError, OSError) as error:
        print(f"Cannot start CampusFlow: {error}")
        return 1

    while True:
        try:
            print(MENU)
            choice = input("Choose an option: ").strip()
            if choice == "0":
                print("Goodbye.")
                return 0
            if choice == "1":
                create_from_prompt(tickets, path)
            elif choice == "2":
                display_collection(tickets)
            elif choice == "3":
                ticket_id = input("Ticket ID: ").strip().upper()
                display_ticket(get_ticket(tickets, ticket_id))
            elif choice in ("4", "5", "6"):
                update_from_prompt(tickets, path, choice)
            elif choice == "7":
                display_collection(get_queue(tickets), "No open tickets.")
            elif choice == "8":
                display_report(tickets)
            else:
                print("Choose a number from 0 to 8.")
        except (ValueError, OSError) as error:
            print(f"Error: {error}")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            return 0


if __name__ == "__main__":
    raise SystemExit(main())
