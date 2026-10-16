"""Tests for open ticket queues and summary reports."""

import unittest

from campusflow.reports import get_queue, get_report


class QueueTests(unittest.TestCase):
    def test_queue_sorts_by_priority_then_numeric_id_and_excludes_closed(self):
        tickets = [
            {"id": "T010", "status": "open", "priority": "high"},
            {"id": "T002", "status": "open", "priority": "critical"},
            {"id": "T003", "status": "resolved", "priority": "critical"},
            {"id": "T004", "status": "open", "priority": "high"},
            {"id": "T001", "status": "open", "priority": "high"},
        ]

        queue = get_queue(tickets)

        self.assertEqual(
            [(ticket["id"], ticket["priority"]) for ticket in queue],
            [("T002", "critical"), ("T001", "high"), ("T004", "high"), ("T010", "high")],
        )
        self.assertEqual(len(tickets), 5)

    def test_queue_is_a_new_list(self):
        tickets = [{"id": "T001", "status": "open", "priority": "low"}]

        self.assertIsNot(get_queue(tickets), tickets)


class ReportTests(unittest.TestCase):
    def test_report_counts_all_tickets_and_includes_zero_categories(self):
        tickets = [
            {"id": "T001", "status": "open", "priority": "high"},
            {"id": "T002", "status": "resolved", "priority": "low"},
            {"id": "T003", "status": "open", "priority": "high"},
        ]

        self.assertEqual(
            get_report(tickets),
            {
                "total": 3,
                "by_status": {"open": 2, "in_progress": 0, "resolved": 1},
                "by_priority": {"critical": 0, "high": 2, "medium": 0, "low": 1},
            },
        )

    def test_empty_report_has_every_category_at_zero(self):
        self.assertEqual(
            get_report([]),
            {
                "total": 0,
                "by_status": {"open": 0, "in_progress": 0, "resolved": 0},
                "by_priority": {"critical": 0, "high": 0, "medium": 0, "low": 0},
            },
        )


if __name__ == "__main__":
    unittest.main()
