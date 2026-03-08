from __future__ import annotations

import json
from pathlib import Path

from shanta_yantra import cli


def test_cli_text_json_output(capsys):
    exit_code = cli.main(["reflect", "--text", "I should do this but I keep avoiding it.", "--json", "--no-log"])
    captured = capsys.readouterr()
    payload = json.loads(captured.out)

    assert exit_code == 0
    assert payload["response"]["type"] in {"mirror", "question", "practice_return", "silence"}


def test_cli_rejects_empty_input(capsys):
    exit_code = cli.main(["reflect", "--no-log"])
    captured = capsys.readouterr()
    assert exit_code == 2
    assert "No input provided" in captured.err


def test_cli_writes_log_when_enabled(tmp_path: Path, monkeypatch, capsys):
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    exit_code = cli.main(["reflect", "--text", "I should slow down, but I keep pushing."])
    capsys.readouterr()

    session_dir = tmp_path / "shanta-yantra" / "sessions"
    session_files = list(session_dir.glob("*.json"))

    assert exit_code == 0
    assert len(session_files) == 1
