"""Conversation loop and deterministic intent router."""
from __future__ import annotations

from jarvis.ai.ollama_client import OllamaClient, OllamaError
from jarvis.core.state import AssistantState
from jarvis.desktop.applications import ApplicationLauncher
from jarvis.vision.screen_capture import ScreenCapture

SYSTEM_PROMPT = (
    "You are JARVIS, a practical Windows desktop assistant. Be concise and clear. "
    "You run locally. Never claim to have performed an action unless a tool result confirms it. "
    "Never ask for passwords or secrets. Never generate shell commands for automatic execution. "
    "If a requested action is unavailable, explain that plainly."
)


class Assistant:
    def __init__(
        self,
        ai: OllamaClient,
        state: AssistantState | None = None,
        apps: ApplicationLauncher | None = None,
        screen: ScreenCapture | None = None,
        vision_model: str = "",
    ) -> None:
        self.ai = ai
        self.state = state or AssistantState()
        self.apps = apps or ApplicationLauncher()
        self.screen = screen or ScreenCapture()
        self.vision_model = vision_model

    def handle(self, user_text: str) -> str:
        text = user_text.strip()
        if not text:
            return "I didn't catch that. Try again."
        self.state.last_user_text = text
        lowered = text.lower().strip()

        if lowered in {"stop", "quit", "exit", "goodbye"}:
            self.state.running = False
            return "Stopping the current session."
        if lowered in {"/help", "help"}:
            return (
                "Try 'open notepad', 'open calculator', 'what am I looking at', "
                "'/models', '/help', or ask a general question. Screen capture is on-demand only."
            )
        if lowered == "/models":
            try:
                models = self.ai.list_models()
                return "Local Ollama models: " + (", ".join(models) if models else "none found")
            except OllamaError as exc:
                return str(exc)
        if lowered.startswith("open "):
            return self.apps.open_app(text[5:].strip())

        screen_phrases = (
            "what am i looking at", "describe my screen", "look at my screen", "analyze my screen"
        )
        if any(phrase in lowered for phrase in screen_phrases):
            if not self.vision_model:
                return (
                    "Screen image understanding is disabled because no local vision model is configured. "
                    "Set ai.vision_model to a vision-capable model installed in Ollama. Nothing was sent anywhere."
                )
            try:
                image_data = self.screen.capture_primary_base64()
                return self.ai.describe_image(
                    image_data,
                    "Describe the visible screen and help with the user's likely task. "
                    "Do not infer private information that is not clearly visible.",
                    self.vision_model,
                )
            except (RuntimeError, OllamaError) as exc:
                return str(exc)

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(self.state.conversation[-12:])
        messages.append({"role": "user", "content": text})
        try:
            answer = self.ai.chat(messages)
        except OllamaError as exc:
            return str(exc)
        self.state.add_message("user", text)
        self.state.add_message("assistant", answer)
        return answer
