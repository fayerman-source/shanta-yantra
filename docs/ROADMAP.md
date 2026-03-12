# Roadmap

## Current State

The project has a runnable v1.0 text prototype with a deterministic CLI, local session logging, and test coverage. The next work is to deepen the implementation without widening the claims.

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

- add lightweight speech-feature ingestion once inputs and claims are clearly separated
- broaden test coverage for edge-case phrasing and false positives
- add config controls only where they preserve bounded behavior
- document release and support expectations for public contributors

## Phase 2: Expression Mapping Layer

- add biometric context ingestion
- add sleep context ingestion
- add environmental context ingestion
- implement expression mapping across multiple inputs
- keep output cautious and non-authoritative
- expand tests for notation-vs-proof boundaries

## Phase 3: Contemplative Restraint Layer

- minimize interpretation further
- prefer silence where useful
- measure concentration, clarity, and reduced dependence
- validate that the system becomes less central over time

## Release Principle

Each phase should make the system more honest and less intrusive. New capability is acceptable only if it does not expand metaphysical claims or dependence pressure.
