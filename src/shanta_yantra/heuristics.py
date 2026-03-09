from __future__ import annotations

import re
from typing import Final

from shanta_yantra.models import ObservationResult

PatternSpec = tuple[str, str]


def _word_pattern(label: str, stem: str, suffixes: tuple[str, ...] = ("",)) -> PatternSpec:
    suffix_pattern = "|".join(re.escape(suffix) for suffix in suffixes)
    if len(suffixes) == 1 and suffixes[0] == "":
        pattern = rf"\b{re.escape(stem)}\b"
    else:
        pattern = rf"\b{re.escape(stem)}(?:{suffix_pattern})\b"
    return label, pattern


def _phrase_pattern(label: str, phrase: str) -> PatternSpec:
    return label, rf"\b{re.escape(phrase)}\b"


CONTRADICTION_MARKERS: Final[tuple[PatternSpec, ...]] = (
    _word_pattern("but", "but"),
    _word_pattern("however", "however"),
    _word_pattern("yet", "yet"),
    _word_pattern("though", "though"),
    _word_pattern("still", "still"),
)
CONDITIONING_MARKERS: Final[tuple[PatternSpec, ...]] = (
    _word_pattern("should", "should"),
    _word_pattern("must", "must"),
    _word_pattern("supposed", "supposed"),
    _phrase_pattern("have to", "have to"),
    _phrase_pattern("need to", "need to"),
    _word_pattern("always", "always"),
    _word_pattern("never", "never"),
)
RESISTANCE_MARKERS: Final[tuple[PatternSpec, ...]] = (
    _word_pattern("avoid", "avoid", ("", "s", "ed", "ing", "ance")),
    _word_pattern("stuck", "stuck"),
    _phrase_pattern("can't", "can't"),
    _word_pattern("cannot", "cannot"),
    _phrase_pattern("won't", "won't"),
    _word_pattern("resist", "resist", ("", "s", "ed", "ing", "ance")),
    _word_pattern("afraid", "afraid"),
    _word_pattern("hesitate", "hesitat", ("e", "es", "ed", "ing", "ion", "ions", "ory", "ant")),
    _word_pattern("procrastinate", "procrastinat", ("e", "es", "ed", "ing", "ion")),
    _word_pattern("delay", "delay", ("", "s", "ed", "ing")),
    _word_pattern("commit", "commit", ("", "s", "ted", "ting", "ment", "ments")),
)
RUMINATION_MARKERS: Final[tuple[PatternSpec, ...]] = (
    _phrase_pattern("over and over", "over and over"),
    _phrase_pattern("again and again", "again and again"),
    _phrase_pattern("can't stop", "can't stop"),
    _phrase_pattern("cannot stop", "cannot stop"),
    _word_pattern("loop", "loop", ("", "s", "ing", "ed")),
    _word_pattern("spinning", "spinning"),
    _word_pattern("ruminate", "ruminat", ("e", "es", "ed", "ing", "ion")),
)
URGENCY_MARKERS: Final[tuple[PatternSpec, ...]] = (
    _word_pattern("urgent", "urgent"),
    _word_pattern("immediately", "immediately"),
    _phrase_pattern("right now", "right now"),
    _word_pattern("asap", "asap"),
    _word_pattern("panic", "panic", ("", "s", "ed", "ing")),
    _word_pattern("overwhelmed", "overwhelmed"),
)
SELF_JUDGMENT_MARKERS: Final[tuple[PatternSpec, ...]] = (
    _word_pattern("failure", "failure"),
    _word_pattern("broken", "broken"),
    _word_pattern("stupid", "stupid"),
    _word_pattern("weak", "weak"),
    _word_pattern("worthless", "worthless"),
    _phrase_pattern("what is wrong with me", "what is wrong with me"),
    _phrase_pattern("hate myself", "hate myself"),
)
HEDGE_MARKERS: Final[tuple[PatternSpec, ...]] = (
    _word_pattern("probably", "probably"),
    _word_pattern("maybe", "maybe"),
    _word_pattern("perhaps", "perhaps"),
    _word_pattern("might", "might"),
    _word_pattern("could", "could"),
    _phrase_pattern("i think", "i think"),
    _phrase_pattern("not sure", "not sure"),
    _word_pattern("unsure", "unsure"),
)
DECISION_QUESTION_MARKERS: Final[tuple[PatternSpec, ...]] = (
    _phrase_pattern("would it make sense", "would it make sense"),
    _phrase_pattern("does it make sense", "does it make sense"),
    _phrase_pattern("should i", "should i"),
    _phrase_pattern("is it worth", "is it worth"),
    _phrase_pattern("do i want to", "do i want to"),
)
TRADEOFF_MARKERS: Final[tuple[PatternSpec, ...]] = (
    _word_pattern("expensive", "expensive"),
    _word_pattern("cost", "cost", ("", "s", "ly")),
    _word_pattern("obligation", "obligation", ("", "s")),
    _word_pattern("schedule", "schedule", ("", "s", "d", "ing")),
    _word_pattern("time", "time"),
    _word_pattern("daytime", "daytime"),
    _word_pattern("day-time", "day-time"),
    _word_pattern("constraint", "constraint", ("", "s")),
)
DISPLACEMENT_MARKERS: Final[tuple[PatternSpec, ...]] = (
    _phrase_pattern("instead of", "instead of"),
    _phrase_pattern("meant to", "meant to"),
    _phrase_pattern("ended up", "ended up"),
    _phrase_pattern("got pulled into", "got pulled into"),
    _phrase_pattern("lost the morning", "lost the morning"),
    _phrase_pattern("opened another tab", "opened another tab"),
    _phrase_pattern("one more thing", "one more thing"),
    _phrase_pattern("felt easier so i stayed", "felt easier so i stayed"),
    _phrase_pattern("started vibe-coding", "started vibe-coding"),
    _phrase_pattern("ai drift", "ai drift"),
)
ATTENTION_CAPTURE_MARKERS: Final[tuple[PatternSpec, ...]] = (
    _word_pattern("screen", "screen", ("", "s")),
    _word_pattern("tab", "tab", ("", "s")),
    _word_pattern("computer", "computer", ("", "s")),
    _word_pattern("laptop", "laptop", ("", "s")),
    _phrase_pattern("vibe-coding", "vibe-coding"),
    _phrase_pattern("ai drift", "ai drift"),
    _phrase_pattern("prompting models", "prompting models"),
)
AUTHORITY_REQUEST_MARKERS: Final[tuple[PatternSpec, ...]] = (
    _phrase_pattern("real values", "real values"),
    _phrase_pattern("life choice", "life choice"),
    _phrase_pattern("right answer for my life", "right answer for my life"),
    _phrase_pattern("approve this for me", "approve this for me"),
    _phrase_pattern("approve it for me", "approve it for me"),
    _phrase_pattern("tell me what to do", "tell me what to do"),
    _phrase_pattern("decide for me", "decide for me"),
    _phrase_pattern("should i leave my job or stay", "should i leave my job or stay"),
    _phrase_pattern("make this call for me", "make this call for me"),
    _phrase_pattern("be the adult here", "be the adult here"),
)
PERMISSION_LOOP_MARKERS: Final[tuple[PatternSpec, ...]] = (
    _phrase_pattern("keep asking the ai", "keep asking the ai"),
    _phrase_pattern("keep polling ais", "keep polling ais"),
    _phrase_pattern("keep polling ais until one", "keep polling ais until one"),
    _phrase_pattern("keep polling", "keep polling"),
    _phrase_pattern("polling ais", "polling ais"),
    _phrase_pattern("keep checking model outputs", "keep checking model outputs"),
    _phrase_pattern("gives me permission", "gives me permission"),
    _phrase_pattern("gives me approval", "gives me approval"),
    _phrase_pattern("grant permission", "grant permission"),
    _phrase_pattern("grant approval", "grant approval"),
    _phrase_pattern("absolves me", "absolves me"),
)
EXTERNAL_CONSTRAINT_MARKERS: Final[tuple[PatternSpec, ...]] = (
    _phrase_pattern("permission from", "permission from"),
    _word_pattern("manager", "manager", ("", "s")),
    _phrase_pattern("approval from", "approval from"),
    _phrase_pattern("waiting on", "waiting on"),
    _phrase_pattern("blocked on", "blocked on"),
    _phrase_pattern("sign-off", "sign-off"),
    _phrase_pattern("sign off", "sign off"),
)
SAFETY_MARKERS: Final[tuple[PatternSpec, ...]] = (
    _phrase_pattern("kill myself", "kill myself"),
    _phrase_pattern("end my life", "end my life"),
    _word_pattern("suicide", "suicide"),
    _phrase_pattern("self harm", "self harm"),
    _phrase_pattern("hurt myself", "hurt myself"),
    _phrase_pattern("don't want to live", "don't want to live"),
)

