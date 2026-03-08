from __future__ import annotations

import json
import os
from pathlib import Path
from uuid import uuid4

from shanta_yantra.models import SessionRecord


def default_session_dir() -> Path:
    xdg_data_home = os.environ.get("XDG_DATA_HOME")
    if xdg_data_home:
        return Path(xdg_data_home) / "shanta-yantra" / "sessions"
    return Path.home() / ".local" / "share" / "shanta-yantra" / "sessions"


def write_session(record: SessionRecord, directory: Path | None = None) -> Path:
    target_dir = directory or default_session_dir()
    target_dir.mkdir(parents=True, exist_ok=True)
    target_file = target_dir / f"{record.timestamp.replace(':', '-')}--{uuid4().hex[:8]}.json"
    target_file.write_text(json.dumps(record.to_dict(), indent=2) + "\n", encoding="utf-8")
    return target_file
