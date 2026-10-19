# CampusFlow

A Python command-line helpdesk for campus technical support, built by two fellows during an AI-assisted engineering sprint.

## Team and responsibilities

| Fellow | Issue | Branch | Responsibility |
| --- | --- | --- | --- |
| KINGSLEY AMORIE | #1 | `feat/1-tickets-storage-cli` | Ticket creation, validation, priority, list/view, JSON storage, CLI menu, and matching tests |
| FABIAN PAUL (`paulfabian-338-art`) | #2 | `feat/2-workflow-reports` | Assignment, lifecycle, reopening, queue, reports, and matching tests |

Kingsley owns changes to `main.py`; both fellows review code and agree on shared interfaces.

## Setup

Use Python 3.10 or newer and its standard library. No third-party packages or API keys are required.

```bash
python --version
python -m venv .venv
```

Activate with `source .venv/bin/activate` on Linux/macOS or `.venv\Scripts\Activate.ps1` in Windows PowerShell.

## Run and test

Run the current CLI and tests:

```bash
python main.py
python -m unittest discover -s tests -v
```

If your system provides `python3` instead of `python`, use `python3` in these commands.

The menu offers `1` create, `2` list, `3` view by ID, `4` assign, `5` change status, `6` reopen, `7` work queue, `8` reports, and `0` exit. Ticket IDs accept case variations at the prompts; status changes accept `in_progress` or `resolved`.

Every successful creation, assignment, status change, and reopening is saved immediately to `data/tickets.json`, excluded from Git. On restart, existing tickets are loaded before the menu appears. If loading fails, the program displays an error and exits so the original data is preserved. With the app closed, move that file elsewhere to start fresh while preserving a backup.

## Required behavior

Priority uses the first matching rule: high urgency plus at least 10 users → critical; high urgency or at least 10 users → high; medium urgency or at least 3 users → medium; otherwise low.

Tickets progress from open to in_progress to resolved. Assignment is required before in_progress. Reopen resolved tickets explicitly before editing. The queue includes open tickets ordered by priority and numeric ID.

## Collaboration and evidence

Read `AGENTS.md` and read the agreed contracts in `docs/design-decisions.md` before implementation. Each fellow writes code and tests, opens a PR, and obtains partner approval before merging. Record individual learning in `docs/ai-learning-log.md`.

Issues: https://github.com/0x777helsor/CampusFlow/issues

PR index: https://github.com/0x777helsor/CampusFlow/pulls

## Current implementation and limitations

All seven features are connected to the CLI. Kingsley's ticket creation, lookup, and JSON storage use the agreed contracts alongside Fabian's assignment, lifecycle, queue, and report functions. Previously reviewed priority and workflow changes remain part of the implementation.

Tests cover priority boundaries, invalid creation inputs, lookup, lifecycle guards, queue ordering, empty reports, JSON round trips, duplicate IDs, creation after reload, malformed data, and preservation of existing files when saving fails. CLI tests exercise the full lifecycle, reopening, queue and report output, restarts, invalid inputs, startup errors, and failed saves. Storage validates the agreed eight-field ticket format. Saves write a temporary file in the destination directory and replace the destination only after a successful write; the CLI updates its active collection only after saving succeeds.

Final integrated-main verification (2026-10-19): `python3 -m unittest discover -s tests -v` ran 61 tests successfully. A CLI walkthrough using a temporary JSON file created a critical ticket, assigned it, moved it through `in_progress` and `resolved`, reopened it, displayed the queue and report, and exited successfully. The saved record retained its assignment and reopened `open` status.

This is a single-user local application. Run one CLI instance at a time; concurrent writers are not coordinated.
