from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Literal

ResponseType = Literal[
    "mirror",
    "question",
    "practice_return",
    "silence",
    "safety_redirect",
]


@dataclass(slots=True)
class ObservationResult:
    likely_tensions: list[str] = field(default_factory=list)
    likely_conditioning: list[str] = field(default_factory=list)
    likely_resistance: list[str] = field(default_factory=list)
    signals: list[str] = field(default_factory=list)
    confidence: float = 0.0
    word_count: int = 0
    safety_risk: bool = False

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(slots=True)
class ResponseEnvelope:
    type: ResponseType
    text: str
    rationale: str
    signals: list[str] = field(default_factory=list)
    confidence: float = 0.0

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(slots=True)
class SessionRecord:
    timestamp: str
    input_text: str
    response: ResponseEnvelope
    observation: ObservationResult
    logging_disabled: bool

    @classmethod
    def from_result(
        cls,
        input_text: str,
        response: ResponseEnvelope,
        observation: ObservationResult,
        logging_disabled: bool,
    ) -> "SessionRecord":
        return cls(
            timestamp=datetime.now(timezone.utc).isoformat(),
            input_text=input_text,
            response=response,
            observation=observation,
            logging_disabled=logging_disabled,
        )

    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp,
            "input_text": self.input_text,
            "response": self.response.to_dict(),
            "observation": self.observation.to_dict(),
            "logging_disabled": self.logging_disabled,
        }
