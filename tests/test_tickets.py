"""Tests for ticket priority and input validation."""

import unittest

from campusflow.tickets import calculate_priority


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
