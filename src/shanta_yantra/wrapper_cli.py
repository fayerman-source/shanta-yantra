from __future__ import annotations

import argparse
import sys
from typing import Sequence

from shanta_yantra.engine import build_response
from shanta_yantra.wrapper_policy import decide_interruption
from shanta_yantra.wrapper_render import render_interruption
from shanta_yantra.wrapper_state import create_session_state, register_prompt
from shanta_yantra.wrapper_tools import get_adapter


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="shanta-wrap",
        description="Optional bounded wrapper around existing AI CLIs.",
    )
    parser.add_argument("tool", choices=["gemini"], help="Underlying AI CLI to wrap.")
    parser.add_argument("--prompt", help="Prompt text to send to the wrapped tool.")
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run a simple local prompt loop around the wrapped tool.",
    )
    parser.add_argument(
        "--send-anyway",
        action="store_true",
        help="Continue to the wrapped tool even after a Shanta interruption.",
    )
    parser.add_argument(
        "--show-rationale",
        action="store_true",
        help="Show rationale text inside wrapper interruptions.",
    )
    return parser


def _read_prompt(prompt_arg: str | None) -> str:
    if prompt_arg:
        return prompt_arg.strip()
    if not sys.stdin.isatty():
        try:
            return sys.stdin.read().strip()
        except OSError:
            return ""
    return ""


def _confirm_send() -> bool:
    try:
        answer = input("Send to Gemini anyway? [y/N]: ").strip().lower()
    except EOFError:
        return False
    return answer in {"y", "yes"}


def _normalize_tool_args(tool_args: Sequence[str]) -> list[str]:
    if not tool_args:
        return []
    if tool_args[0] == "--":
        return list(tool_args[1:])
    return list(tool_args)


def _handle_prompt(
    prompt: str,
    adapter,
    state,
    show_rationale: bool,
    send_anyway: bool,
) -> int:
    observation, response = build_response(prompt)
    register_prompt(state, prompt, observation)
    decision = decide_interruption(state, observation, response)

    if decision.action == "interrupt":
        sys.stderr.write(render_interruption(decision, include_rationale=show_rationale))
        state.interruption_count += 1
        if not send_anyway:
            if sys.stdin.isatty() and _confirm_send():
                return adapter.run(prompt)
            return 3

    return adapter.run(prompt)


def run_once(args: argparse.Namespace) -> int:
    prompt = _read_prompt(args.prompt)
    if not prompt:
        print("No prompt provided. Use --prompt or pipe text to stdin.", file=sys.stderr)
        return 2

    adapter = get_adapter(args.tool, passthrough_args=_normalize_tool_args(args.tool_args))
    if not adapter.is_available():
        print(f"Wrapped tool not found on PATH: {args.tool}", file=sys.stderr)
        return 127

    state = create_session_state(args.tool)
    return _handle_prompt(
        prompt,
        adapter,
        state,
        show_rationale=args.show_rationale,
        send_anyway=args.send_anyway,
    )


def run_interactive(args: argparse.Namespace) -> int:
    adapter = get_adapter(args.tool, passthrough_args=_normalize_tool_args(args.tool_args))
    if not adapter.is_available():
        print(f"Wrapped tool not found on PATH: {args.tool}", file=sys.stderr)
        return 127

    state = create_session_state(args.tool)

    while True:
        try:
            prompt = input(f"{args.tool}> ").strip()
        except EOFError:
            print(file=sys.stderr)
            return 0

        if not prompt:
            continue
        if prompt in {"exit", "quit", "/exit", "/quit"}:
            return 0

        exit_code = _handle_prompt(
            prompt,
            adapter,
            state,
            show_rationale=args.show_rationale,
            send_anyway=args.send_anyway,
        )
        if exit_code not in {0, 3}:
            return exit_code


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args, tool_args = parser.parse_known_args(argv)
    args.tool_args = tool_args

    if args.interactive:
        return run_interactive(args)
    return run_once(args)


if __name__ == "__main__":
    raise SystemExit(main())
