"""Tests for the question scoring and retry behavior."""

import unittest

from campusflow.understanding_check import QUESTIONS, run_check, score_answers


class UnderstandingCheckTests(unittest.TestCase):
    def test_scores_six_correct_answers(self):
        self.assertEqual(score_answers([question[2] for question in QUESTIONS]), 6)

    def test_scores_incorrect_answers(self):
        self.assertEqual(score_answers(["A"] * 6), 1)

    def test_rejects_wrong_number_of_answers(self):
        with self.assertRaisesRegex(ValueError, "Exactly 6"):
            score_answers(["A"])

    def test_rejects_non_sequence_answer_input(self):
        with self.assertRaisesRegex(ValueError, "Exactly 6"):
            score_answers(None)

    def test_rejects_invalid_answer(self):
        with self.assertRaisesRegex(ValueError, "A, B, C, or D"):
            score_answers(["AB"] + ["A"] * 5)

    def test_prompt_retries_invalid_choice_and_requests_two_explanations(self):
        answers = iter(["X", *[question[2] for question in QUESTIONS], "why numeric", "avoid mutation"])
        prompts = []
        output = []
        score = run_check(lambda prompt: (prompts.append(prompt), next(answers))[1], output.append)

        self.assertEqual(score, 6)
        self.assertEqual(len(prompts), 9)
        self.assertIn("Enter A, B, C, or D.", output)
        self.assertTrue(any("Explain why the queue" in line for line in output))


if __name__ == "__main__":
    unittest.main()
