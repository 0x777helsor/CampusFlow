"""Tests for persistence, invalid records, and safe replacement."""

import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from campusflow.storage import load_tickets, save_tickets
from campusflow.tickets import create_ticket


class StorageTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "tickets.json"
        self.tickets = []
        create_ticket(self.tickets, "Wi-Fi café outage", "Network", "high", 12)

    def test_missing_file_returns_empty_list_without_creating_file(self):
        self.assertEqual(load_tickets(self.path), [])
        self.assertFalse(self.path.exists())

    def test_round_trip_preserves_all_fields_and_assignment(self):
        self.tickets[0]["status"] = "in_progress"
        self.tickets[0]["assigned_to"] = "Kingsley Amorie"

        self.assertIsNone(save_tickets(self.tickets, self.path))

        self.assertEqual(load_tickets(self.path), self.tickets)
        self.assertEqual(json.loads(self.path.read_text(encoding="utf-8")), self.tickets)

    def test_empty_collection_round_trip(self):
        save_tickets([], str(self.path))
        self.assertEqual(load_tickets(str(self.path)), [])

    def test_save_creates_missing_parent_directories(self):
        path = self.path.parent / "data" / "tickets.json"
        save_tickets(self.tickets, path)
        self.assertEqual(load_tickets(path), self.tickets)

    def test_malformed_json_raises_and_preserves_original_bytes(self):
        original = b'{"unfinished":'
        self.path.write_bytes(original)

        with self.assertRaisesRegex(ValueError, "invalid JSON"):
            load_tickets(self.path)

        self.assertEqual(self.path.read_bytes(), original)

    def test_invalid_utf8_raises_and_preserves_original_bytes(self):
        self.path.write_bytes(b"\xff")
        with self.assertRaisesRegex(ValueError, "invalid JSON"):
            load_tickets(self.path)
        self.assertEqual(self.path.read_bytes(), b"\xff")

    def test_invalid_collection_shapes_are_rejected_without_rewriting(self):
        for value in ({}, None, "tickets", 3, [None], [{}]):
            with self.subTest(value=value):
                original = json.dumps(value)
                self.path.write_text(original, encoding="utf-8")

                with self.assertRaises(ValueError):
                    load_tickets(self.path)

                self.assertEqual(self.path.read_text(encoding="utf-8"), original)

    def test_invalid_ticket_fields_are_rejected(self):
        changes = [
            {"id": "T000"}, {"id": "T01"}, {"id": "T0001"},
            {"id": 1}, {"id": "X001"}, {"title": "   "}, {"title": None},
            {"category": "Unknown"}, {"urgency": "urgent"},
            {"affected_users": 0}, {"affected_users": True},
            {"affected_users": 1.5}, {"affected_users": "12"},
            {"priority": "low"}, {"status": "closed"},
            {"assigned_to": "   "}, {"assigned_to": 12},
            {"status": "in_progress", "assigned_to": None},
            {"status": "resolved", "assigned_to": None},
        ]
        for change in changes:
            with self.subTest(change=change):
                ticket = dict(self.tickets[0], **change)
                self.path.write_text(json.dumps([ticket]), encoding="utf-8")
                with self.assertRaises(ValueError):
                    load_tickets(self.path)

    def test_duplicate_ids_are_rejected(self):
        self.path.write_text(json.dumps(self.tickets * 2), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Duplicate ticket ID"):
            load_tickets(self.path)

    def test_creation_after_reload_uses_largest_existing_id(self):
        self.tickets[0]["id"] = "T010"
        second = dict(self.tickets[0], id="T002")
        self.tickets.append(second)
        save_tickets(self.tickets, self.path)

        loaded = load_tickets(self.path)
        new_ticket = create_ticket(loaded, "Broken keyboard", "Hardware", "low", 1)
        save_tickets(loaded, self.path)

        self.assertEqual(new_ticket["id"], "T011")
        self.assertEqual([ticket["id"] for ticket in load_tickets(self.path)],
                         ["T010", "T002", "T011"])

    def test_invalid_save_leaves_existing_file_unchanged(self):
        save_tickets(self.tickets, self.path)
        original = self.path.read_bytes()

        with self.assertRaises(ValueError):
            save_tickets([{}], self.path)

        self.assertEqual(self.path.read_bytes(), original)

    def test_partial_write_failure_preserves_existing_file(self):
        save_tickets(self.tickets, self.path)
        original = self.path.read_bytes()

        def fail_during_write(tickets, destination, **kwargs):
            destination.write("[")
            raise OSError("Disk full")

        with patch("campusflow.storage.json.dump", side_effect=fail_during_write):
            with self.assertRaisesRegex(OSError, "Disk full"):
                save_tickets(self.tickets, self.path)

        self.assertEqual(self.path.read_bytes(), original)
        self.assertEqual(list(self.path.parent.iterdir()), [self.path])

    def test_failed_replacement_preserves_existing_file(self):
        save_tickets(self.tickets, self.path)
        original = self.path.read_bytes()

        with patch("campusflow.storage.os.replace", side_effect=OSError("Cannot replace")):
            with self.assertRaisesRegex(OSError, "Cannot replace"):
                save_tickets([], self.path)

        self.assertEqual(self.path.read_bytes(), original)
        self.assertEqual(list(self.path.parent.iterdir()), [self.path])


if __name__ == "__main__":
    unittest.main()
