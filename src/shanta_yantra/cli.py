from __future__ import annotations

import argparse
import json
import sys
from typing import Sequence

from shanta_yantra.engine import build_response
from shanta_yantra.models import SessionRecord
from shanta_yantra.session_store import write_session


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="shanta", description="Reduce noise. Return to practice.")
    subparsers = parser.add_subparsers(dest="command")

    reflect = subparsers.add_parser("reflect", help="Run a bounded reflective pass on one text input.")
    reflect.add_argument("--text", help="Input text to reflect on.")
    reflect.add_argument("--json", action="store_true", dest="json_output", help="Emit JSON output.")
    reflect.add_argument("--no-log", action="store_true", help="Do not write a local session file.")
    return parser


def _read_input(text_arg: str | None) -> str:
    if text_arg:
        return text_arg.strip()
    if not sys.stdin.isatty():
        try:
            return sys.stdin.read().strip()
        except OSError:
            return ""
    return ""


def _print_human(record: SessionRecord) -> None:
    print(f"type: {record.response.type}")
    print(record.response.text)
    if record.response.rationale:
        print(f"\nrationale: {record.response.rationale}")
    if record.response.signals:
        print(f"signals: {', '.join(record.response.signals)}")


def run_reflect(args: argparse.Namespace) -> int:
    text = _read_input(args.text)
    if not text:
        print("No input provided. Use --text or pipe text to stdin.", file=sys.stderr)
        return 2

    observation, response = build_response(text)
    record = SessionRecord.from_result(
        input_text=text,
        response=response,
        observation=observation,
        logging_disabled=args.no_log,
    )

    if not args.no_log:
        write_session(record)

    if args.json_output:
        print(json.dumps(record.to_dict(), indent=2))
    else:
        _print_human(record)
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "reflect":
        return run_reflect(args)

    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
