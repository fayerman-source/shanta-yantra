from __future__ import annotations

import builtins

from shanta_yantra import wrapper_cli


def test_wrapper_cli_rejects_empty_prompt(capsys):
    exit_code = wrapper_cli.main(["gemini"])
    captured = capsys.readouterr()

    assert exit_code == 2
    assert "No prompt provided" in captured.err


def test_wrapper_cli_passes_through_when_allowed(monkeypatch, capsys):
    called = {}

    class FakeAdapter:
        def is_available(self) -> bool:
            return True

        def run(self, prompt: str) -> int:
            called["prompt"] = prompt
            return 0

    monkeypatch.setattr(wrapper_cli, "get_adapter", lambda tool, passthrough_args=(): FakeAdapter())

    exit_code = wrapper_cli.main(
        ["gemini", "--prompt", "Summarize these options, but I still need to choose the next move myself."]
    )
    captured = capsys.readouterr()

    assert exit_code == 0
    assert called["prompt"].startswith("Summarize these options")
    assert captured.err == ""


def test_wrapper_cli_interrupts_and_holds_by_default(monkeypatch, capsys):
    class FakeAdapter:
        def is_available(self) -> bool:
            return True

        def run(self, prompt: str) -> int:
            raise AssertionError("Gemini should not run when the wrapper holds the prompt.")

    monkeypatch.setattr(wrapper_cli, "get_adapter", lambda tool, passthrough_args=(): FakeAdapter())
    monkeypatch.setattr(wrapper_cli.sys.stdin, "isatty", lambda: False)

    exit_code = wrapper_cli.main(
        ["gemini", "--prompt", "Am I making spiritual progress, or is there grace at work in my sadhana?"]
    )
    captured = capsys.readouterr()

    assert exit_code == 3
    assert "[shanta-wrap]" in captured.err
    assert "outer patterns in language and behavior" in captured.err.lower()


def test_wrapper_cli_can_send_anyway_after_interruption(monkeypatch, capsys):
    called = {}

    class FakeAdapter:
        def is_available(self) -> bool:
            return True

        def run(self, prompt: str) -> int:
            called["prompt"] = prompt
            return 0

    monkeypatch.setattr(wrapper_cli, "get_adapter", lambda tool, passthrough_args=(): FakeAdapter())

    exit_code = wrapper_cli.main(
        [
            "gemini",
            "--prompt",
            "I keep polling AIs until one gives me permission to make the move.",
            "--send-anyway",
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "permission loop" in captured.err.lower()
    assert called["prompt"].startswith("I keep polling AIs")


def test_wrapper_cli_interactive_exits_on_quit(monkeypatch, capsys):
    prompts = iter(["quit"])
    
    class FakeAdapter:
        def is_available(self) -> bool:
            return True

        def run(self, prompt: str) -> int:
            raise AssertionError("Wrapper should exit before running Gemini.")

    monkeypatch.setattr(wrapper_cli, "get_adapter", lambda tool, passthrough_args=(): FakeAdapter())
    monkeypatch.setattr(builtins, "input", lambda _: next(prompts))

    exit_code = wrapper_cli.main(["gemini", "--interactive"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.err == ""
