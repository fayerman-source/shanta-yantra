from __future__ import annotations

import json

from shanta_yantra import cli
from shanta_yantra.eval_summary import build_eval_summary, render_eval_summary


def test_build_eval_summary_counts_engine_and_wrapper_cases():
    summary = build_eval_summary()

    assert summary["engine"]["build_response_cases"] == 9
    assert summary["engine"]["observe_text_cases"] == 2
    assert summary["wrapper"]["interrupt_cases"] == 4
    assert summary["wrapper"]["allow_cases"] == 6
    assert summary["wrapper"]["thresholds"]["permission_loop"] == 1


def test_render_eval_summary_includes_wrapper_section():
    rendered = render_eval_summary(build_eval_summary())

    assert "engine:" in rendered
    assert "wrapper:" in rendered
    assert "permission_loop" in rendered


def test_cli_eval_summary_outputs_json(capsys):
    exit_code = cli.main(["eval-summary", "--json"])
    captured = capsys.readouterr()
    payload = json.loads(captured.out)

    assert exit_code == 0
    assert payload["engine"]["build_response_cases"] == 9
    assert payload["wrapper"]["interrupt_cases"] == 4
    assert payload["wrapper"]["allow_cases"] == 6


def test_cli_eval_summary_outputs_human_text(capsys):
    exit_code = cli.main(["eval-summary"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "engine:" in captured.out
    assert "wrapper:" in captured.out
