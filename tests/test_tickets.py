"""Tests for ticket priority and input validation."""

import unittest

from campusflow.tickets import calculate_priority, create_ticket, get_ticket


class TicketCreationTests(unittest.TestCase):
    def test_creates_complete_normalized_ticket_and_appends_it(self):
        tickets = []

        ticket = create_ticket(tickets, "  Wi-Fi outage  ", " NETWORK ", " HIGH ", 12)

        self.assertEqual(ticket, {
            "id": "T001",
            "title": "Wi-Fi outage",
            "category": "Network",
            "urgency": "high",
            "affected_users": 12,
            "priority": "critical",
            "status": "open",
            "assigned_to": None,
        })
        self.assertEqual(len(tickets), 1)
        self.assertIs(tickets[0], ticket)

    def test_accepts_case_variations_for_every_category(self):
        for category in ("Network", "Hardware", "Software", "Other"):
            with self.subTest(category=category):
                ticket = create_ticket([], "Problem", category.swapcase(), "low", 1)
                self.assertEqual(ticket["category"], category)

    def test_uses_largest_numeric_id_in_unsorted_collection(self):
        tickets = [{"id": "T010"}, {"id": "T002"}, {"id": "T009"}]

        ticket = create_ticket(tickets, "Problem", "Other", "low", 1)

        self.assertEqual(ticket["id"], "T011")
        self.assertEqual([item["id"] for item in tickets],
                         ["T010", "T002", "T009", "T011"])

    def test_ids_expand_beyond_three_digits(self):
        tickets = [{"id": "T999"}]

        ticket = create_ticket(tickets, "Problem", "Other", "low", 1)

        self.assertEqual(ticket["id"], "T1000")

    def test_rejects_invalid_inputs_without_mutating_collection(self):
        invalid_inputs = [
            ("", "Network", "low", 1),
            ("   ", "Network", "low", 1),
            (None, "Network", "low", 1),
            (12, "Network", "low", 1),
            ("Problem", "", "low", 1),
            ("Problem", "Unknown", "low", 1),
            ("Problem", None, "low", 1),
            ("Problem", "Other", "urgent", 1),
            ("Problem", "Other", None, 1),
            ("Problem", "Other", "low", 0),
            ("Problem", "Other", "low", -1),
            ("Problem", "Other", "low", 1.5),
            ("Problem", "Other", "low", "3"),
            ("Problem", "Other", "low", True),
        ]
        for inputs in invalid_inputs:
            with self.subTest(inputs=inputs):
                tickets = [{"id": "T001", "title": "Existing problem"}]

                with self.assertRaises(ValueError):
                    create_ticket(tickets, *inputs)

                self.assertEqual(tickets,
                                 [{"id": "T001", "title": "Existing problem"}])

    def test_invalid_attempt_does_not_consume_an_id(self):
        tickets = []
        with self.assertRaises(ValueError):
            create_ticket(tickets, "", "Network", "high", 2)

        first = create_ticket(tickets, "Wi-Fi outage", "Network", "high", 2)
        second = create_ticket(tickets, "Broken laptop", "Hardware", "low", 1)

        self.assertEqual((first["id"], second["id"]), ("T001", "T002"))


class TicketLookupTests(unittest.TestCase):
    def test_finds_ticket_after_non_matching_ticket(self):
        first = {"id": "T001", "title": "Wi-Fi outage"}
        second = {"id": "T002", "title": "Broken laptop"}

        self.assertIs(get_ticket([first, second], "T002"), second)

    def test_unknown_id_raises_without_changing_tickets(self):
        tickets = [{"id": "T001", "title": "Wi-Fi outage"}]

        with self.assertRaisesRegex(ValueError, "Unknown ticket ID"):
            get_ticket(tickets, "T009")

        self.assertEqual(tickets, [{"id": "T001", "title": "Wi-Fi outage"}])

    def test_empty_collection_raises_value_error(self):
        with self.assertRaises(ValueError):
            get_ticket([], "T001")


class PriorityTests(unittest.TestCase):
    def test_medium_urgency_with_two_users_is_medium(self):
        self.assertEqual(calculate_priority("medium", 2), "medium")

    def test_high_urgency_becomes_critical_at_ten_users(self):
        self.assertEqual(calculate_priority("high", 9), "high")
        self.assertEqual(calculate_priority("high", 10), "critical")
        self.assertEqual(calculate_priority("high", 11), "critical")

    def test_user_count_becomes_high_at_ten_users(self):
        for urgency in ("low", "medium"):
            with self.subTest(urgency=urgency):
                self.assertEqual(calculate_priority(urgency, 9), "medium")
                self.assertEqual(calculate_priority(urgency, 10), "high")

    def test_low_urgency_becomes_medium_at_three_users(self):
        self.assertEqual(calculate_priority("low", 2), "low")
        self.assertEqual(calculate_priority("low", 3), "medium")

    def test_medium_urgency_with_one_user_is_medium(self):
        self.assertEqual(calculate_priority("medium", 1), "medium")

    def test_normalizes_urgency_case_and_whitespace(self):
        self.assertEqual(calculate_priority(" HIGH ", 10), "critical")
        self.assertEqual(calculate_priority("Medium", 1), "medium")
        self.assertEqual(calculate_priority("LOW", 1), "low")

    def test_rejects_unknown_or_non_string_urgency(self):
        for urgency in ("", "urgent", None, 1):
            with self.subTest(urgency=urgency):
                with self.assertRaises(ValueError):
                    calculate_priority(urgency, 1)

    def test_rejects_non_positive_user_count(self):
        for affected_users in (0, -1):
            with self.subTest(affected_users=affected_users):
                with self.assertRaises(ValueError):
                    calculate_priority("low", affected_users)

    def test_rejects_non_integer_user_count_including_booleans(self):
        for affected_users in (True, False, 1.5, "3", None):
            with self.subTest(affected_users=affected_users):
                with self.assertRaises(ValueError):
                    calculate_priority("low", affected_users)


if __name__ == "__main__":
    unittest.main()
