"""Conversation history utilities."""
from __future__ import annotations


class Conversation:
    def __init__(self, max_messages: int = 20) -> None:
        self.max_messages = max(2, max_messages)
        self.messages: list[dict[str, str]] = []

    def add(self, role: str, content: str) -> None:
        if role not in {"user", "assistant", "system"}:
            raise ValueError("Unsupported conversation role.")
        self.messages.append({"role": role, "content": content})
        self.messages = self.messages[-self.max_messages :]

    def for_model(self, system_prompt: str) -> list[dict[str, str]]:
        return [{"role": "system", "content": system_prompt}, *self.messages]
