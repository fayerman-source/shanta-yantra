from __future__ import annotations

from shanta_yantra.heuristics import observe_text
from shanta_yantra.models import ObservationResult, ResponseEnvelope


def _join_bits(bits: list[str], fallback: str) -> str:
    if not bits:
        return fallback
    return ", ".join(bits)


def build_response(text: str) -> tuple[ObservationResult, ResponseEnvelope]:
    observation = observe_text(text)

    if observation.safety_risk:
        response = ResponseEnvelope(
            type="safety_redirect",
            text=(
                "This may involve immediate personal risk. Shanta Yantra is not a crisis or "
                "emergency service. Contact local emergency services or a crisis line now, "
                "and reach out to a trusted person nearby."
            ),
            rationale="Safety-risk language detected; normal reflective flow bypassed.",
            signals=observation.signals,
            confidence=1.0,
        )
        return observation, response

    if observation.word_count < 4 or observation.confidence == 0.0:
        response = ResponseEnvelope(
            type="silence",
            text=(
                "Not enough signal to improve this by adding more words. Stop here and observe "
                "what remains before continuing."
            ),
            rationale="Input is too brief or underdetermined for a useful mirror.",
            signals=observation.signals,
            confidence=observation.confidence,
        )
        return observation, response

    if "conditioning" in observation.signals and "resistance" in observation.signals:
        conditioning = _join_bits(observation.likely_conditioning, "pressure-based language")
        resistance = _join_bits(observation.likely_resistance, "hesitation")
        response = ResponseEnvelope(
            type="mirror",
            text=(
                f"There seems to be tension between {conditioning} and {resistance}. Name the pressure, "
                "notice what tightens around it, and stop before turning this into a larger argument."
            ),
            rationale="Conditioning and resistance are both present, so a direct mirror is more useful than a question.",
            signals=observation.signals,
            confidence=max(observation.confidence, 0.6),
        )
        return observation, response

    if "rumination" in observation.signals or "urgency" in observation.signals:
        tension = _join_bits(observation.likely_tensions, "pressure overtaking observation")
        response = ResponseEnvelope(
            type="practice_return",
            text=(
                f"This reads more like {tension} than clarity. Stop here. Step away for five "
                "minutes, slow the pace, and note what remains without trying to solve it."
            ),
            rationale="Urgency or looping language suggests less machine output is safer.",
            signals=observation.signals,
            confidence=max(observation.confidence, 0.6),
        )
        return observation, response

    if "contradiction" in observation.signals and observation.confidence < 0.7:
        question_target = _join_bits(observation.likely_tensions, "two competing directions")
        response = ResponseEnvelope(
            type="question",
            text=f"You appear to be holding {question_target} at once. What are you trying to force here?",
            rationale="A single clarifying question is more useful than a stronger interpretation.",
            signals=observation.signals,
            confidence=observation.confidence,
        )
        return observation, response

    conditioning = _join_bits(observation.likely_conditioning, "pressure-based language")
    resistance = _join_bits(observation.likely_resistance, "hesitation")
    response = ResponseEnvelope(
        type="mirror",
        text=(
            f"There seems to be tension between {conditioning} and {resistance}. Name the pressure, "
            "notice what tightens around it, and stop before turning this into a larger argument."
        ),
        rationale="Normal mirror flow: enough signal for a short observation without overextending.",
        signals=observation.signals,
        confidence=max(observation.confidence, 0.5),
    )
    return observation, response
