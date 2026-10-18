"""Small shared state container."""
from dataclasses import dataclass, field


@dataclass
class AssistantState:
    running: bool = True
    listening: bool = False
    speaking: bool = False
    last_user_text: str = ""
    conversation: list[dict[str, str]] = field(default_factory=list)

    def add_message(self, role: str, content: str) -> None:
        self.conversation.append({"role": role, "content": content})
        if len(self.conversation) > 20:
            del self.conversation[:-20]
