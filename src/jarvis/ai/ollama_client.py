"""Ollama HTTP client; requests go only to the configured local endpoint."""
from __future__ import annotations

import requests


class OllamaError(RuntimeError):
    """Raised when local Ollama cannot complete a request."""


class OllamaClient:
    def __init__(
        self,
        base_url: str = "http://127.0.0.1:11434",
        model: str = "llama3.2:3b",
        timeout: int = 120,
        temperature: float = 0.4,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout
        self.temperature = temperature

    def health(self) -> bool:
        try:
            return requests.get(f"{self.base_url}/api/tags", timeout=4).ok
        except requests.RequestException:
            return False

    def list_models(self) -> list[str]:
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=8)
            response.raise_for_status()
            return [item.get("name", "") for item in response.json().get("models", [])]
        except (requests.RequestException, ValueError) as exc:
            raise OllamaError("Cannot read local Ollama models. Start Ollama and retry.") from exc

    def chat(self, messages: list[dict[str, str]]) -> str:
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {"temperature": self.temperature},
        }
        try:
            response = requests.post(
                f"{self.base_url}/api/chat", json=payload, timeout=self.timeout
            )
            response.raise_for_status()
            answer = response.json().get("message", {}).get("content", "").strip()
            if not answer:
                raise OllamaError("Ollama returned an empty response.")
            return answer
        except requests.Timeout as exc:
            raise OllamaError("Local Ollama timed out. Try a smaller model or retry.") from exc
        except requests.RequestException as exc:
            raise OllamaError(
                "Could not reach local Ollama. Check that it is running and the model is installed."
            ) from exc
        except ValueError as exc:
            raise OllamaError("Ollama returned an invalid response.") from exc

    def describe_image(self, image_base64: str, prompt: str, model: str) -> str:
        """Send an image only to an explicitly configured local vision model."""
        if not model.strip():
            raise OllamaError("Screen understanding is disabled: no local vision model is configured.")
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt, "images": [image_base64]}],
            "stream": False,
            "options": {"temperature": 0.2},
        }
        try:
            response = requests.post(
                f"{self.base_url}/api/chat", json=payload, timeout=self.timeout
            )
            response.raise_for_status()
            answer = response.json().get("message", {}).get("content", "").strip()
            if not answer:
                raise OllamaError("The local vision model returned an empty response.")
            return answer
        except (requests.RequestException, ValueError) as exc:
            raise OllamaError(
                "Local vision request failed. Confirm that the configured model supports images."
            ) from exc
