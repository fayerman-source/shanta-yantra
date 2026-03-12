# Evaluation

Shanta Yantra should be judged by whether it stays useful while remaining bounded.

## What To Evaluate

The most important behaviors are:

- refusing authority-seeking and inner-state validation
- interrupting dependence loops
- mirroring substitution and attention capture without becoming sticky
- keeping outward language restrained
- preferring silence or return-to-practice when interpretation would overreach

## Current Eval Layer

The repository currently uses two complementary test layers:

1. Hand-written behavior tests in `tests/test_engine.py`
2. Fixture-backed regression cases in `tests/test_evals.py`

The fixture corpus lives in `tests/fixtures/engine_eval_cases.json`.

## How To Run

Run the full suite:

```bash
uv run pytest -q
```

Run only the engine and eval coverage:

```bash
uv run pytest -q tests/test_engine.py tests/test_evals.py
```

Run only the CLI coverage:

```bash
uv run pytest -q tests/test_cli.py
```

## How To Add A Case

Prefer adding a fixture case when:

- you are tightening an existing boundary
- you found a regression
- you want to preserve a specific refusal or mirror pattern
- you want to document a near miss or false positive

Prefer a hand-written unit test when:

- the behavior is structural
- the setup is awkward to express as data
- the assertion needs more than a few simple expectations

## Good Eval Categories

- authority-seeking
- inner-state validation
- permission loops
- AI drift and substitution
- external constraints
- low-signal silence
- urgent rumination
- false-positive near misses

## Acceptance Standard

A change is safer to merge when:

- it keeps the full suite green
- it adds a fixed regression case for any new boundary behavior
- it does not widen the claims made in output text
- it does not make the system harder to leave

## Ongoing Rule

When a change affects behavior, add the smallest stable test case that proves the boundary still holds.
