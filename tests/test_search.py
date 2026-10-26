"""Tests for combined, read-only ticket search."""

import unittest

from campusflow.search import search_tickets


class TicketSearchTests(unittest.TestCase):
    def setUp(self):
        self.tickets = [
            {"id": "T010", "title": "Wi-Fi in Library", "category": "Network",
             "status": "open", "priority": "high"},
            {"id": "T002", "title": "Wi-Fi in Lab", "category": "Network",
             "status": "in_progress", "priority": "high"},
            {"id": "T003", "title": "Library projector", "category": "Hardware",
             "status": "open", "priority": "medium"},
        ]

    def test_combines_all_filters_with_and_and_casefolds_title(self):
        matches = search_tickets(
            self.tickets, title=" wi-fi ", category="network",
            status="OPEN", priority="HIGH",
        )
        self.assertEqual([ticket["id"] for ticket in matches], ["T010"])

    def test_default_search_orders_by_numeric_id(self):
        self.assertEqual(
            [ticket["id"] for ticket in search_tickets(self.tickets)],
            ["T002", "T003", "T010"],
        )

    def test_blank_filters_do_not_filter_results(self):
        self.assertEqual(len(search_tickets(self.tickets, " ", "", None, "  ")), 3)

    def test_unknown_filter_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Category filter"):
            search_tickets(self.tickets, category="Facilities")

    def test_search_returns_new_list_and_does_not_change_tickets(self):
        original = [ticket.copy() for ticket in self.tickets]
        results = search_tickets(self.tickets, status="open")
        self.assertIsNot(results, self.tickets)
        self.assertEqual(self.tickets, original)


if __name__ == "__main__":
    unittest.main()
