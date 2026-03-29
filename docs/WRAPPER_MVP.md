# Wrapper MVP

This document captures the current Gemini-first wrapper MVP now implemented in the repository. It also records the remaining shape for follow-on adapter work.

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

### Implemented baseline

- `shanta-wrap = "shanta_yantra.wrapper_cli:main"` entrypoint
- Gemini-first pre-send wrapper flow
- thin adapter boundary for later tools
- wrapper state, policy, and rendering layers
- fixture-backed wrapper tests

### Current file shape

- `src/shanta_yantra/models.py`
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

- `src/shanta_yantra/wrapper_state.py`
Responsibilities:

- append event
- update short-lived session state
- compute simple repetition and threshold counters

No subprocess or terminal handling logic here.

- `src/shanta_yantra/wrapper_policy.py`
Responsibilities:

- map `SessionState` plus latest user text to:
  - `allow`
  - `interrupt`
  - `silence`

Current threshold cases:

- repeated authority-seeking
- repeated inner-state validation requests
- repeated permission loops
- repeated substitution or AI drift language

This layer must remain non-coercive.

- `src/shanta_yantra/wrapper_render.py`
Responsibilities:

- render one bounded terminal interruption block
- reuse current Shanta response style where practical
- keep output sparse and one-shot

- `src/shanta_yantra/wrapper_cli.py`
Responsibilities:

- expose `shanta-wrap gemini`
- support one-shot `--prompt` use and a simple local `--interactive` loop
- collect user input before pass-through
- update `SessionState`
- call `wrapper_policy`
- print interruption if threshold is crossed
- require explicit `--send-anyway` or TTY confirmation before forwarding an interrupted prompt

### `src/shanta_yantra/heuristics.py`

- add wrapper-relevant markers only if necessary
- do not widen into inward inference

### `src/shanta_yantra/engine.py`

- prefer reusing `build_response()` for interruption content
- avoid adding wrapper-specific semantics to the core engine unless necessary

- `tests/test_wrapper_policy.py`
Current cases:

- one authority request does not necessarily interrupt
- repeated authority requests interrupt
- repeated inner-state validation interrupts
- repeated permission loop interrupts
- normal productive use stays silent

- `tests/test_wrapper_cli.py`
Current cases:

- argument parsing
- basic wrapper flow
- interruption print path
- silent path

- `tests/fixtures/wrapper_eval_cases.json`
Current multi-turn cases:

- normal usage
- escalating sanction-seeking
- repeated self-validation
- AI drift loop
- near-miss productive use that should stay silent

### Next follow-on work

- broaden wrapper false-positive coverage
- add Codex as a second adapter only if the same bounded posture holds
- avoid turning the wrapper into a persistent or governing presence

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
