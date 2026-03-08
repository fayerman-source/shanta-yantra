# Why This Is Not Just A Prompt

A modern LLM can imitate the tone of Shanta Yantra with a single prompt.
That is useful for prototyping, but it is not the same thing as the product.

## A Prompt Gives Style

A prompt can ask a model to:
- be restrained
- ask one question at most
- avoid authority language
- return the user to practice

That may produce a good answer in one session.
It does not create a durable system.

## The Product Adds Structure

Shanta Yantra is a governed reflective protocol.
It adds things that a prompt alone does not reliably provide:

- a fixed response contract: `mirror`, `question`, `practice_return`, `silence`
- stopping rules and explicit refusal to prolong the session
- local audit logs for inspection and debugging
- tests for boundary behavior
- safety redirects for crisis language
- a portable behavior layer that does not depend on one model vendor

## Why That Matters

The main risk is not that AI sounds unreflective.
The main risk is that AI becomes persuasive, sticky, and hard to leave.

A prompt can ask for restraint.
A product can enforce restraint.

That difference matters if the goal is to:
- reduce dependence
- protect concentration
- make outputs inspectable
- stop before the system turns into an authority or companion

## Working Distinction

```text
prompt = behavior request
product = behavior request + boundaries + tests + logs + stopping rules
```

Shanta Yantra is being built as the second thing.
