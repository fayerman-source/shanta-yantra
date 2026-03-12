# Contributing

Thanks for contributing to Shanta Yantra.

This project is still early, but it already has a runnable Python CLI and a boundary-first design. Good contributions make the implementation clearer, more testable, and more honest about what the system can and cannot do.

## Before You Start

Read these files first:

1. `README.md`
2. `GOVERNANCE.md`
3. `docs/CONSTITUTION.md`
4. `docs/ARCHITECTURE.md`
5. `docs/INTERACTION_MODEL.md`
6. `docs/ROADMAP.md`

If your change affects behavior, boundaries, or product language, make sure it still matches the governance document.

For behavior changes, also check:

1. `docs/CONSTITUTION.md`
2. `docs/EVALUATION.md`
3. `docs/RAG_REVIEW_PROMPTS.md`
4. `tests/test_engine.py`
5. `tests/test_cli.py`

## Local Setup

```bash
uv sync --extra dev
```

## Common Commands

Run the test suite:

```bash
uv run pytest -q
```

Run the boundary-focused engine coverage:

```bash
uv run pytest -q tests/test_engine.py tests/test_evals.py
```

Try the CLI:

```bash
uv run shanta reflect --text "I should do this, but I keep avoiding it."
```

Use transcript input:

```bash
uv run shanta reflect --transcript notes/session.txt
```

## Contribution Guidelines

- Keep changes narrow and concrete.
- Prefer deterministic behavior over hidden complexity.
- Add or update tests when behavior changes.
- Prefer fixed evaluation cases over ad hoc examples when boundary behavior changes.
- Keep public language plain and bounded.
- Prefer outer-pattern mirroring over inward interpretation.
- Do not add features that increase dependence, authority claims, or anthropomorphic tone.

## Boundary Review

Before opening a pull request, confirm:

- the change does not validate inner condition
- the change does not increase engagement pressure
- the change improves or preserves stopping behavior
- the change uses outer-pattern language rather than inward claims
- new examples and tests cover the intended boundary

## Pull Requests

Include:

- the purpose of the change
- files touched
- any behavior or terminology changes
- any follow-up work that remains open

Small, reviewable pull requests are preferred over large mixed changes.
