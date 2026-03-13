# Wrapper MVP

This document captures the current implementation plan for an optional wrapper around existing AI CLIs. It is a planning artifact, not a committed product expansion.

## Goal

Add an optional, non-coercive wrapper around existing AI command-line tools that watches only outer session patterns, stays silent by default, and prints one bounded Shanta interruption when a clear threshold is crossed.

The wrapper must preserve the same constitutional rules as the core module:

- outer observation, not inner authority
- no dependence loops
- no inner-state validation
- no coercive enforcement
- interrupt briefly, then stop

## Product Posture

The wrapper may:

- reflect repeated authority-seeking
- reflect repeated permission loops
- reflect repeated inner-state validation requests
- reflect substitution or AI drift patterns

The wrapper must not:

- block the underlying tool by default
- enforce behavior mechanically
- become a persistent companion
- present hidden scores as truth
- claim to detect inner condition

## MVP Shape

```text
user
  |
  v
wrapped AI CLI
  |
  +-- observe outer session signals
  +-- evaluate threshold
  +-- if no threshold: stay silent
  +-- if threshold crossed: print one bounded interruption
  |
  v
user decides what to do next
```

## File-by-File Plan

### `pyproject.toml`

- add a second console entry point:
  - `shanta-wrap = "shanta_yantra.wrapper_cli:main"`

### `src/shanta_yantra/models.py`

- add small wrapper dataclasses:
  - `SessionEvent`
  - `SessionState`
  - `InterruptionDecision`

Keep them limited to outer signals such as:

- turn count
- repeated prompt count
- authority-request hits
- inner-state-request hits
- substitution hits
- interruption count

### `src/shanta_yantra/wrapper_state.py`

New file.

Responsibilities:

- append event
- update short-lived session state
- compute simple repetition and threshold counters

No subprocess or terminal handling logic here.

### `src/shanta_yantra/wrapper_policy.py`

New file.

Responsibilities:

- map `SessionState` plus latest user text to:
  - `allow`
  - `interrupt`
  - `silence`

First-threshold cases:

- repeated authority-seeking
- repeated inner-state validation requests
- repeated permission loops
- repeated substitution or AI drift language

This layer must remain non-coercive.

### `src/shanta_yantra/wrapper_render.py`

New file.

Responsibilities:

- render one bounded terminal interruption block
- reuse current Shanta response style where practical
- keep output sparse and one-shot

### `src/shanta_yantra/wrapper_cli.py`

New file.

Responsibilities:

- expose `shanta-wrap`
- support a minimal interface such as:
  - `shanta-wrap --tool codex`
  - `shanta-wrap --tool gemini`
  - `shanta-wrap --tool claude`
- collect user input before pass-through
- update `SessionState`
- call `wrapper_policy`
- print interruption if threshold is crossed

If full bidirectional terminal proxying is messy in the first iteration, a simpler pre-send wrapper is acceptable for phase 1.

### `src/shanta_yantra/heuristics.py`

- add wrapper-relevant markers only if necessary
- do not widen into inward inference

### `src/shanta_yantra/engine.py`

- prefer reusing `build_response()` for interruption content
- avoid adding wrapper-specific semantics to the core engine unless necessary

### `tests/test_wrapper_policy.py`

New file.

Minimum cases:

- one authority request does not necessarily interrupt
- repeated authority requests interrupt
- repeated inner-state validation interrupts
- repeated permission loop interrupts
- normal productive use stays silent

### `tests/test_wrapper_cli.py`

New file.

Minimum cases:

- argument parsing
- basic wrapper flow
- interruption print path
- silent path

### `tests/fixtures/wrapper_eval_cases.json`

New file.

Multi-turn cases:

- normal usage
- escalating sanction-seeking
- repeated self-validation
- AI drift loop
- near-miss productive use that should stay silent

### `docs/ARCHITECTURE.md`

- add a short note that optional wrappers are adapters around the same bounded core

### `docs/ROADMAP.md`

- add wrapper MVP as a possible next implementation branch
- emphasize optional, non-coercive, thresholded behavior

### `docs/CONSTITUTION.md`

- add one explicit rule:
  - wrapper integrations may interrupt, but must not enforce

### `README.md`

- after implementation, add a short wrapper section with one example invocation

## Acceptance Criteria

The wrapper MVP is acceptable only if all of the following hold:

- normal single-turn productive use stays silent
- repeated sanction-seeking triggers one interruption
- repeated inner-state validation triggers one interruption
- repeated permission loops trigger one interruption
- wrapper never presents itself as authority
- wrapper never blocks execution automatically
- full test suite stays green

## Design Law

```text
detect -> reflect -> stop
```

Not:

```text
detect -> block -> govern
```

## Status

This plan is preserved for continuity and future review.
It is not yet implemented.
