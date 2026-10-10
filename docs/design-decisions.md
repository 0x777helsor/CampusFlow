# Design Decisions

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
