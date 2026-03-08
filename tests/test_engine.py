from shanta_yantra.engine import build_response


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
