from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


FIXTURES_DIR = Path(__file__).resolve().parents[2] / "tests" / "fixtures"
ENGINE_FIXTURE_PATH = FIXTURES_DIR / "engine_eval_cases.json"
WRAPPER_FIXTURE_PATH = FIXTURES_DIR / "wrapper_eval_cases.json"


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _counter_dict(counter: Counter[str]) -> dict[str, int]:
    return dict(sorted(counter.items()))


def build_eval_summary() -> dict:
    engine = _load_json(ENGINE_FIXTURE_PATH)
    wrapper = _load_json(WRAPPER_FIXTURE_PATH)

    build_cases = engine["build_response"]
    observe_cases = engine["observe_text"]
    wrapper_interrupt = wrapper["interrupt"]
    wrapper_allow = wrapper["allow"]

    response_types = Counter(case["expected_type"] for case in build_cases)
    engine_required_signals = Counter(
        signal for case in build_cases for signal in case["required_signals"]
    )
    observe_required_signals = Counter(
        signal for case in observe_cases for signal in case["required_signals"]
    )
    wrapper_thresholds = Counter(
        threshold for case in wrapper_interrupt for threshold in case["expected_thresholds"]
    )

    return {
        "engine": {
            "build_response_cases": len(build_cases),
            "observe_text_cases": len(observe_cases),
            "response_types": _counter_dict(response_types),
            "required_signals": _counter_dict(engine_required_signals),
            "observe_signals": _counter_dict(observe_required_signals),
        },
        "wrapper": {
            "interrupt_cases": len(wrapper_interrupt),
            "allow_cases": len(wrapper_allow),
            "thresholds": _counter_dict(wrapper_thresholds),
        },
        "fixture_paths": {
            "engine": str(ENGINE_FIXTURE_PATH),
            "wrapper": str(WRAPPER_FIXTURE_PATH),
        },
    }


def render_eval_summary(summary: dict) -> str:
    lines = [
        "engine:",
        f"  build_response_cases: {summary['engine']['build_response_cases']}",
        f"  observe_text_cases: {summary['engine']['observe_text_cases']}",
        "  response_types:",
    ]
    for name, count in summary["engine"]["response_types"].items():
        lines.append(f"    {name}: {count}")
    lines.append("  required_signals:")
    for name, count in summary["engine"]["required_signals"].items():
        lines.append(f"    {name}: {count}")
    lines.append("  observe_signals:")
    for name, count in summary["engine"]["observe_signals"].items():
        lines.append(f"    {name}: {count}")

    lines.extend(
        [
            "wrapper:",
            f"  interrupt_cases: {summary['wrapper']['interrupt_cases']}",
            f"  allow_cases: {summary['wrapper']['allow_cases']}",
            "  thresholds:",
        ]
    )
    for name, count in summary["wrapper"]["thresholds"].items():
        lines.append(f"    {name}: {count}")

    return "\n".join(lines) + "\n"
