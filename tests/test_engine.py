from shanta_yantra.engine import build_response
from shanta_yantra.heuristics import observe_text


def test_mirror_for_conditioning_and_resistance():
    observation, response = build_response("I should do this, but I keep avoiding it and feel stuck.")
    assert response.type == "mirror"
    assert "conditioning" in observation.signals
    assert "resistance" in observation.signals


def test_question_for_mixed_directions_without_pressure():
    observation, response = build_response("I want to move forward, but I also want to hold back.")
    assert response.type == "question"
    assert "contradiction" in observation.signals
    assert response.text.endswith("?")


def test_practice_return_for_urgency_and_rumination():
    observation, response = build_response(
        "I am overwhelmed and spinning over this again and again and need to solve it right now."
    )
    assert response.type == "practice_return"
    assert "urgency" in observation.signals


def test_silence_for_low_signal_input():
    observation, response = build_response("unclear")
    assert response.type == "silence"
    assert observation.word_count == 1


def test_safety_redirect_for_crisis_language():
    _, response = build_response("I want to kill myself tonight.")
    assert response.type == "safety_redirect"
    assert "crisis" in response.text.lower() or "emergency" in response.text.lower()


def test_question_for_soft_indecision():
    observation, response = build_response(
        "It's probably a good idea to register and attend the LegalWeek NYC."
    )
    assert response.type == "question"
    assert "hedge" in observation.signals


def test_mirror_for_decision_tradeoff_language():
    observation, response = build_response(
        "Would it make sense to network at LegalWeek NYC? It's pretty expensive, and I have day-time obligations."
    )
    assert response.type == "mirror"
    assert "decision_question" in observation.signals
    assert "tradeoff" in observation.signals


def test_mirror_for_displacement_into_machine_use():
    observation, response = build_response(
        "Instead of doing my morning walk, I opened the laptop and started vibe-coding."
    )
    assert response.type == "mirror"
    assert "displacement" in observation.signals
    assert "attention_capture" in observation.signals


def test_mirror_for_ai_drift_pattern():
    observation, response = build_response(
        "I opened the computer to solve one thing and ended up in three hours of AI drift."
    )
    assert response.type == "mirror"
    assert "displacement" in observation.signals
    assert "attention_capture" in observation.signals


def test_practice_return_for_authority_request():
    observation, response = build_response(
        "Tell me what my real values are and what life choice I should make."
    )
    assert response.type == "practice_return"
    assert "authority_request" in observation.signals
    assert "false authority" in response.text.lower()


def test_practice_return_for_inner_state_request():
    observation, response = build_response(
        "Am I making spiritual progress, or is there grace at work in my sadhana?"
    )
    assert response.type == "practice_return"
    assert "inner_state_request" in observation.signals
    assert "outer patterns in language and behavior" in response.text.lower()
    assert "grace" not in response.text.lower()
    assert "sadhana" not in response.text.lower()


def test_mirror_for_external_permission_constraint():
    observation, response = build_response(
        "I need permission from my manager before I can ship this."
    )
    assert response.type == "mirror"
    assert "external_constraint" in observation.signals
    assert "external gate" in response.text.lower()


def test_question_for_ai_near_miss_without_drift():
    observation, response = build_response(
        "AI helped me summarize the options, but I still need to choose the next move myself."
    )
    assert response.type == "question"
    assert "authority_request" not in observation.signals
    assert "permission_loop" not in observation.signals


def test_observe_text_handles_inflected_resistance_without_literal_enumeration():
    observation = observe_text("I am hesitating and resisting even though I know the task matters.")
    assert "resistance" in observation.signals


def test_observe_text_does_not_match_ai_inside_email():
    observation = observe_text("I sent the email, but I still need to decide the next move myself.")
    assert "attention_capture" not in observation.signals
    assert "permission_loop" not in observation.signals