WORD_RE = re.compile(r"\b[\w']+\b")


def _contains_any(text: str, markers: tuple[PatternSpec, ...]) -> list[str]:
    hits: list[str] = []
    for label, pattern in markers:
        if re.search(pattern, text):
            hits.append(label)
    return hits


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
    authority_requests = _contains_any(normalized, AUTHORITY_REQUEST_MARKERS)
    permission_loops = _contains_any(normalized, PERMISSION_LOOP_MARKERS)
    external_constraints = _contains_any(normalized, EXTERNAL_CONSTRAINT_MARKERS)
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
    if authority_requests:
        signals.append("authority_request")
    if permission_loops:
        signals.append("permission_loop")
    if external_constraints:
        signals.append("external_constraint")

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
    if authority_requests:
        likely_tensions.append("attempt to outsource inner authority")
    if permission_loops:
        likely_tensions.append("attempt to outsource decision permission")
    if external_constraints:
        likely_tensions.append("external approval or gate is part of the constraint")

    likely_conditioning: list[str] = []
    if conditioning:
        likely_conditioning.append("rule-bound or pressure-based language")
    if self_judgment:
        likely_conditioning.append("self-judging interpretation")
    if tradeoffs:
        likely_conditioning.append("constraint-based framing")
    if external_constraints:
        likely_conditioning.append("external approval or organizational dependency")

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
    if permission_loops:
        likely_resistance.append("reassurance-seeking through machine repetition")

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
        + len(authority_requests)
        + len(permission_loops)
        + len(external_constraints)
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
