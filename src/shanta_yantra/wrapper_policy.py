from __future__ import annotations

from shanta_yantra.models import InterruptionDecision, ObservationResult, ResponseEnvelope, SessionState


TASK_SCOPED_MARKERS = (
    "pytest",
    "test",
    "file",
    "function",
    "method",
    "class",
    "module",
    "stack trace",
    "traceback",
    "error",
    "bug",
    "failing",
    "command",
    "cli",
    "repo",
    "code",
    ".py",
    ".ts",
    ".js",
)


def _looks_task_scoped(prompt_text: str) -> bool:
    normalized = prompt_text.lower()
    return any(marker in normalized for marker in TASK_SCOPED_MARKERS)


def decide_interruption(
    state: SessionState,
    observation: ObservationResult,
    response: ResponseEnvelope,
    prompt_text: str = "",
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
        if not _looks_task_scoped(prompt_text):
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
