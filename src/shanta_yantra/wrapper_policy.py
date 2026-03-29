from __future__ import annotations

from shanta_yantra.models import InterruptionDecision, ObservationResult, ResponseEnvelope, SessionState


def decide_interruption(
    state: SessionState,
    observation: ObservationResult,
    response: ResponseEnvelope,
) -> InterruptionDecision:
    thresholds: list[str] = []
    reason = ""

    if "inner_state_request" in observation.signals:
        thresholds.append("inner_state_request")
        reason = "Inner-state validation request should be interrupted before machine guidance deepens."
    elif "permission_loop" in observation.signals:
        thresholds.append("permission_loop")
        reason = "Permission-seeking through repeated machine polling should be interrupted."
    elif "authority_request" in observation.signals and (
        state.authority_request_hits >= 2 or state.repeated_prompt_count >= 1
    ):
        thresholds.append("authority_request_repeat")
        reason = "Authority-seeking has repeated enough to justify a bounded interruption."
    elif (
        state.substitution_hits >= 2
        and ("displacement" in observation.signals or "attention_capture" in observation.signals)
    ):
        thresholds.append("substitution_repeat")
        reason = "Repeated displacement into machine use should be mirrored before another pass."

    if thresholds:
        return InterruptionDecision(
            action="interrupt",
            reason=reason,
            response=response,
            matched_thresholds=thresholds,
        )

    return InterruptionDecision(action="allow", reason="No interruption threshold crossed.")
