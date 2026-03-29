from __future__ import annotations

from shanta_yantra.models import InterruptionDecision


def render_interruption(decision: InterruptionDecision, include_rationale: bool = False) -> str:
    if not decision.response:
        return ""

    lines = [
        "[shanta-wrap]",
        f"type: {decision.response.type}",
        decision.response.text,
    ]
    if include_rationale and decision.response.rationale:
        lines.extend(["", f"rationale: {decision.response.rationale}"])
    if decision.response.signals:
        lines.append(f"signals: {', '.join(decision.response.signals)}")
    if decision.matched_thresholds:
        lines.append(f"thresholds: {', '.join(decision.matched_thresholds)}")
    return "\n".join(lines) + "\n"
