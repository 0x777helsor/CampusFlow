# AI Learning Log

Each fellow records at least three real interactions, including one suggestion independently corrected, improved, or rejected. Do not invent experiments, results, or understanding. Copy this template for each entry and fill it after doing the work.

## Fellow: KINGSLEY AMORIE

No verified entries recorded yet.

## Fellow: FABIAN PAUL

### Interaction #1 — Sorting with tuple keys

- Problem: I did not know how to sort lists in Python.
- My initial understanding: I initially thought sorting tuples would rearrange the individual numbers rather than preserve each pair.
- Actual prompt to AI: "i don't know anything about sorting list in python yet"
- Useful AI guidance: sorted() creates a new list. A tuple key compares the first value first, then the second when the first values tie.
- My predictions before experiments: I predicted the sorted scores and unchanged original list correctly. After learning how tuple comparisons work, I predicted parcel orders [3, 8, 10] and, after changing parcel 8's rank to 0, [8, 3, 10].
- My independent experiment/test: I sorted numbers, pairs, and parcel dictionaries in the Python interpreter, using a function returning (rank, number).
- Verification source or actual result: Shared interpreter output showed sorted scores [10, 20, 30], unchanged original scores [30, 10, 20], sorted pairs [(1, 3), (1, 8), (2, 10)], and parcel orders [3, 8, 10] and [8, 3, 10].
- Decision: I accepted tuple-key sorting because the queue needs a well-defined order: rank first, then number to break ties. Tuple comparison provides this without a custom comparator.
- Related file/commit: Python interpreter experiment; no application file or project commit yet.
- What I can now explain in my own words: The key returns rank and number in that order. Python compares rank first and only compares number when ranks match. A smaller rank comes first regardless of the number.

### Interaction #2 — Testing with unittest

- Problem: Learn how to test returned values and expected exceptions.
- My initial understanding: I had a partial understanding of automated tests before this experiment.
- Actual prompt to AI: "how do i go about this?"
- Useful AI guidance: Test methods start with test_ inside a unittest.TestCase subclass. Assertions check actual outcomes against expected outcomes.
- My predictions before experiments: Expecting double(3) to equal 8 would fail because the result is 6. Expecting ValueError for require_positive(0) would pass; expecting it for require_positive(2) would fail.
- My independent experiment/test: I created /tmp/campusflow-fabian-practice/test_double.py, ran a deliberately incorrect assertion, corrected the expectation, and added an expected-exception test.
- Verification source or actual result:
  - Shared output showed AssertionError: 6 != 8 for the incorrect expectation.
  - After correcting the expectation to 6, shared output showed one passing test.
  - After adding the exception test, shared output showed two passing tests.
  - I confirmed in conversation that require_positive(2) caused the exception test to fail before restoring require_positive(0); I did not paste that intermediate failure output.
  - Final shared output: Ran 2 tests; OK.
- Decision: I accepted the testing approach after observing the assertions detect incorrect expectations and pass for the expected behavior.
- Related file: /tmp/campusflow-fabian-practice/test_double.py; practice file outside the repository, not a project commit.
- What I can now explain in my own words: assertEqual() checks that actual == expected. assertRaises() checks that the expected exception is raised.

These entries record verified learning; neither claims an independently corrected, improved, or rejected AI suggestion. That requirement remains for a later genuine interaction.

## Entry template

### Interaction #<number> — <topic>

- Fellow:
- Problem:
- My initial understanding:
- Actual prompt to AI:
- Useful AI guidance:
- My prediction before the experiment:
- My independent experiment/test:
- Verification source or actual result:
- Decision (accepted, improved, or rejected, and why):
- Related file, test, commit, or PR:
- What I can now explain in my own words:
