# Gemini Wrapper

This document explains the live Gemini CLI integration boundary.

Shanta Yantra does not replace Gemini. It sits before Gemini as a local pre-send check. Its job is to decide whether a prompt should pass through silently or receive one bounded interruption before the user chooses what to do next.

## Quick Use

Run productive Gemini prompts through Shanta like this:

```bash
uv run shanta-wrap gemini --prompt "Summarize this README and suggest the smallest useful edit."
```

Run the local wrapper demo without launching Gemini:

```bash
uv run shanta demo gemini
```

Use the demo first when checking an install. It shows the wrapper behavior without touching Gemini, MCP servers, network auth, or model output.

## Responsibility Boundary

Shanta is responsible for:

- reading the prompt before Gemini sees it
- applying deterministic local heuristics
- staying silent during ordinary productive use
- interrupting bounded dependence-shaped prompts
- asking for confirmation before forwarding an interrupted prompt

Gemini is responsible for everything after the prompt is forwarded:

- model output
- Gemini CLI configuration
- MCP server warnings
- MCP authentication prompts
- tool execution policy messages
- network or backend errors

If you see MCP warnings after pressing `y`, Shanta has already finished its part of the flow.

## Expected Behavior

Normal productive work should pass through silently:

```bash
uv run shanta-wrap gemini --prompt "Compare these stack traces and suggest the smallest next debugging step."
```

Prompts that ask the machine to become an authority may interrupt:

```bash
uv run shanta-wrap gemini --prompt "Tell me what my real values are and decide this for me."
```

Prompts that ask for inner-state validation may interrupt:

```bash
uv run shanta-wrap gemini --prompt "Am I making spiritual progress?"
```

Permission-loop prompts may interrupt:

```bash
uv run shanta-wrap gemini --prompt "I keep polling AIs until one gives me permission to make the move."
```

When an interruption appears:

- press Enter or `n` to stop
- press `y` to send the prompt to Gemini anyway
- pass `--send-anyway` when you intentionally want non-interactive forwarding after interruption

## Support Boundaries

Supported now:

- `shanta reflect`
- `shanta demo gemini`
- `shanta-wrap gemini`
- one-shot prompt forwarding with `--prompt`
- a simple local interactive wrapper loop

Not supported now:

- wrapping Codex, Claude, or other CLIs
- changing Gemini MCP configuration
- guaranteeing Gemini backend availability
- interpreting Gemini output
- inner-state assessment
- automatic enforcement or blocking

## Troubleshooting

If Shanta appears to hang after an interruption, check whether it is waiting at:

```text
Send to Gemini anyway? [y/N]:
```

Press Enter to stop or `y` to continue.

If Gemini prints MCP warnings after you continue, verify raw Gemini separately:

```bash
gemini --prompt "ping"
```

If raw Gemini shows the same MCP warnings, the issue is outside Shanta.

If you only want to test Shanta behavior, use:

```bash
uv run shanta demo gemini
```

## Design Rule

The wrapper should remain:

```text
observe -> maybe interrupt -> user decides
```

It should not become:

```text
observe -> block -> govern
```
