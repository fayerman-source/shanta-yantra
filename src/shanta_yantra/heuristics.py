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
    "hesitat",
    "procrast",
    "delay",
    "commit",
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
HEDGE_MARKERS = (
    "probably",
    "maybe",
    "perhaps",
    "might",
    "could",
    "i think",
    "not sure",
    "unsure",
)
DECISION_QUESTION_MARKERS = (
    "would it make sense",
    "does it make sense",
    "should i",
    "is it worth",
    "do i want to",
)
TRADEOFF_MARKERS = (
    "expensive",
    "cost",
    "costly",
    "obligation",
    "obligations",
    "schedule",
    "time",
    "daytime",
    "day-time",
    "constraint",
    "constraints",
)
DISPLACEMENT_MARKERS = (
    "instead of",
    "meant to",
    "ended up",
    "got pulled into",
    "lost the morning",
    "opened another tab",
    "one more thing",
    "felt easier so i stayed",
    "started vibe-coding",
    "ai drift",
)
ATTENTION_CAPTURE_MARKERS = (
    "screen",
    "tab",
    "computer",
    "laptop",
    "vibe-coding",
    "ai drift",
    "prompting models",
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
    hedges = _contains_any(normalized, HEDGE_MARKERS)
    decision_questions = _contains_any(normalized, DECISION_QUESTION_MARKERS)
    tradeoffs = _contains_any(normalized, TRADEOFF_MARKERS)
    displacement = _contains_any(normalized, DISPLACEMENT_MARKERS)
    attention_capture = _contains_any(normalized, ATTENTION_CAPTURE_MARKERS)
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
    if hedges:
        signals.append("hedge")
    if decision_questions:
        signals.append("decision_question")
    if tradeoffs:
        signals.append("tradeoff")
    if displacement:
        signals.append("displacement")
    if attention_capture:
        signals.append("attention_capture")

    likely_tensions: list[str] = []
    if contradictions:
        likely_tensions.append("mixed or competing directions")
    if conditioning and resistance:
        likely_tensions.append("pressure colliding with reluctance")
    if urgency and rumination:
        likely_tensions.append("pressure overtaking observation")
    if hedges:
        likely_tensions.append("tentative commitment")
    if decision_questions and tradeoffs:
        likely_tensions.append("possible value colliding with practical cost")
    if displacement:
        likely_tensions.append("intended action displaced by an easier pull")
    if displacement and attention_capture:
        likely_tensions.append("attention captured by the machine")

    likely_conditioning: list[str] = []
    if conditioning:
        likely_conditioning.append("rule-bound or pressure-based language")
    if self_judgment:
        likely_conditioning.append("self-judging interpretation")
    if tradeoffs:
        likely_conditioning.append("constraint-based framing")

    likely_resistance: list[str] = []
    if resistance:
        likely_resistance.append("avoidance or hesitation")
    if rumination:
        likely_resistance.append("repetitive mental looping")
    if hedges:
        likely_resistance.append("indecision or soft holding back")
    if displacement:
        likely_resistance.append("lower-friction substitution")
    if attention_capture:
        likely_resistance.append("attention capture or re-entry")

    raw_score = (
        len(contradictions)
        + len(conditioning)
        + len(resistance)
        + len(rumination)
        + len(urgency)
        + len(self_judgment)
        + len(hedges)
        + len(decision_questions)
        + len(tradeoffs)
        + len(displacement)
        + len(attention_capture)
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
