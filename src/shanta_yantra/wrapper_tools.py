from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass, field
from typing import Sequence


@dataclass(frozen=True, slots=True)
class ToolAdapter:
    name: str
    command: str
    prompt_args: tuple[str, ...] = ("--prompt",)
    passthrough_args: tuple[str, ...] = field(default_factory=tuple)

    def is_available(self) -> bool:
        return shutil.which(self.command) is not None

    def build_command(self, prompt: str) -> list[str]:
        return [self.command, *self.prompt_args, prompt, *self.passthrough_args]

    def run(self, prompt: str) -> int:
        completed = subprocess.run(self.build_command(prompt), check=False)
        return completed.returncode


def get_adapter(tool_name: str, passthrough_args: Sequence[str] = ()) -> ToolAdapter:
    if tool_name != "gemini":
        raise ValueError(f"Unsupported tool: {tool_name}")
    return ToolAdapter(name="gemini", command="gemini", passthrough_args=tuple(passthrough_args))
