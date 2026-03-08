from __future__ import annotations

import json
from pathlib import Path

from shanta_yantra.models import ObservationResult, ResponseEnvelope, SessionRecord
from shanta_yantra.session_store import default_session_dir, write_session


def test_default_session_dir_uses_xdg(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path))
    assert default_session_dir() == tmp_path / "shanta-yantra" / "sessions"


def test_write_session_creates_parseable_json(tmp_path: Path):
    record = SessionRecord.from_result(
        input_text="test",
        response=ResponseEnvelope(type="mirror", text="ok", rationale="because"),
        observation=ObservationResult(confidence=0.5),
        logging_disabled=False,
    )
    path = write_session(record, tmp_path)
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["input_text"] == "test"
    assert payload["response"]["type"] == "mirror"
