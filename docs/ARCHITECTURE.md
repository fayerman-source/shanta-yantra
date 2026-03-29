# Architecture

Shanta Yantra is designed as a restrained system for observation and return-to-practice. The architecture becomes quieter as the project matures.

## Phase 1: v1.0 - Outer Clarification

**Goal:** help users notice likely outer tension, confusion, substitution, or resistance in language and behavior.

**Inputs:**
- text
- transcript file

**Behavior:**
- identify likely pressure, hesitation, tradeoff, displacement, or attention capture
- provide one concise mirror
- optionally ask one clarifying question
- stop early rather than prolong the interaction

**Example processing shape:**

```ts
interface V1Processing {
  input: {
    text?: string;
    transcript?: string;
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

## Deferred Research

These are not part of the current implementation path for this repository:

- biometric context
- sleep context
- environmental context
- broader state-mapping beyond outer expression in language and behavior

Any future work here would require a new governance case and must still remain notation, not proof.

## Phase 2: Further Restraint

**Goal:** reduce mediation further and return the user to direct practice.

**Inputs:**
- short reflection
- minimal optional context

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

Optional adapters may sit in front of the same bounded core. The current implementation includes a Gemini-first pre-send wrapper that observes outer prompt/session patterns, stays silent during normal use, and prints one bounded interruption only when a threshold is crossed.

## Stable Constraints

- Shanta Yantra is a mirror, not an authority.
- The system may organize outer and mental material; it may not claim inner certainty.
- The system must leave the inner station free.
- The system should become less necessary over time.
- Every phase should preserve a path back to offline practice.
- Wrapper integrations may interrupt, but must not enforce.
