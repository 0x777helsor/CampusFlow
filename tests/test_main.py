"""Exercise the CLI with scripted input and isolated data files."""

from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from main import main
from campusflow.storage import load_tickets, save_tickets
from campusflow.tickets import create_ticket


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
        self.assertIn("Choose 1, 2, 3, or 0.", output)
        self.assertIn("No tickets yet.", output)

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
