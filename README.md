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

Once implemented:

```bash
python main.py
python -m unittest discover -s tests -v
```

The planned menu covers create, list/view, assign, change status, reopen, queue, reports, and exit. Runtime tickets will live in `data/tickets.json`, excluded from Git. With the app closed, move that file elsewhere to start fresh while preserving a backup.

## Required behavior

Priority uses the first matching rule: high urgency plus at least 10 users → critical; high urgency or at least 10 users → high; medium urgency or at least 3 users → medium; otherwise low.

Tickets progress from open to in_progress to resolved. Assignment is required before in_progress. Reopen resolved tickets explicitly before editing. The queue includes open tickets ordered by priority and numeric ID.

## Collaboration and evidence

Read `AGENTS.md` and read the agreed contracts in `docs/design-decisions.md` before implementation. Each fellow writes code and tests, opens a PR, and obtains partner approval before merging. Record individual learning in `docs/ai-learning-log.md`.

Issues: https://github.com/0x777helsor/CampusFlow/issues

PR index: https://github.com/0x777helsor/CampusFlow/pulls

## Current limitations

This is the planning foundation. Application code and tests are not implemented; no test results or reviewed feature PRs exist yet. Both fellows have agreed to the documented function contracts.
