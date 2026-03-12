# Shanta Yantra

[![Tests](https://github.com/fayerman-source/shanta-yantra/actions/workflows/tests.yml/badge.svg)](https://github.com/fayerman-source/shanta-yantra/actions/workflows/tests.yml)

Reduce noise. Return to practice.

Shanta Yantra is a contemplative support system designed to help people observe patterns in thought, speech, behavior, and bodily state without replacing direct practice.

The project is intentionally narrow. It treats AI as a tool for outer observation and clarification, not as a guide, authority, or source of insight by itself.

## Why This Exists

Most AI systems are optimized to prolong attention. Shanta Yantra is designed to do the opposite.

Its purpose is to help users notice what is happening more clearly, reduce unnecessary mediation, and return to offline practice sooner.

It is also being shaped as an attention-protection tool: something that can notice drift, substitution, and screen capture without turning those patterns into more machine time.

## What Shanta Yantra Is

- A mirror for patterns in expression
- A support for clearer self-observation
- A framework for short, restrained interactions
- A guard against attention capture and lower-friction substitution
- A system that should reduce dependence on itself over time

## What Shanta Yantra Is Not

- A spiritual guide or teacher
- A measure of consciousness itself
- A source of revelation, transmission, or hidden authority
- A replacement for meditation, reflection, journaling, or focused work
- An engagement-optimized companion

## Core Principles

1. **Outer observation, not inner authority**
   Shanta Yantra may highlight patterns in expression, but it must not claim privileged access to a person's inner state.

2. **Notation, not proof**
   Text, voice, biometric, sleep, and environmental signals are forms of notation. They may help describe expression, but they are not proof of realization, progress, or truth.

3. **Short sessions, clear stopping points**
   The system should prefer one useful mirror and a return to practice over extended dialogue.

4. **No dependence loops**
   Shanta Yantra should avoid reward loops, anthropomorphic behavior, retention mechanics, and persuasive nudging.

5. **Restraint before ambition**
   The system should speak less as the work deepens, not more.

6. **Protect concentration**
   A valid feature should help users notice drift, interruption, and substitution before those patterns harden into dependence.

## Architecture Summary

Shanta Yantra is organized into three phases:

- **v1.0: Outer Clarification**
  Text and voice input. Short mirrors that help separate likely tension, confusion, or resistance.
- **v2.0: Expression Mapping**
  Adds biometric, sleep, and environmental context to improve self-observation while keeping claims modest.
- **v3.0: Contemplative Restraint**
  Minimal prompting, deliberate silence, and stronger return-to-practice behavior.

## Design Standard

Every feature should make the system:

- more honest about what it can observe
- less likely to create dependence
- more willing to stop
- easier to leave behind when direct practice is available

## Current Status

This repository includes a runnable text-first v1.0 prototype with a deterministic Python CLI and test coverage.

Current contents:

- public positioning and boundaries
- architecture and interaction model
- roadmap for the next implementation steps
- deterministic Python CLI for bounded reflective output
- local JSON session logging
- tests for CLI behavior, response shaping, and session persistence
- early heuristics for decision-making, tradeoffs, and attention/substitution patterns

## What Exists Today

- one-shot CLI command: `shanta reflect`
- input via `--text`, `--transcript`, or stdin
- bounded response types: `mirror`, `question`, `practice_return`, `silence`, `safety_redirect`
- deterministic heuristics layer with no model or API dependency
- local JSON session logs for inspection and debugging
- test suite covering core response paths and logging behavior

## Install

```bash
uv sync --extra dev
```

## Quickstart

```bash
uv run shanta reflect --text "I should do this, but I keep avoiding it."
```

Example terminal output:

```text
type: mirror
This reads more like pressure meeting reluctance than a settled decision. Name the pressure, notice what tightens around it, and stop before turning it into a larger argument.

rationale: Conditioning and resistance are both present, so a direct mirror is more useful than a question.
signals: contradiction, conditioning, resistance
```

Transcript-file input:

```bash
uv run shanta reflect --transcript notes/session.txt
```

Example JSON output:

```bash
uv run shanta reflect --text "I am overwhelmed and spinning over this again and again." --json
```

Representative JSON shape:

```json
{
  "response": {
    "type": "mirror",
    "text": "This looks like a real tradeoff, not a hidden perfect answer. Separate the possible value from the cost or constraint, set a clean rule, and then take one next step."
  },
  "observation": {
    "signals": ["contradiction", "hedge", "decision_question", "tradeoff"]
  }
}
```

Run the test suite:

```bash
uv run pytest -q
```

## v1.0 Limits

The current implementation is deliberately narrow:

- text or transcript-file input
- one-shot CLI interactions
- deterministic rules-first engine
- no live voice, no model dependency, no database
- bounded outputs plus explicit stopping behavior
- local-only session logging

## Reading Order

1. `README.md`
2. `GOVERNANCE.md`
3. `docs/ARCHITECTURE.md`
4. `docs/INTERACTION_MODEL.md`
5. `docs/ROADMAP.md`
6. `docs/THESIS.md`
7. `docs/WHY_NOT_JUST_A_PROMPT.md`

## Repository Structure

```text
shanta-yantra/
├── README.md
├── GOVERNANCE.md
├── CONTRIBUTING.md
├── SECURITY.md
├── LICENSE
├── docs/
│   ├── ARCHITECTURE.md
│   ├── INTERACTION_MODEL.md
│   ├── ROADMAP.md
│   ├── THESIS.md
│   └── WHY_NOT_JUST_A_PROMPT.md
├── src/shanta_yantra/
│   ├── cli.py
│   ├── engine.py
│   ├── heuristics.py
│   ├── models.py
│   └── session_store.py
└── tests/
    ├── test_cli.py
    ├── test_engine.py
    └── test_session_store.py
```

## Contributing

See `CONTRIBUTING.md` for local development steps and contribution boundaries.

## Changelog

See `CHANGELOG.md` for release-oriented project history.

## Security

See `SECURITY.md` for vulnerability reporting guidance.

## License

MIT. See `LICENSE`.
