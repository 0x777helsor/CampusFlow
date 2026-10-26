"""Six-question check of the documented CampusFlow rules."""


QUESTIONS = (
    ("What priority applies to high urgency with 10 affected users?",
     ("A. low", "B. medium", "C. high", "D. critical"), "D"),
    ("Which status must a ticket enter before it can be resolved?",
     ("A. open", "B. in_progress", "C. queued", "D. assigned"), "B"),
    ("What must be true before an open ticket can enter in_progress?",
     ("A. It has a note", "B. It is high priority", "C. It is assigned", "D. It is reopened"), "C"),
    ("Which tickets appear in the original open work queue?",
     ("A. Open tickets only", "B. All unresolved tickets", "C. Resolved tickets", "D. All tickets"), "A"),
    ("How are equal-priority queue tickets ordered?",
     ("A. Title alphabetically", "B. Numeric ticket ID", "C. Creation date", "D. Category"), "B"),
    ("What happens to resolution percentage for an empty collection?",
     ("A. It is 100%", "B. It is unavailable", "C. It is 0%", "D. It raises an error"), "C"),
)

EXPLANATION_PROMPTS = (
    "Explain why the queue uses numeric IDs to break priority ties.",
    "Explain why the CLI saves a pending copy before replacing active data.",
)


def score_answers(answers):
    """Score six submitted A/B/C/D answers, returning a number from 0 to 6."""
    if not isinstance(answers, (list, tuple)) or len(answers) != len(QUESTIONS):
        raise ValueError(f"Exactly {len(QUESTIONS)} answers are required.")
    normalized = []
    for answer in answers:
        if (not isinstance(answer, str)
                or answer.strip().upper() not in {"A", "B", "C", "D"}):
            raise ValueError("Answers must be A, B, C, or D.")
        normalized.append(answer.strip().upper())
    return sum(answer == question[2] for answer, question in zip(normalized, QUESTIONS))


def run_check(input_fn=None, output_fn=None):
    """Ask all questions, retry invalid choices, and invite two ungraded explanations."""
    if input_fn is None:
        input_fn = input
    if output_fn is None:
        output_fn = print
    answers = []
    for number, (prompt, options, _correct) in enumerate(QUESTIONS, start=1):
        while True:
            output_fn(f"\n{number}. {prompt}")
            for option in options:
                output_fn(f"  {option}")
            answer = input_fn("Answer (A/B/C/D): ").strip().upper()
            if answer in ("A", "B", "C", "D"):
                answers.append(answer)
                break
            output_fn("Enter A, B, C, or D.")

    score = score_answers(answers)
    output_fn(f"Score: {score}/{len(QUESTIONS)}")
    for prompt in EXPLANATION_PROMPTS:
        output_fn(prompt)
        input_fn("Your explanation: ")
    return score
