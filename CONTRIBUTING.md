# Contributing

Thanks for contributing to Shanta Yantra.

This project is still early, but it already has a runnable Python CLI and a boundary-first design. Good contributions make the implementation clearer, more testable, and more honest about what the system can and cannot do.

## Before You Start

Read these files first:

1. `README.md`
2. `GOVERNANCE.md`
3. `docs/ARCHITECTURE.md`
4. `docs/INTERACTION_MODEL.md`
5. `docs/ROADMAP.md`

If your change affects behavior, boundaries, or product language, make sure it still matches the governance document.

## Local Setup

```bash
uv sync --extra dev
```

## Common Commands

Run the test suite:

```bash
uv run pytest -q
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
- Keep public language plain and bounded.
- Do not add features that increase dependence, authority claims, or anthropomorphic tone.

## Pull Requests

Include:

- the purpose of the change
- files touched
- any behavior or terminology changes
- any follow-up work that remains open

Small, reviewable pull requests are preferred over large mixed changes.
