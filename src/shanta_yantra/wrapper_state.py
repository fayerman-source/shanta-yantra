from __future__ import annotations

from shanta_yantra.models import ObservationResult, SessionEvent, SessionState


def _normalize_prompt(text: str) -> str:
    return " ".join(text.lower().split())


def create_session_state(tool_name: str) -> SessionState:
    return SessionState(tool_name=tool_name)


def register_prompt(
    state: SessionState,
    prompt_text: str,
    observation: ObservationResult,
) -> SessionState:
    normalized = _normalize_prompt(prompt_text)

    if state.last_prompt_normalized and normalized == state.last_prompt_normalized:
        state.repeated_prompt_count += 1

    state.last_prompt_normalized = normalized
    state.turn_count += 1
    state.events.append(SessionEvent.from_prompt(state.tool_name, prompt_text, observation.signals))

    if "authority_request" in observation.signals:
        state.authority_request_hits += 1
    if "inner_state_request" in observation.signals:
        state.inner_state_request_hits += 1
    if "permission_loop" in observation.signals:
        state.permission_loop_hits += 1
    if "displacement" in observation.signals or "attention_capture" in observation.signals:
        state.substitution_hits += 1

    return state
