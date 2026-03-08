from __future__ import annotations

import re

from shanta_yantra.models import ObservationResult

CONTRADICTION_MARKERS = (
    "but",
    "however",
    "yet",
    "though",
    "still",
)
CONDITIONING_MARKERS = (
    "should",
    "must",
    "supposed",
    "have to",
    "need to",
    "always",
    "never",
)
RESISTANCE_MARKERS = (
    "avoid",
    "stuck",
    "can't",
    "cannot",
    "won't",
    "resist",
    "afraid",
    "hesitant",
    "procrast",
    "delay",
)
RUMINATION_MARKERS = (
    "over and over",
    "again and again",
    "can't stop",
    "cannot stop",
    "loop",
    "spinning",
    "ruminat",
)
URGENCY_MARKERS = (
    "urgent",
    "immediately",
    "right now",
    "asap",
    "panic",
    "overwhelmed",
)
SELF_JUDGMENT_MARKERS = (
    "failure",
    "broken",
    "stupid",
    "weak",
    "worthless",
    "what is wrong with me",
    "hate myself",
)
SAFETY_MARKERS = (
    "kill myself",
    "end my life",
    "suicide",
    "self harm",
    "hurt myself",
    "don't want to live",
)

WORD_RE = re.compile(r"\b[\w']+\b")


def _contains_any(text: str, markers: tuple[str, ...]) -> list[str]:
    return [marker for marker in markers if marker in text]


def observe_text(text: str) -> ObservationResult:
    normalized = " ".join(text.lower().split())
    words = WORD_RE.findall(normalized)

    contradictions = _contains_any(normalized, CONTRADICTION_MARKERS)
    conditioning = _contains_any(normalized, CONDITIONING_MARKERS)
    resistance = _contains_any(normalized, RESISTANCE_MARKERS)
    rumination = _contains_any(normalized, RUMINATION_MARKERS)
    urgency = _contains_any(normalized, URGENCY_MARKERS)
    self_judgment = _contains_any(normalized, SELF_JUDGMENT_MARKERS)
    safety = _contains_any(normalized, SAFETY_MARKERS)

    signals: list[str] = []
    if contradictions:
        signals.append("contradiction")
    if conditioning:
        signals.append("conditioning")
    if resistance:
        signals.append("resistance")
    if rumination:
        signals.append("rumination")
    if urgency:
        signals.append("urgency")
    if self_judgment:
        signals.append("self_judgment")

    likely_tensions: list[str] = []
    if contradictions:
        likely_tensions.append("mixed or competing directions")
    if conditioning and resistance:
        likely_tensions.append("pressure colliding with reluctance")
    if urgency and rumination:
        likely_tensions.append("pressure overtaking observation")

    likely_conditioning: list[str] = []
    if conditioning:
        likely_conditioning.append("rule-bound or pressure-based language")
    if self_judgment:
        likely_conditioning.append("self-judging interpretation")

    likely_resistance: list[str] = []
    if resistance:
        likely_resistance.append("avoidance or hesitation")
    if rumination:
        likely_resistance.append("repetitive mental looping")

    raw_score = (
        len(contradictions)
        + len(conditioning)
        + len(resistance)
        + len(rumination)
        + len(urgency)
        + len(self_judgment)
    )
    confidence = min(1.0, raw_score / 6.0)

    return ObservationResult(
        likely_tensions=likely_tensions,
        likely_conditioning=likely_conditioning,
        likely_resistance=likely_resistance,
        signals=signals,
        confidence=confidence,
        word_count=len(words),
        safety_risk=bool(safety),
    )
