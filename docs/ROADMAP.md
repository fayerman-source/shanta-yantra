# Roadmap

## Current State

The project has a runnable v1.0 text prototype with a deterministic CLI, local session logging, test coverage, and a Gemini-first optional wrapper MVP. The next work is to deepen the implementation without widening the claims.

Shanta Yantra is the bounded proving module for this line of work. If it cannot preserve restraint, anti-dependence behavior, and stopping discipline, the scope should not expand.

## Phase 1: v1.0 Standalone Core

Completed:

- define text ingestion workflow
- define transcript-file ingestion workflow
- implement an observation and clarification engine
- implement the response gate: `mirror`, `question`, `practice_return`, `silence`, `safety_redirect`
- implement explicit stopping rules
- add local session state logging
- add tests for core CLI and boundary behavior

Next:

- broaden test coverage for edge-case phrasing and false positives
- add more fixture-style evaluation cases for wrapper interruptions and near-miss productive use
- tighten wrapper wording around sparse interruption, outer-pattern mirroring, and explicit refusal of inner-state validation
- add config controls only where they preserve bounded behavior
- document live integration expectations and support boundaries for public contributors

Release-quality `v1` should mean:

- the core refusal paths are covered by fixed eval cases
- contributor docs explain the boundary checks clearly
- public docs no longer imply wider scope than the module actually supports
- new changes can be judged against a small, stable behavior corpus

Current adapter branch after the release-quality baseline:

- optional Gemini-first wrapper MVP around an existing AI CLI
- non-coercive, thresholded, and silent by default
- see `docs/WRAPPER_MVP.md`

## Deferred Research

These are not currently authorized for implementation in this repository:

- biometric context ingestion
- sleep context ingestion
- environmental-state inference
- broader inner-state mapping

Any future revisit would require a separate governance case and much stronger justification than feature curiosity.

## Phase 2: Further Restraint

- minimize interpretation further
- prefer silence where useful
- measure concentration, clarity, and reduced dependence
- validate that the system becomes less central over time

## Release Principle

Each phase should make the system more honest and less intrusive. New capability is acceptable only if it does not expand metaphysical claims or dependence pressure.
