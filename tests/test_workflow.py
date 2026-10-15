import unittest

from campusflow.workflow import change_status


class ChangeStatusTests(unittest.TestCase):
    def test_unassigned_ticket_cannot_start_and_remains_open(self):
        ticket = {
            "id": "T001",
            "status": "open",
            "assigned_to": None,
        }

        with self.assertRaises(ValueError):
            change_status([ticket], "T001", "in_progress")

        self.assertEqual(ticket["status"], "open")


if __name__ == "__main__":
    unittest.main()
