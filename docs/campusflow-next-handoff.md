# CampusFlow Next: shared working agreement and handoff

## Purpose and current stage

This is an upgrade of the existing CampusFlow repository, not a new application or stack. Use Python 3.10+, standard-library functions, dictionaries/lists, JSON, exceptions, unittest and the existing CLI structure. Preserve all original features and priority-rule precedence. The original Open Work Queue continues to include only open tickets, ordered by priority then numeric ticket ID.

Current stage: preparation and baseline diagnosis. Kingsley confirmed the roles below. No Next application implementation or revised interface agreement has been completed. No external audit or audited commit has been supplied. Do not treat self-diagnostic findings as mentor feedback.

Starting reference: `6ef5ff8` (completed original main, not an audited commit). Kingsley shared 61 passing tests in 0.180 seconds at that version, plus the original CLI demonstration. Next still needs a reproducible baseline with three manual inputs in `docs/baseline-check.md`; that file has not yet been created. Record commands, actual results, version and audit availability. Do not claim old results were freshly rerun.

## Ownership for this sprint

| Engineer | Owns application work | Owns corresponding tests |
| --- | --- | --- |
| A: KINGSLEY AMORIE | `campusflow/validation.py`, `tickets.py`, `workflow.py`, new `notes.py`, `storage.py`; validation, lifecycle protections, notes API, reload safety, ticket/note ID continuity | Validation, tickets, workflow, notes, storage |
| B: FABIAN PAUL | `main.py`, new `search.py`, `reports.py`, new `understanding_check.py`; search/filter interface, analytics, note menus, retries, six-question understanding check | Search, reports, CLI, understanding check |
| Both | Baseline, contracts, README, independent learning/reflections, integration, reciprocal review and demonstration | Original regressions and full acceptance coverage |

This replaces the original split: Fabian now owns CLI changes; Kingsley now owns workflow safety. Ownership coordinates edits, not rank. Discuss partner-file changes first. Each engineer devises one extra bug-hunter case for the other's module; coordinate edits rather than concurrently rewriting their tests.

## Before application coding: agree on contracts

Record agreed signatures, return values, side effects, failure behavior and ownership in `docs/design-decisions.md`. Its existing agreement describes the original eight-field version; it is not approval of Next changes. Both engineers must confirm revised contracts before coding shared APIs.

Decisions still pending:

- Notes API: A exposes add-note and read-note behavior for B's CLI. Agree collection/ticket arguments, return values and read-only display ordering. Existing business functions use `ValueError`; retain consistent error handling unless both agree otherwise.
- Ticket schema adds `notes: []`; each note has `note_id`, `author`, `message`. Agree ID validation and max-existing-number allocation for ticket and per-ticket note IDs. Failed actions consume no IDs.
- Central validation: define helpers and callers, validation-before-mutation, unique IDs and full collection invariants. Invalid actions must preserve the entire collection, including nested notes.
- Storage compatibility: preserve the JSON list format and existing eight-field records. Choose and document legacy loading/migration before changing validation. Never silently discard old tickets or overwrite invalid source data.
- Reload: parse and validate everything before replacing active memory. Agree the API and CLI behavior; failure preserves the current collection.
- Save isolation: current CLI copies dictionaries, but nested note lists will need separate protection. A and B must coordinate pending-copy behavior so failed saves cannot alter active notes.
- Search: agree read-only title substring matching with `casefold`, optional category/status/priority filters combined with AND, invalid-filter handling, and deterministic result ordering. Any priority-sorted search view stays separate from the original queue.
- Reports: retain original keys and agree category counts, unresolved/resolved counts and resolution percentage shape. Zero tickets gives 0%; use current status after reopening.
- Understanding check: B separates the six supplied questions from scoring. Invalid A/B/C/D choices retry; first submitted valid answers determine score 0–6. Obtain two explanations for discussion without automatically grading their correctness.

## Acceptance and evidence checklist

