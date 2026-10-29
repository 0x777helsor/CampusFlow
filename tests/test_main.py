"""Exercise the CLI with scripted input and isolated data files."""

from contextlib import redirect_stdout
from copy import deepcopy
from io import StringIO
from pathlib import Path
import sys
import tempfile
from types import ModuleType
import unittest
from unittest.mock import patch

from main import main
from campusflow.storage import load_tickets, save_tickets
from campusflow.tickets import create_ticket
from campusflow.understanding_check import QUESTIONS


class CliTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "tickets.json"

    def run_cli(self, inputs):
        output = StringIO()
        with patch("builtins.input", side_effect=inputs), redirect_stdout(output):
            result = main(self.path)
        return result, output.getvalue()

    def test_create_list_view_and_exit_saves_normalized_ticket(self):
        result, output = self.run_cli([
            "1", " Wi-Fi outage ", " NETWORK ", " HIGH ", "12",
            "2", "3", " t001 ", "0",
        ])

        self.assertEqual(result, 0)
        self.assertIn("Created T001 with critical priority.", output)
        self.assertEqual(output.count("ID: T001"), 2)
        self.assertIn("Category: Network", output)
        self.assertIn("Affected users: 12", output)
        self.assertIn("Status: open", output)
        self.assertIn("Assigned to: Unassigned", output)
        self.assertEqual(load_tickets(self.path)[0]["title"], "Wi-Fi outage")

    def test_restart_loads_existing_tickets_and_creates_unique_id(self):
        self.run_cli(["1", "Wi-Fi outage", "Network", "high", "12", "0"])

        result, output = self.run_cli([
            "2", "1", "Broken laptop", "Hardware", "low", "1", "0",
        ])

        self.assertEqual(result, 0)
        self.assertIn("ID: T001", output)
        self.assertIn("Created T002", output)
        self.assertEqual([ticket["id"] for ticket in load_tickets(self.path)],
                         ["T001", "T002"])

    def test_invalid_user_counts_are_rejected_and_menu_continues(self):
        for count in ("1.5", "0", "-1", "abc"):
            with self.subTest(count=count):
                result, output = self.run_cli([
                    "1", "Wi-Fi outage", "Network", "low", count, "2", "0",
                ])
                self.assertEqual(result, 0)
                self.assertIn("Error:", output)
                self.assertIn("No tickets yet.", output)
                self.assertFalse(self.path.exists())

    def test_invalid_creation_preserves_existing_file(self):
        tickets = []
        create_ticket(tickets, "Existing problem", "Other", "low", 1)
        save_tickets(tickets, self.path)
        original = self.path.read_bytes()

        result, output = self.run_cli(["1", "   ", "Network", "high", "12", "0"])

        self.assertEqual(result, 0)
        self.assertIn("Title must not be blank", output)
        self.assertEqual(self.path.read_bytes(), original)

    def test_corrupted_file_stops_before_menu_and_preserves_data(self):
        self.path.write_bytes(b'{"unfinished":')
        original = self.path.read_bytes()

        result, output = self.run_cli([])

        self.assertEqual(result, 1)
        self.assertIn("Cannot start CampusFlow", output)
        self.assertNotIn("1. Create ticket", output)
        self.assertEqual(self.path.read_bytes(), original)

    def test_invalid_records_stop_before_menu(self):
        self.path.write_text('[{"id": "T001"}]', encoding="utf-8")

        result, output = self.run_cli([])

        self.assertEqual(result, 1)
        self.assertIn("eight required fields", output)
        self.assertNotIn("1. Create ticket", output)

    def test_startup_access_error_is_reported(self):
        with patch("main.load_tickets", side_effect=PermissionError("Access denied")):
            result, output = self.run_cli([])

        self.assertEqual(result, 1)
        self.assertIn("Access denied", output)

    def test_failed_save_does_not_add_ticket_or_consume_id(self):
        with patch("main.save_tickets", side_effect=[OSError("Disk full"), None]) as save:
            result, output = self.run_cli([
                "1", "First attempt", "Other", "low", "1", "2",
                "1", "Second attempt", "Other", "low", "1", "0",
            ])

        self.assertEqual(result, 0)
        self.assertIn("Disk full", output)
        self.assertIn("No tickets yet.", output)
        self.assertIn("Created T001", output)
        self.assertNotIn("Created T002", output)
        self.assertEqual(save.call_args_list[0].args[0][0]["title"], "First attempt")
        self.assertEqual(save.call_args_list[1].args[0][0]["title"], "Second attempt")

    def test_unknown_id_reports_error_then_accepts_next_choice(self):
        result, output = self.run_cli(["3", "T009", "0"])
        self.assertEqual(result, 0)
        self.assertIn("Unknown ticket ID", output)
        self.assertIn("Goodbye.", output)

    def test_invalid_choice_returns_to_menu(self):
        result, output = self.run_cli(["99", "2", "0"])
        self.assertEqual(result, 0)
        self.assertIn("Choose a number from 0 to 12.", output)
        self.assertIn("No tickets yet.", output)

    def test_workflow_menu_saves_lifecycle_and_retains_assignment_after_reopen(self):
        result, output = self.run_cli([
            "1", "Wi-Fi outage", "Network", "high", "12",
            "4", " t001 ", "  Kingsley Amorie  ",
            "5", "T001", " IN_PROGRESS ",
            "5", "T001", "resolved",
            "4", "T001", "Other staff",
            "6", "T001", "0",
        ])

        self.assertEqual(result, 0)
        self.assertIn("reopen it first", output)
        self.assertIn("Status: resolved", output)
        self.assertEqual(output.count("Updated T001."), 4)
        ticket = load_tickets(self.path)[0]
        self.assertEqual(ticket["status"], "open")
        self.assertEqual(ticket["assigned_to"], "Kingsley Amorie")

    def test_unassigned_progress_is_rejected_without_saving(self):
        tickets = []
        create_ticket(tickets, "Wi-Fi outage", "Network", "high", 12)
        save_tickets(tickets, self.path)
        original = self.path.read_bytes()

        result, output = self.run_cli(["5", "T001", "in_progress", "0"])

        self.assertEqual(result, 0)
        self.assertIn("must be assigned", output)
        self.assertEqual(self.path.read_bytes(), original)

    def test_queue_and_report_use_merged_functions(self):
        tickets = []
        for ticket_id, urgency, users, status in (
            ("T010", "high", 2, "open"),
            ("T002", "high", 12, "open"),
            ("T009", "high", 2, "open"),
            ("T004", "low", 4, "open"),
            ("T005", "low", 1, "open"),
            ("T003", "high", 12, "resolved"),
            ("T006", "high", 2, "in_progress"),
        ):
            ticket = create_ticket(tickets, "Problem", "Other", urgency, users)
            ticket["id"] = ticket_id
            ticket["status"] = status
            if status != "open":
                ticket["assigned_to"] = "Kingsley Amorie"
        save_tickets(tickets, self.path)

        result, output = self.run_cli(["7", "8", "0"])

        self.assertEqual(result, 0)
        displayed_ids = [line for line in output.splitlines() if line.startswith("ID:")]
        self.assertEqual(displayed_ids,
                         ["ID: T002", "ID: T009", "ID: T010", "ID: T004", "ID: T005"])
        for count in ("Total tickets: 7", "open: 5", "in_progress: 1", "resolved: 1",
                      "critical: 2", "high: 3", "medium: 1", "low: 1"):
            self.assertIn(count, output)

    def test_empty_queue_and_report_are_displayed(self):
        result, output = self.run_cli(["7", "8", "0"])

        self.assertEqual(result, 0)
        self.assertIn("No open tickets.", output)
        self.assertIn("Total tickets: 0", output)
        for category in ("open", "in_progress", "resolved", "critical", "high", "medium", "low"):
            self.assertIn(f"{category}: 0", output)
        self.assertFalse(self.path.exists())

    def test_search_menu_displays_empty_result_message(self):
        result, output = self.run_cli(["11", "wifi", "Network", "open", "critical", "0"])

        self.assertEqual(result, 0)
        self.assertIn("No matching tickets.", output)

    def test_search_menu_displays_matching_ticket(self):
        tickets = []
        create_ticket(tickets, "Wi-Fi outage", "Network", "high", 2)
        save_tickets(tickets, self.path)

        result, output = self.run_cli(["11", "wi-fi", "network", "open", "high", "0"])

        self.assertEqual(result, 0)
        self.assertIn("ID: T001", output)
        self.assertIn("Title: Wi-Fi outage", output)

    def test_note_menu_adds_and_views_note_through_business_api(self):
        ticket = {
            "id": "T001", "title": "Problem", "category": "Other", "urgency": "low",
            "affected_users": 1, "priority": "low", "status": "open",
            "assigned_to": None, "notes": [],
        }

        def fake_add_note(tickets, ticket_id, author, message):
            note = {"note_id": "N001", "author": author.strip(), "message": message.strip()}
            next(item for item in tickets if item["id"] == ticket_id)["notes"].append(note)
            return note

        def fake_get_notes(tickets, ticket_id):
            return deepcopy(next(item for item in tickets if item["id"] == ticket_id)["notes"])

        notes_module = ModuleType("campusflow.notes")
        notes_module.add_note = fake_add_note
        notes_module.get_notes = fake_get_notes
        output = StringIO()
        with patch("main.load_tickets", return_value=[ticket]), \
                patch("main.save_tickets") as save, \
                patch.dict(sys.modules, {"campusflow.notes": notes_module}), \
                patch("builtins.input", side_effect=[
                    "9", "T001", " Fabian ", "A useful note", "10", "T001", "0",
                ]), redirect_stdout(output):
            result = main(self.path)

        self.assertEqual(result, 0)
        self.assertEqual(save.call_args.args[0][0]["notes"][0]["note_id"], "N001")
        self.assertIn("Added note N001 to T001.", output.getvalue())
        self.assertIn("N001 | Fabian: A useful note", output.getvalue())

    def test_note_menu_reports_when_business_module_is_not_integrated(self):
        with patch.dict(sys.modules, {"campusflow.notes": None}):
            result, output = self.run_cli(["9", "0"])

        self.assertEqual(result, 0)
        self.assertIn("The notes business module is not integrated yet.", output)

    def test_understanding_check_is_reachable_from_menu(self):
        answers = [question[2] for question in QUESTIONS]
        result, output = self.run_cli(["12", *answers, "queue uses numeric order", "save copy protects memory", "0"])

        self.assertEqual(result, 0)
        self.assertIn("Score: 6/6", output)

    def test_failed_note_save_does_not_change_nested_active_notes(self):
        ticket = {
            "id": "T001", "title": "Problem", "category": "Other", "urgency": "low",
            "affected_users": 1, "priority": "low", "status": "open",
            "assigned_to": None, "notes": [],
        }

        def fake_add_note(tickets, ticket_id, author, message):
            note = {"note_id": "N001", "author": author.strip(), "message": message.strip()}
            next(item for item in tickets if item["id"] == ticket_id)["notes"].append(note)
            return note

        notes_module = ModuleType("campusflow.notes")
        notes_module.add_note = fake_add_note
        notes_module.get_notes = lambda tickets, ticket_id: deepcopy(
            next(item for item in tickets if item["id"] == ticket_id)["notes"]
        )
        original = deepcopy(ticket)
        output = StringIO()
        with patch("main.load_tickets", return_value=[ticket]), \
                patch("main.save_tickets", side_effect=OSError("Disk full")), \
                patch.dict(sys.modules, {"campusflow.notes": notes_module}), \
                patch("builtins.input", side_effect=["9", "T001", "Fabian", "A useful note", "2", "0"]), \
                redirect_stdout(output):
            result = main(self.path)

        self.assertEqual(result, 0)
        self.assertEqual(ticket, original)
        self.assertIn("Disk full", output.getvalue())
        self.assertNotIn("Added note", output.getvalue())

    def test_failed_workflow_save_preserves_active_and_stored_tickets(self):
        for choice, status, staff, arguments in (
            ("4", "open", None, ["Other staff"]),
            ("5", "open", "Kingsley Amorie", ["in_progress"]),
            ("6", "resolved", "Kingsley Amorie", []),
        ):
            with self.subTest(choice=choice):
                tickets = []
                ticket = create_ticket(tickets, "Problem", "Other", "low", 1)
                ticket["status"] = status
                ticket["assigned_to"] = staff
                save_tickets(tickets, self.path)
                original = self.path.read_bytes()

                with patch("main.save_tickets", side_effect=OSError("Disk full")):
                    result, output = self.run_cli([choice, "T001", *arguments, "2", "0"])

                self.assertEqual(result, 0)
                self.assertIn("Disk full", output)
                self.assertNotIn("Updated T001.", output)
                self.assertIn(f"Status: {status}", output)
                self.assertIn(f"Assigned to: {staff or 'Unassigned'}", output)
                self.assertEqual(self.path.read_bytes(), original)

    def test_invalid_workflow_requests_preserve_data(self):
        tickets = []
        create_ticket(tickets, "Problem", "Other", "low", 1)
        save_tickets(tickets, self.path)
        original = self.path.read_bytes()

        result, output = self.run_cli([
            "4", "T001", "   ", "5", "T001", "resolved",
            "6", "T001", "4", "T999", "Kingsley", "0",
        ])

        self.assertEqual(result, 0)
        self.assertIn("staff name must not be blank", output)
        self.assertIn("cannot move ticket", output)
        self.assertIn("is not resolved", output)
        self.assertIn("unknown ticket ID", output)
        self.assertEqual(self.path.read_bytes(), original)

    def test_end_of_input_and_keyboard_interrupt_exit_cleanly(self):
        for interruption in (EOFError, KeyboardInterrupt):
            with self.subTest(interruption=interruption):
                output = StringIO()
                with patch("builtins.input", side_effect=interruption):
                    with redirect_stdout(output):
                        result = main(self.path)
                self.assertEqual(result, 0)
                self.assertFalse(self.path.exists())


if __name__ == "__main__":
    unittest.main()
