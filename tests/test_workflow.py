import unittest

from campusflow.workflow import (
    assign_ticket,
    change_status,
    reopen_ticket,
)


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

    def test_assigned_ticket_can_start_and_resolve(self):
        ticket = {"id": "T001", "status": "open", "assigned_to": "Ari"}

        self.assertIs(change_status([ticket], "T001", "in_progress"), ticket)
        self.assertIs(change_status([ticket], "T001", "resolved"), ticket)
        self.assertEqual(ticket["status"], "resolved")

    def test_cannot_skip_a_lifecycle_step(self):
        ticket = {"id": "T001", "status": "open", "assigned_to": "Ari"}

        with self.assertRaises(ValueError):
            change_status([ticket], "T001", "resolved")

        self.assertEqual(ticket["status"], "open")

    def test_assignment_trims_staff_name(self):
        ticket = {"id": "T001", "status": "open", "assigned_to": None}

        self.assertIs(assign_ticket([ticket], "T001", "  Ari  "), ticket)
        self.assertEqual(ticket["assigned_to"], "Ari")

    def test_assignment_rejects_blank_name_without_mutation(self):
        ticket = {"id": "T001", "status": "open", "assigned_to": None}

        with self.assertRaises(ValueError):
            assign_ticket([ticket], "T001", "  ")

        self.assertIsNone(ticket["assigned_to"])

    def test_resolved_ticket_must_be_reopened_before_assignment(self):
        ticket = {"id": "T001", "status": "resolved", "assigned_to": "Ari"}

        with self.assertRaises(ValueError):
            assign_ticket([ticket], "T001", "Bo")

        self.assertEqual(ticket["assigned_to"], "Ari")

    def test_reopen_resolved_ticket_retains_assignment(self):
        ticket = {"id": "T001", "status": "resolved", "assigned_to": "Ari"}

        self.assertIs(reopen_ticket([ticket], "T001"), ticket)
        self.assertEqual(ticket["status"], "open")
        self.assertEqual(ticket["assigned_to"], "Ari")

    def test_reopening_non_resolved_ticket_is_rejected(self):
        ticket = {"id": "T001", "status": "open", "assigned_to": None}

        with self.assertRaises(ValueError):
            reopen_ticket([ticket], "T001")

        self.assertEqual(ticket["status"], "open")

    def test_unknown_ticket_id_is_rejected(self):
        with self.assertRaises(ValueError):
            change_status([], "T404", "in_progress")


if __name__ == "__main__":
    unittest.main()
