from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from shanta_yantra import __version__
from shanta_yantra.engine import build_response
from shanta_yantra.eval_summary import build_eval_summary, render_eval_summary
from shanta_yantra.models import SessionRecord
from shanta_yantra.session_store import write_session


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="shanta", description="Reduce noise. Return to practice.")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command")

    reflect = subparsers.add_parser("reflect", help="Run a bounded reflective pass on one text input.")
    reflect.add_argument("--text", help="Input text to reflect on.")
    reflect.add_argument("--transcript", help="Path to a text transcript file to reflect on.")
    reflect.add_argument("--json", action="store_true", dest="json_output", help="Emit JSON output.")
    reflect.add_argument(
        "--no-rationale",
        action="store_true",
        help="Hide the rationale block in human-readable output.",
    )
    reflect.add_argument("--no-log", action="store_true", help="Do not write a local session file.")
    reflect.add_argument("--output", help="Write output to a file instead of stdout.")
    reflect.add_argument("--session-dir", help="Optional directory for session log files.")

    eval_summary = subparsers.add_parser(
        "eval-summary",
        help="Summarize the current fixture-backed engine and wrapper evaluation corpus.",
    )
    eval_summary.add_argument("--json", action="store_true", dest="json_output", help="Emit JSON output.")
    eval_summary.add_argument("--output", help="Write output to a file instead of stdout.")
    return parser


def _read_input(text_arg: str | None, transcript_arg: str | None) -> str:
    if text_arg and transcript_arg:
        raise ValueError("Use either --text or --transcript, not both.")
    if text_arg:
        return text_arg.strip()
    if transcript_arg:
        return Path(transcript_arg).read_text(encoding="utf-8").strip()
    if not sys.stdin.isatty():
        try:
            return sys.stdin.read().strip()
        except OSError:
            return ""
    return ""


def _format_human(record: SessionRecord, include_rationale: bool = True) -> str:
    lines = [f"type: {record.response.type}", record.response.text]
    if include_rationale and record.response.rationale:
        lines.extend(["", f"rationale: {record.response.rationale}"])
    if record.response.signals:
        lines.append(f"signals: {', '.join(record.response.signals)}")
    return "\n".join(lines) + "\n"


def _emit_output(text: str, output_path: str | None) -> None:
    if output_path:
        Path(output_path).write_text(text, encoding="utf-8")
        return
    print(text, end="")


def run_reflect(args: argparse.Namespace) -> int:
    try:
        text = _read_input(args.text, args.transcript)
    except FileNotFoundError as exc:
        print(f"Transcript file not found: {exc.filename}", file=sys.stderr)
        return 2
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2
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
        write_session(record, directory=Path(args.session_dir) if args.session_dir else None)

    if args.json_output:
        rendered = json.dumps(record.to_dict(), indent=2) + "\n"
    else:
        rendered = _format_human(record, include_rationale=not args.no_rationale)

    _emit_output(rendered, args.output)
    return 0


def run_eval_summary(args: argparse.Namespace) -> int:
    summary = build_eval_summary()
    if args.json_output:
        rendered = json.dumps(summary, indent=2) + "\n"
    else:
        rendered = render_eval_summary(summary)
    _emit_output(rendered, args.output)
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "reflect":
        return run_reflect(args)
    if args.command == "eval-summary":
        return run_eval_summary(args)

    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
