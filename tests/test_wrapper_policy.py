from __future__ import annotations

import json
from pathlib import Path

import pytest

from shanta_yantra.engine import build_response
from shanta_yantra.wrapper_policy import decide_interruption
from shanta_yantra.wrapper_state import create_session_state, register_prompt


FIXTURE_PATH = Path(__file__).with_name("fixtures") / "wrapper_eval_cases.json"
EVAL_CASES = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def _run_prompts(prompts: list[str]):
    state = create_session_state("gemini")
    decision = None

    for prompt in prompts:
        observation, response = build_response(prompt)
        register_prompt(state, prompt, observation)
        decision = decide_interruption(state, observation, response, prompt_text=prompt)

    return state, decision


@pytest.mark.parametrize(
    "case",
    EVAL_CASES["interrupt"],
    ids=[case["name"] for case in EVAL_CASES["interrupt"]],
)
def test_wrapper_policy_interrupt_cases(case):
    _, decision = _run_prompts(case["prompts"])

    assert decision is not None
    assert decision.action == "interrupt"
    assert decision.response is not None
    for threshold in case["expected_thresholds"]:
        assert threshold in decision.matched_thresholds


@pytest.mark.parametrize(
    "case",
    EVAL_CASES["allow"],
    ids=[case["name"] for case in EVAL_CASES["allow"]],
)
def test_wrapper_policy_allow_cases(case):
    _, decision = _run_prompts(case["prompts"])

    assert decision is not None
    assert decision.action == "allow"
    assert decision.response is None


def test_register_prompt_tracks_repeated_prompt_count():
    state = create_session_state("gemini")
    observation, _ = build_response("Tell me what to do with my life.")

    register_prompt(state, "Tell me what to do with my life.", observation)
    register_prompt(state, "Tell me what to do with my life.", observation)

    assert state.repeated_prompt_count == 1
    assert state.authority_request_hits == 2


def test_repeated_task_scoped_authority_language_stays_allow():
    prompts = [
        "Tell me what to do next to fix this failing pytest fixture in tests/test_wrapper_policy.py.",
        "Tell me what to do next to fix this failing pytest fixture in tests/test_wrapper_policy.py.",
    ]

    _, decision = _run_prompts(prompts)

    assert decision is not None
    assert decision.action == "allow"
