"""Read-only helpers for checking local Ollama models."""
from __future__ import annotations

from jarvis.ai.ollama_client import OllamaClient, OllamaError


class ModelManager:
    def __init__(self, client: OllamaClient) -> None:
        self.client = client

    def available_models(self) -> list[str]:
        return self.client.list_models()

    def model_available(self, model_name: str) -> bool:
        try:
            return any(
                item == model_name or item.split(":")[0] == model_name
                for item in self.available_models()
            )
        except OllamaError:
            return False