- Preserve original priority precedence, assignment guard, lifecycle, reopening, queue and persistence.
- Notes: trimmed nonblank author, trimmed message length 5–300, only open/in_progress may add, retained through resolve/reopen, ordered IDs preserved after reload.
- Search: case-insensitive substring and all supplied filters must match; never mutate records.
- Reports: totals and all status/priority/category counts agree; unresolved = open + in_progress; resolution percentage is resolved / total * 100, or 0 for empty input.
- Loading validates full schema, category/urgency/priority consistency, statuses, ticket ID uniqueness, and note shapes/IDs unique within each ticket. Invalid JSON/data leaves active memory unchanged.
- Cover all 14 assessment acceptance cases, at least five tests authored by each engineer, plus each engineer's extra partner-module case. For each bug-hunter case record initial state, input, expected/actual results, test name and any code change.
- Each engineer records two new learning cycles in `docs/ai-learning-log.md`, clearly separate from the original sprint: exact question, concept gap, unrelated experiment, verification and engineering decision. Do not relabel old learning as new. Do not manufacture an incorrect AI suggestion for the rejection requirement.
- Each engineer authors source and tests, at least two focused commits and one substantial PR. Each reviews the other's diff, runs relevant tests, leaves two specific observations, addresses blockers, reruns checks and obtains approval before merging. Re-review changes after requested revisions.
- Demonstrate independently: six-question quiz and two explanations, implementation invariants, a regression investigation, duplicate-ID rejection and personal contributions. Record honest individual reflections.
- Submit full names, repo URL, final main SHA, both feature PR URLs, test command/output, README, baseline, learning logs and demonstration evidence.

## Working from two computers

1. Read `AGENTS.md`, this file and design decisions. Check `git status`, current branch and latest history. Identify which engineer is present; do not assume a previous session's identity.
2. Fetch remote changes. With a clean checkout, update local main with `git switch main` and `git pull --ff-only`. Preserve uncommitted work; never reset or delete it to synchronize.
3. Create real GitHub issues for A's validation/notes/storage and B's search/reports/CLI/check work. Record their actual numbers below. Use branches such as `feat/<actual-issue>-validation-and-notes` and `feat/<actual-issue>-search-and-insights`; do not invent issue numbers.
4. Work on the appropriate branch. Explain changes, teach small concepts, and let the learner contribute. Do not use agents to impersonate either engineer or fabricate human review.
5. Update only your own progress block below wherever possible. Shared contract changes need both engineers' agreement. Commit/push through the human-controlled workflow so the other computer can receive the updates.
6. Before integration, merge the latest `origin/main` into the feature branch, preserving both contributions. Run `python3 -m unittest discover -s tests -v`; record actual results and obtain partner review of integration changes. No direct feature commits to main.
7. After each approved merge, both computers synchronize and rerun the integrated suite. Perform a final fresh-clone check. If branch protection is available, require approval; otherwise preserve actual review chronology. Never approve your own PR.

Agents must not invent progress, run personal-data demonstrations, push automatically, delete files without permission, or claim completion with failures or zero tests. Use dummy operator labels for new sprint demonstrations. A local update is not shared until pushed; an unmerged branch is not main.

## Engineer A handoff — Kingsley updates this block

- Status: baseline recorded; proposed contracts awaiting both engineers' confirmation.
- Issue / feature branch / PR: not created.
- Completed: role confirmed; AI prepared `docs/baseline-check.md` and Next contract proposal during Kingsley's session on 2026-10-20. No Next source/tests implemented.
- Checks: AI baseline at `0482c75`: Python 3.12.3, 61 tests passed in 0.164s; three scripted temporary-file CLI checks passed. See baseline for attribution and inputs.
- Blockers: revised contracts require both engineers' agreement; mentor priority focus not supplied.
- Next: Kingsley reads/explains the proposed contracts; obtain Fabian's confirmation or revisions, complete a focused learning cycle, then create the A issue and feature branch.

## Engineer B handoff — Fabian updates this block

- Status: Engineer B role recorded from Kingsley's confirmation; no new implementation reported.
- Issue / feature branch / PR: not created.
- Completed: no CampusFlow Next work recorded yet.
- Checks: none recorded for this sprint.
- Blockers: revised contracts require both engineers' agreement.
- Next: read this guide and existing code; confirm shared contracts with Kingsley, complete a focused learning cycle, then create the B issue and feature branch.

## Shared handoff

- Shared guide merged through PR #10 at `0482c75`. Current preparation branch: `docs/next-baseline-contracts`.
- Baseline and contract proposal are prepared locally; this preparation needs partner review before merging. No contract agreement is inferred from preparation.
- Issue links, revised contract agreement, review evidence, fresh-clone check and final submission SHA remain pending. Update these only from actual work. Earlier introduction text describes the starting state; use this block and each engineer's entry for subsequent progress.
