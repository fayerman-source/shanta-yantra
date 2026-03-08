# Architecture

Adhara is designed as a restrained system for observation and return-to-practice. The architecture becomes quieter as the project matures.

## Phase 1: v1.0 - Outer Clarification

**Goal:** help users notice likely tension, confusion, or resistance in language and tone.

**Inputs:**
- text
- voice transcript
- lightweight speech features

**Behavior:**
- identify likely tension between aspiration, conditioning, and avoidance
- provide one concise mirror
- optionally ask one clarifying question
- stop early rather than prolong the interaction

**Example processing shape:**

```ts
interface V1Processing {
  input: {
    text?: string;
    transcript?: string;
    speechFeatures?: {
      pace?: string;
      rhythm?: string;
      strain?: string;
    };
  };
  analysis: {
    likelyTensions: string[];
    likelyConditioning: string[];
    likelyResistance: string[];
  };
  output: {
    type: "mirror" | "question" | "practice_return" | "silence";
    text?: string;
  };
}
```

## Phase 2: v2.0 - Expression Mapping

**Goal:** widen observation without widening claims.

**Inputs:**
- v1.0 inputs
- biometric context
- sleep context
- environmental context
- brief self-report

**Behavior:**
- map patterns across mental, emotional, physical, and subconscious expression
- surface possible distortions or conflicting tendencies
- reduce interpretation as quieter practice becomes more important

**Rules:**
- signals are notation, not proof
- expression mapping must remain tentative
- no feature may infer attainment, realization, or special status

## Phase 3: v3.0 - Contemplative Restraint

**Goal:** reduce mediation further and return the user to direct practice.

**Inputs:**
- short reflection
- optional practice context
- minimal optional signals

**Behavior:**
- prefer minimal prompts
- prefer silence when more output would add noise
- optimize for concentration and non-dependence

## System Shape

```text
User reflection or signal input
            |
            v
   Observation and filtering
            |
            v
  Response gate with hard limits
     |        |        |       |
     v        v        v       v
  mirror   question  practice  silence
                      return
```

## Stable Constraints

- The system is a mirror, not an authority.
- The system may organize outer material; it may not claim inner certainty.
- The system should become less necessary over time.
- Every phase should preserve a path back to offline practice.
