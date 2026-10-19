# Repository Guidelines

## Active sprint: CampusFlow Next

Continue this existing repository using Python's standard library. Before work, read `docs/campusflow-next-handoff.md` completely, then `docs/design-decisions.md`. The handoff defines current ownership and progress for both computers. Its Next ownership supersedes the original ownership below. Original interfaces remain the baseline until both engineers agree to revised contracts.

KINGSLEY AMORIE is Engineer A (validation, workflow safety, notes business/data layer, storage and ID continuity). FABIAN PAUL is Engineer B (search, reports, CLI including notes menus, and understanding check). Preserve individual contributions; do not implement the partner's assigned work merely to finish faster. Both engineers author source and tests and perform genuine reciprocal reviews.

No external audit has been received. Do not invent audit findings, an audited SHA, experiments, authorship, or approvals. Next requires at least 14 meaningful tests covering all acceptance cases, at least five authored by each engineer, and one additional partner-module bug-hunter test devised by each engineer. Each engineer needs at least two focused commits, one substantial source-and-tests PR, and two new verified AI learning cycles. At least one genuine changed/rejected AI suggestion per team must be supported by evidence; do not deliberately invent an AI error to meet this requirement.

At session start, inspect Git state and identify the engineer using the checkout. At session end, update that engineer's handoff entry with actual changes, checks, blockers and next steps. GitHub and merged files are the shared record; local unpushed changes are not visible on the other computer. Never push automatically. Follow the detailed synchronization and review procedure in the handoff.

## Project Structure & Module Organization

CampusFlow is a Python command-line campus helpdesk. This repository starts empty; use the assessment’s suggested layout: `main.py` for the menu, `campusflow/tickets.py` for creation and priority, `workflow.py` for assignment and transitions, `storage.py` for JSON persistence, and `reports.py` for queue/report logic. Put automated tests in `tests/test_*.py`. Record agreed interfaces and ownership in `docs/design-decisions.md`, and individual learning evidence in `docs/ai-learning-log.md`.

## Build, Test, and Development Commands

Use Python’s standard library; no framework, database, AI SDK, or build step is required. Document the supported Python version in `README.md`.

- `python main.py`: run the CLI once implemented.
- `python -m unittest discover -s tests -v`: run all automated tests.
- `git status` and `git diff`: inspect changes before staging specific files.

## Coding Style & Naming Conventions

Use four-space indentation, `snake_case` for modules/functions/variables, and descriptive names. Keep interactive input and printing separate from business logic. Agree on return values and error handling before implementing shared functions. No formatter or linter is configured yet; follow consistent Python style.

## Business Rules & Reliability

Normalize valid category and urgency case variations. Reject blank titles and non-positive or non-integer affected-user counts. Apply priority rules in the assessment’s exact order. Require assignment before `in_progress`; enforce `open → in_progress → resolved`, and explicit reopening before modifying resolved tickets. Sort the open-ticket queue by priority, then numeric ID. Preserve unique IDs after reload; report malformed JSON without overwriting it.

## Testing Guidelines

Use `unittest` with descriptive `test_*` methods. Both fellows must write application code and tests. Deliver at least eight meaningful tests covering priority boundaries, invalid input, lifecycle guards, queue order, persistence, and IDs after reload. Run the complete suite on integrated `main` and record actual results.

## Commit & Pull Request Guidelines

No commit history exists yet. Follow assessment conventions: `feat/1-ticket-creation` branches and commits such as `feat: validate ticket creation`. Do not work directly on `main`. Each fellow authors a PR and reviews their partner’s PR with two substantive observations and final approval. Include issue references, changes, test evidence, and limitations. Retest and obtain approval after integration changes.

## Learning Evidence & Configuration

Each fellow records three verified AI interactions, including one corrected, improved, or rejected suggestion. Use AI for focused learning; never fabricate experiments, reviews, or results. Ignore `.venv/`, `__pycache__/`, `*.pyc`, `.env`, and `data/tickets.json`; never commit secrets.

## Shared Learning Instructions

Both fellows are learning Python. Explain changes before making them, use simple language, and offer hints before solving exercises. Explain important Python concepts and the causes of errors. Keep functions small and names descriptive; avoid unnecessary complexity. After application or test changes, run `python -m unittest discover -s tests -v`; never report completion with failing tests or present zero discovered tests as proof of correctness.

Do not delete files without permission, modify environment secrets, or push to GitHub automatically. Ask before major architectural changes. Preserve each fellow’s independent code, tests, learning evidence, and genuine human review.

Kingsley owns `main.py`, tickets, and storage on `feat/1-tickets-storage-cli` (Issue #1). Fabian owns workflow and reports on `feat/2-workflow-reports` (Issue #2). See `docs/design-decisions.md` for detailed ownership and proposed interfaces. Both fellows must agree on these contracts before coding. Initial setup establishes main; subsequent feature and fix work uses reviewed PRs.
