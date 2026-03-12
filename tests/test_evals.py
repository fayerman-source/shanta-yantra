from __future__ import annotations

import json
from pathlib import Path

import pytest

from shanta_yantra.engine import build_response
from shanta_yantra.heuristics import observe_text


FIXTURE_PATH = Path(__file__).with_name("fixtures") / "engine_eval_cases.json"
EVAL_CASES = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


@pytest.mark.parametrize(
    "case",
    EVAL_CASES["build_response"],
    ids=[case["name"] for case in EVAL_CASES["build_response"]],
)
def test_build_response_eval_cases(case):
    observation, response = build_response(case["input"])

    assert response.type == case["expected_type"]

    for signal in case["required_signals"]:
        assert signal in observation.signals

    for signal in case["forbidden_signals"]:
        assert signal not in observation.signals

    rendered = response.text.lower()
    for snippet in case["contains_text"]:
        assert snippet.lower() in rendered

    for snippet in case["omits_text"]:
        assert snippet.lower() not in rendered


@pytest.mark.parametrize(
    "case",
    EVAL_CASES["observe_text"],
    ids=[case["name"] for case in EVAL_CASES["observe_text"]],
)
def test_observe_text_eval_cases(case):
    observation = observe_text(case["input"])

    for signal in case["required_signals"]:
        assert signal in observation.signals

    for signal in case["forbidden_signals"]:
        assert signal not in observation.signals
