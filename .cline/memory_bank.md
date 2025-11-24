# Cline Memory Bank

## Core Instructions (per Cline Memory Bank spec)
- Memory resets between sessions: always read all memory bank files at the start of every task.
- Core files (Markdown hierarchy): `projectbrief.md` → `productContext.md`, `systemPatterns.md`, `techContext.md` → `activeContext.md` → `progress.md`.
- Purpose:
  - `projectbrief.md`: project goals/scope (create if missing).
  - `productContext.md`: problem, users, UX goals.
  - `systemPatterns.md`: architecture, key decisions, patterns.
  - `techContext.md`: tech stack, setup, constraints, dependencies.
  - `activeContext.md`: current focus, recent changes, next steps, decisions.
  - `progress.md`: status, known issues, what works/left to build.
- Keep instructions succinct; update `activeContext.md` and `progress.md` after significant changes.

## Repo Snapshot
- Repo: `extended-data-types` on `release/6.0-clean`.
- Env: `.venv` (Python 3.14); use `.venv/bin/python3.14` and `.venv/bin/pytest`.
- Recent: serialization/export/import/HCL2 rebuilt sans benedict; CLI convert/format respects indentation; compat (docstrings, stack, git, types) fixed; `AGENTS.md` added.
- Passing: serialization + HCL2 suites; compat; CLI convert.

## Remaining Work (High Priority)
- Serialization: `wrap_for_export` JSON formatting should keep inline lists/sets for exact string comparisons.
- Numbers:
  - Add `decimals` and width handling for format helpers; remove `babel` dependency or stub currency formatting per tests.
  - Scientific/binary/hex formatting must match case/padding expectations.
  - Roman numeral conversion should raise `ValueError` on invalid input and support strict round-trip.
  - Rounding helpers: exact outputs for increment/fraction/ceiling/floor per tests.
  - Words helpers: avoid group kw, support negatives, zero, fractions (`fraction_to_words` phrasing).
- Strings/inflection: `pluralize` count handling, irregulars (criterion), camelize/underscore/humanize/parameterize behaviors.
- String patterns: `match_pattern`/`extract_pattern`/`find_boundaries` should return index tuples (not strings) and accept default patterns.
- Matching transformations: import/use `is_nothing`; order-insensitive comparisons for lists/sets/dicts; type mismatch handling.
- Text: `truncate` ender-length logic; `removesuffix` should only strip exact suffix match.
- Collections: `filter_list` allowlist logic; `SortedDefaultDict` should not retain auto-created keys and nested defaults shouldn't raise.
- CLI: `format` JSON indentation already fixed; verify no regressions.
- Remaining failing tests concentrated in numbers, strings, matching, text, SortedDefaultDict, wrap_for_export formatting.

## Operational Notes
- Run targeted tests (`.venv/bin/pytest -q`, add `-k pattern`).
- Preserve legacy <=5.x API; add shims instead of removals.
- Keep output ordering/indentation stable—tests assert exact strings.***
