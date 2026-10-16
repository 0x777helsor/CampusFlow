# AI Learning Log

Each fellow records at least three real interactions, including one suggestion independently corrected, improved, or rejected. Do not invent experiments, results, or understanding. Copy this template for each entry and fill it after doing the work.

## Fellow: KINGSLEY AMORIE

Two completed verified interactions are recorded below. One further interaction involving an independently corrected, improved, or rejected AI suggestion is still required.

### Interaction #1 — Lookup, return values, and loop placement

- Problem: Implement the agreed `get_ticket(tickets, ticket_id)` function.
- Initial understanding demonstrated in conversation: Kingsley predicted that a matching book lookup returns its title, that an unknown ID raises ValueError, and that raising inside the loop would stop the search before all entries were checked.
- Independent code attempt submitted by Kingsley:

  ```text
  def get_tick(tickets, ticket_id):    for ticket in tickets:        if ticket["id"] == tickets_id:        return tickets;    raise ValueError("Unknown book ID")
  ```

- AI feedback: A successful lookup returns the whole matching dictionary. Use `ticket_id` consistently, return `ticket` rather than the collection, indent the return inside the matching condition, and raise after the loop.
- Application: The corrected function was added to `campusflow/tickets.py`. AI added tests for finding a match after a non-match, rejecting unknown IDs without mutation, and searching an empty collection.
- Verification performed by AI: The full local feature-branch suite ran 43 tests successfully, including the three lookup tests. This is not a claim that Kingsley independently ran those tests.
- Independent verification by Kingsley: He ran `python3 -m unittest discover -s tests -p test_tickets.py -v` and shared the terminal output: `Ran 18 tests in 0.001s`, followed by `OK`. All three lookup tests passed, including finding a ticket after a non-matching entry and rejecting unknown IDs without changing the collection.
- Decision: Accepted the corrected return behavior because a lookup by ID should return the matching record rather than the whole collection.
- What Kingsley can explain in his own words: "A lookup by ID should return the matching ticket. return ticket immediately exits the function with that record. Returning tickets would give the caller the whole collection"
- Related implementation commit: `d7be621`; `campusflow/tickets.py` and `tests/test_tickets.py`.
- Critical-evaluation requirement: Still pending. This interaction records accepted AI guidance, not an independently corrected, improved, or rejected AI suggestion.

### Interaction #2 — Generating IDs when numbers have gaps

- Problem: Understand why new ticket IDs use the maximum existing numeric ID plus one rather than the ticket count plus one.
- Initial understanding: Not separately stated before the exercise; Kingsley correctly predicted that the two calculations would return 3 and 4 for existing IDs `[1, 3]`.
- AI exercise: Predict both results, then run `python3 -c 'ids = [1, 3]; print(len(ids) + 1, max(ids) + 1)'` and explain which result avoids a duplicate ID.
- Independent prediction and verification: Kingsley replied "3 and 4", then ran the command and shared terminal output `3 4`.
- Useful guidance: Computing a duplicate number does not itself raise ValueError; CampusFlow's storage validator rejects duplicate IDs when loading or saving. The next number should be 4 because 3 already exists.
- Decision: Accepted maximum-based allocation because the number of tickets does not identify the largest existing ID.
- What Kingsley can explain in his own words: "Because IDs can have gaps, the number of tickets doesn’t tell you the largest ID." He explained that `len(ids) + 1` gives the existing ID 3, whereas `max(ids) + 1` gives the unused ID 4, avoiding collisions after earlier IDs are deleted or skipped.
- Related file and commit: `campusflow/tickets.py`, `create_ticket()` in `d7be621`; the application also uses a default maximum of zero for an empty collection.
- Scope: This verifies allocation from the IDs currently present. Deleting tickets is not an implemented CampusFlow feature. This entry does not claim independently corrected or rejected AI advice.

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
