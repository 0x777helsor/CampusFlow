# CampusFlow Next baseline

## Version and audit availability

- Date: 2026-10-20.
- Baseline: merged `main` at `0482c75` (PR #10). Original completed application reference: `6ef5ff8`; subsequent changes through this baseline are documentation.
- Environment: Python 3.12.3, standard library only.
- No external audit, audited commit, or mentor-selected priority focus has been supplied. Findings below are self-diagnostic observations, not confirmed peer-reported bugs.
- Execution attribution: AI ran the commands and scripted CLI checks below during Kingsley's session. These are not claims of independent manual execution by either engineer.

## Automated tests

Command: `python3 -m unittest discover -s tests -v`

Actual output summary:

```text
Ran 61 tests in 0.164s
OK
```

No failures or errors. Passing original tests do not establish coverage of the new Next requirements.

## Three CLI input checks

The actual `main(path)` function was exercised with `unittest.mock.patch` supplying `input()`, captured stdout, and a distinct JSON path inside `tempfile.TemporaryDirectory` for each case. Saved records were checked with `load_tickets(path)`. All runs returned exit code 0. No real ticket data was read or changed. For manual reproduction, use `python3 main.py` with a disposable checkout/data path; entering a ticket creates persistent data.

| Case | Input sequence, ending with exit | Expected | Actual |
| --- | --- | --- | --- |
| Priority boundary | `1`, `Router outage`, `network`, `high`, `10`, `0` | Critical, normalized category, open ticket | `Created T001 with critical priority.`; one saved open ticket |
| Invalid count | `1`, `Router outage`, `Network`, `high`, `0`, `0` | Friendly rejection, no ticket | `Error: Affected users must be a positive integer.`; zero records |
| Assignment guard | Create as case 1, then `5`, `T001`, `in_progress`, `0` | Reject start, retain open state | `Error: ticket T001 must be assigned before it can start`; one saved open ticket |

These are scripted CLI checks, not a replacement for the engineers' individual final demonstrations.

## Evidence-supported improvement work

- `storage.py` validates exactly eight ticket fields. Next needs a ninth field, `notes`, and documented compatibility with existing records. This is a new requirement, not a demonstrated original-version bug.
- `main.py:save_change` copies each dictionary. That is sufficient for current scalar fields, but would share a newly added nested notes list. Next must isolate pending note edits and test failed saves.
- Validation currently lives in tickets and storage, while workflow enforces transitions. Next requires agreed central helpers without introducing import cycles or inconsistent rules.
- Search, structured notes and the understanding check are new features. Reports need category counts, unresolved/resolved totals and resolution percentage. None is claimed to have passed this baseline.
- Existing tests cover assignment guards, resolved-ticket restrictions, malformed JSON, duplicate IDs and reload ID continuity. Extend these with full-collection unchanged-state checks and nested notes coverage rather than treating the rules as absent.

Next: both engineers agree revised contracts, create actual issues and feature branches, and complete learning cycles before independent implementation.
