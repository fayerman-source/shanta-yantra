from __future__ import annotations

import json
from pathlib import Path

import pytest

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


def test_cli_reads_transcript_file(tmp_path: Path, capsys):
    transcript = tmp_path / "input.txt"
    transcript.write_text("I should do this, but I keep avoiding it.", encoding="utf-8")

    exit_code = cli.main(["reflect", "--transcript", str(transcript), "--json", "--no-log"])
    captured = capsys.readouterr()
    payload = json.loads(captured.out)

    assert exit_code == 0
    assert payload["input_text"] == "I should do this, but I keep avoiding it."


def test_cli_rejects_both_text_and_transcript(capsys):
    exit_code = cli.main(["reflect", "--text", "x", "--transcript", "y", "--no-log"])
    captured = capsys.readouterr()

    assert exit_code == 2
    assert "either --text or --transcript" in captured.err


def test_cli_version_output(capsys):
    with pytest.raises(SystemExit) as excinfo:
        cli.main(["--version"])

    captured = capsys.readouterr()

    assert excinfo.value.code == 0
    assert captured.out.strip() == "shanta 0.1.0"


def test_cli_hides_rationale_when_requested(capsys):
    exit_code = cli.main(["reflect", "--text", "I should do this but I keep avoiding it.", "--no-log", "--no-rationale"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "rationale:" not in captured.out
    assert "signals:" in captured.out


def test_cli_writes_human_output_to_file(tmp_path: Path, capsys):
    output_path = tmp_path / "reflect.txt"

    exit_code = cli.main(
        [
            "reflect",
            "--text",
            "I should do this but I keep avoiding it.",
            "--no-log",
            "--output",
            str(output_path),
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out == ""
    assert output_path.exists()
    assert "type:" in output_path.read_text(encoding="utf-8")


def test_cli_writes_json_output_to_file(tmp_path: Path, capsys):
    output_path = tmp_path / "reflect.json"

    exit_code = cli.main(
        [
            "reflect",
            "--text",
            "I should do this but I keep avoiding it.",
            "--json",
            "--no-log",
            "--output",
            str(output_path),
        ]
    )
    captured = capsys.readouterr()
    payload = json.loads(output_path.read_text(encoding="utf-8"))

    assert exit_code == 0
    assert captured.out == ""
    assert payload["response"]["type"] in {"mirror", "question", "practice_return", "silence"}
