"""Command-line interface for Kingsley's ticket and storage features."""

from pathlib import Path

from campusflow.storage import load_tickets, save_tickets
from campusflow.tickets import create_ticket, get_ticket


DATA_PATH = Path(__file__).resolve().parent / "data" / "tickets.json"
MENU = "\nCampusFlow\n1. Create ticket\n2. List tickets\n3. View ticket\n0. Exit"


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


def create_from_prompt(tickets, path):
    """Collect inputs and save before adding a ticket to the active collection."""
    title = input("Title: ")
    category = input("Category (Network/Hardware/Software/Other): ")
    urgency = input("Urgency (low/medium/high): ")
    try:
        affected_users = int(input("Affected users: ").strip())
    except ValueError as error:
        raise ValueError("Affected users must be a positive whole number.") from error

    pending_tickets = tickets.copy()
    ticket = create_ticket(pending_tickets, title, category, urgency, affected_users)
    save_tickets(pending_tickets, path)
    tickets.append(ticket)
    print(f"Created {ticket['id']} with {ticket['priority']} priority.")


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
                if not tickets:
                    print("No tickets yet.")
                for ticket in tickets:
                    display_ticket(ticket)
            elif choice == "3":
                ticket_id = input("Ticket ID: ").strip().upper()
                display_ticket(get_ticket(tickets, ticket_id))
            else:
                print("Choose 1, 2, 3, or 0.")
        except (ValueError, OSError) as error:
            print(f"Error: {error}")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            return 0


if __name__ == "__main__":
    raise SystemExit(main())
