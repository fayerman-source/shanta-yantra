# Shanta Yantra

Reduce noise. Return to practice.

Shanta Yantra is a contemplative support system designed to help people observe patterns in thought, speech, behavior, and bodily state without replacing direct practice.

The project is intentionally narrow. It treats AI as a tool for outer observation and clarification, not as a guide, authority, or source of insight by itself.

## Why This Exists

Most AI systems are optimized to prolong attention. Shanta Yantra is designed to do the opposite.

Its purpose is to help users notice what is happening more clearly, reduce unnecessary mediation, and return to offline practice sooner.

## What Shanta Yantra Is

- A mirror for patterns in expression
- A support for clearer self-observation
- A framework for short, restrained interactions
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

## Repository Structure

```text
shanta-yantra/
├── README.md
├── GOVERNANCE.md
├── AGENTS.md
├── LICENSE
└── docs/
    ├── ARCHITECTURE.md
    ├── INTERACTION_MODEL.md
    └── ROADMAP.md
```

## Current Status

This repository now includes the first runnable implementation skeleton for a text-only v1.0 CLI.

Current contents:

- public positioning and boundaries
- architecture and interaction model
- roadmap for a standalone v1.0 core
- deterministic Python CLI for bounded reflective output
- local JSON session logging and test coverage

## Install

```bash
uv sync --extra dev
```

## Quickstart

```bash
uv run shanta reflect --text "I should do this, but I keep avoiding it."
```

Example JSON output:

```bash
uv run shanta reflect --text "I am overwhelmed and spinning over this again and again." --json
```

## v1.0 Limits

The current implementation is deliberately narrow:

- text input only
- one-shot CLI interactions
- deterministic rules-first engine
- no live voice, no model dependency, no database
- bounded outputs plus explicit stopping behavior

## Reading Order

1. `README.md`
2. `GOVERNANCE.md`
3. `docs/ARCHITECTURE.md`
4. `docs/INTERACTION_MODEL.md`
5. `docs/ROADMAP.md`
6. `docs/THESIS.md`
7. `docs/WHY_NOT_JUST_A_PROMPT.md`

## License

MIT. See `LICENSE`.
