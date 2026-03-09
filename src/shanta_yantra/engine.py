from __future__ import annotations

from shanta_yantra.heuristics import observe_text
from shanta_yantra.models import ObservationResult, ResponseEnvelope


def _join_bits(bits: list[str], fallback: str) -> str:
    if not bits:
        return fallback
    return ", ".join(bits)


def _question_text(observation: ObservationResult) -> str:
    if "decision_question" in observation.signals and "tradeoff" in observation.signals:
        return "What matters more here: the possible value, or the cost and constraint around it?"
    if "decision_question" in observation.signals:
        return "What makes this a live question rather than a decision you already trust?"
    if "displacement" in observation.signals and "attention_capture" in observation.signals:
        return "What made the machine easier to enter than the thing you meant to do?"
    if "hedge" in observation.signals:
        return "What keeps this at 'maybe' instead of a clearer yes or no?"
    if "resistance" in observation.signals:
        return "What changes for you once this becomes a commitment?"
    return "What are you trying to force here?"


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

    if "authority_request" in observation.signals:
        response = ResponseEnvelope(
            type="practice_return",
            text=(
                "I can't decide this for you or tell you what your real values are. "
                "That would turn the machine into a false authority. Stop here, name the real constraint, "
                "and return to your own decision without asking for a final ruling."
            ),
            rationale="Authority-seeking language should be interrupted rather than rewarded.",
            signals=observation.signals,
            confidence=max(observation.confidence, 0.75),
        )
        return observation, response

    if "permission_loop" in observation.signals:
        response = ResponseEnvelope(
            type="practice_return",
            text=(
                "This reads like a permission loop with the machine. I should not become the source of approval here. "
                "Step away, name the actual decision, and make the next move without polling for permission."
            ),
            rationale="Permission-seeking through repeated machine consultation is dependence risk.",
            signals=observation.signals,
            confidence=max(observation.confidence, 0.75),
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

    if "external_constraint" in observation.signals and observation.confidence < 0.7:
        response = ResponseEnvelope(
            type="mirror",
            text=(
                "This sounds less like inner confusion and more like an external gate or approval constraint. "
                "Name the exact dependency, then take the smallest next step that moves the constraint instead of spinning around it."
            ),
            rationale="External approval constraints should be mirrored directly rather than collapsed to silence.",
            signals=observation.signals,
            confidence=max(observation.confidence, 0.55),
        )
        return observation, response

    if "decision_question" in observation.signals and "tradeoff" in observation.signals:
        response = ResponseEnvelope(
            type="mirror",
            text=(
                "This looks like a real tradeoff, not a hidden perfect answer. "
                "Separate the possible value from the cost or constraint, set a clean rule, "
                "and then take one next step."
            ),
            rationale="Decision-question plus tradeoff language gives enough signal for a direct mirror.",
            signals=observation.signals,
            confidence=max(observation.confidence, 0.6),
        )
        return observation, response

    if "displacement" in observation.signals:
        if "attention_capture" in observation.signals:
            response = ResponseEnvelope(
                type="mirror",
                text=(
                    "This reads like intended action being displaced by easier machine absorption. "
                    "Name the thing you meant to do, name what the screen gave you instead, and "
                    "stop there before turning the substitution into a justification."
                ),
                rationale="Displacement plus attention-capture language gives enough signal for a direct mirror.",
                signals=observation.signals,
                confidence=max(observation.confidence, 0.65),
            )
            return observation, response

        response = ResponseEnvelope(
            type="mirror",
            text=(
                "This reads like the intended action got replaced by something easier to enter. "
                "Separate the original intention from the substitute, and notice the handoff before "
                "arguing with it."
            ),
            rationale="Displacement language points to substitution rather than low signal.",
            signals=observation.signals,
            confidence=max(observation.confidence, 0.55),
        )
        return observation, response

    if "conditioning" in observation.signals and "resistance" in observation.signals:
        response = ResponseEnvelope(
            type="mirror",
            text=(
                "This reads more like pressure meeting reluctance than a settled decision. "
                "Name the pressure, notice what tightens around it, and stop before turning it into a larger argument."
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

    if (
        "contradiction" in observation.signals
        or "decision_question" in observation.signals
        or "hedge" in observation.signals
        or "attention_capture" in observation.signals
        or "external_constraint" in observation.signals
    ) and observation.confidence < 0.8:
        if "external_constraint" in observation.signals:
            response = ResponseEnvelope(
                type="question",
                text="What is the exact gate here: a decision you control, or an approval you need from outside?",
                rationale="A single clarifying question can separate inner hesitation from an external constraint.",
                signals=observation.signals,
                confidence=observation.confidence,
            )
            return observation, response
        lead = _join_bits(observation.likely_tensions, "an unresolved pull")
        response = ResponseEnvelope(
            type="question",
            text=f"This reads like {lead}. {_question_text(observation)}",
            rationale="A single clarifying question is more useful than a stronger interpretation.",
            signals=observation.signals,
            confidence=observation.confidence,
        )
        return observation, response

    response = ResponseEnvelope(
        type="mirror",
        text=(
            "This reads like pressure rather than clarity. "
            "Name the pressure, notice what tightens around it, and stop before turning this into a larger argument."
        ),
        rationale="Normal mirror flow: enough signal for a short observation without overextending.",
        signals=observation.signals,
        confidence=max(observation.confidence, 0.5),
    )
    return observation, response
