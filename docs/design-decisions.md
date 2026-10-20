# Design Decisions

## CampusFlow Next proposal — pending both engineers' agreement

Prepared during Kingsley's session on 2026-10-20. This section is a proposal, not approval from Kingsley or Fabian. Review it together before implementing shared interfaces. The historical agreement follows below.

Keep `ValueError` for invalid data/actions and propagate `OSError` for filesystem failures. Business functions do no input/printing. Reject before mutation; a failure preserves the complete collection, including nested notes. Retain current public signatures unless explicitly extended below.

| Owner/module | Proposed API | Return and side effects |
| --- | --- | --- |
| A / validation | `validate_ticket(ticket)`, `validate_tickets(tickets)` | `None` on success, `ValueError` on invalid canonical Next records; read-only; collection validation rejects duplicate ticket IDs |
| A / validation | `normalize_category(value)`, `normalize_urgency(value)`, `validate_affected_users(value)` | Canonical category, canonical urgency, or positive integer respectively; reject invalid types including bool counts |
| A / tickets | `next_ticket_id(tickets)` | Next canonical T ID from maximum numeric ID + 1; empty gives T001; no mutation |
| A / tickets | Existing `create_ticket(...)` | Append/return validated ticket with independent `notes: []` |
| A / notes | `next_note_id(ticket)` | Next canonical N ID from maximum existing per-ticket number + 1; empty gives N001; no mutation |
| A / notes | `add_note(tickets, ticket_id, author, message)` | Append/return note dictionary after validation; only open/in_progress; trimmed author nonblank and message length 5–300 |
| A / notes | `get_notes(tickets, ticket_id)` | New list of copied note dictionaries ordered by numeric note ID; unknown ticket raises ValueError |
| A / storage | Existing `load_tickets(path)` | Return fully validated new collection; missing file gives []; no active-memory argument or mutation |
| A / storage | `reload_tickets(tickets, path)` | Load/validate first, then replace `tickets[:]`; return None; failed load leaves memory unchanged |
| A / storage | Existing `save_tickets(tickets, path)` | Validate and atomically replace JSON only on successful write; return None |

Proposed schema compatibility: keep the JSON list format. On load only, accept valid original eight-field records by copying and adding empty notes, then validate the entire converted collection. Reject other missing/extra fields and malformed notes. Do not rewrite the source merely by loading. Subsequent explicit saves write all nine fields. Permit mixed legacy/Next records during conversion; document this behavior and test that failed conversion changes neither file nor active memory. Canonical IDs retain the existing minimum-three-digit format and expand beyond 999; note IDs follow the same rule with N. Notes have exactly `note_id`, `author`, `message`, unique IDs within each ticket.

Validation helpers must not import modules that import them. Agree placement of priority calculation/helper dependencies before refactoring; preserve exact precedence and public `calculate_priority` behavior.

B coordination proposal: CLI uses `copy.deepcopy(tickets)` for pending changes before calling A's mutating APIs and saving. Update active memory only after save succeeds. The return value of `add_note` is a note, unlike workflow functions returning tickets; the CLI should handle this explicitly.

B-owned contracts to confirm/propose: `search_tickets(tickets, title="", category="", status="", priority="")` returns a new read-only result list, combining supplied filters with AND, normalized valid enum filters and casefold title matching; default numeric ID order. A separate optional priority ordering must not alter `get_queue`. Report proposal retains `total`, `by_status`, `by_priority` and adds `by_category`, `unresolved`, `resolved`, `resolution_percentage` (float, 0.0 for empty input; round only for display). Fabian owns the final search/report/quiz interface proposals and their tests; these signatures are discussion inputs, not implementation instructions accepted on his behalf.

Agreement record: Kingsley confirmation pending; Fabian confirmation pending. Actual issue numbers and feature branches pending.

CampusFlow Next: the agreement below is the original-version baseline. Current roles and pending Next contract decisions are in `campusflow-next-handoff.md`. Next ownership supersedes the original ownership below; no revised function/schema contract has yet been agreed. Preserve this history and record the next agreement explicitly before application coding.

Status: agreed without changes by KINGSLEY AMORIE and FABIAN PAUL, as confirmed by Kingsley on 2026-10-11.

## Ownership

- KINGSLEY AMORIE: Issue #1, branch `feat/1-tickets-storage-cli`; `main.py`, `campusflow/tickets.py`, `campusflow/storage.py`, `tests/test_tickets.py`, and `tests/test_storage.py`.
- FABIAN PAUL: Issue #2, branch `feat/2-workflow-reports`; `campusflow/workflow.py`, `campusflow/reports.py`, `tests/test_workflow.py`, and `tests/test_reports.py`.
- Both: interface agreement, individual AI learning evidence, partner reviews, and final integration checks.

Ownership coordinates edits; it does not prevent partner review or suggestions. Discuss changes to a partner's files first.

## Agreed data and errors

`main.py` loads a list of ticket dictionaries and passes it to functions. Each dictionary has the assessment's eight fields: id, title, category, urgency, affected_users, priority, status, assigned_to.

Use canonical category names, lowercase urgency/status/priority, and trimmed non-empty titles/staff names. Reject booleans as affected-user counts, even though Python treats bool as an integer subclass. CLI conversion must reject decimal strings rather than truncate them.

Business functions raise `ValueError` for invalid input, unknown IDs, or forbidden transitions. Validate before mutation. The CLI catches expected errors and displays useful messages. Business functions do not call input() or print().

## Agreed function contracts

| Module | Function | Result |
| --- | --- | --- |
| tickets | `calculate_priority(urgency, affected_users)` | Priority string after validation |
| tickets | `create_ticket(tickets, title, category, urgency, affected_users)` | Append and return a new ticket |
| tickets | `get_ticket(tickets, ticket_id)` | Matching ticket or ValueError |
| workflow | `assign_ticket(tickets, ticket_id, staff_name)` | Update and return ticket |
| workflow | `change_status(tickets, ticket_id, new_status)` | Update and return ticket |
| workflow | `reopen_ticket(tickets, ticket_id)` | Resolved ticket becomes open; return ticket |
| reports | `get_queue(tickets)` | New ordered list containing only open tickets |
| reports | `get_report(tickets)` | Dictionary containing total, by_status, by_priority |
| storage | `load_tickets(path)` | List of tickets; missing file returns [] |
| storage | `save_tickets(tickets, path)` | Save list as JSON; return None |

Listing all tickets needs no additional function: main.py can display the collection. Reports include every allowed status and priority with zero counts when absent.

## Agreed lifecycle and persistence

Allow only open → in_progress → resolved through change_status. Reject modifications to resolved tickets except reopen_ticket. Reopening retains assignment. Queue ties use the integer portion of the ID, not string order.

New IDs use the maximum existing numeric ID plus one, formatted with at least three digits. Loading malformed JSON or invalid ticket records raises a clear error; the CLI must not continue with an empty collection and overwrite the file. Reject duplicate IDs on load. Save after successful mutations; handle storage errors visibly. Prefer writing to a temporary file in the same directory and replacing the destination after a successful write.

## Agreement

Both fellows agreed to the signatures, mutation behavior, error policy, report shape, reopening behavior, and ownership without changes. Discuss future interface changes together before implementing them.
