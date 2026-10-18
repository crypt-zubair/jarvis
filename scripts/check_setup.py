"""Check the local JARVIS environment without recording audio or capturing the screen."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from jarvis.ai.ollama_client import OllamaClient
from jarvis.config import load_config


def main() -> int:
    config = load_config()
    print("JARVIS setup check")
    print("==================")
    print(f"Python: {sys.version.split()[0]}")
    print(f"Config: {ROOT / 'config' / 'settings.yaml'}")
    print(f"Ollama endpoint: {config['ai']['base_url']}")
    print(f"Chat model configured: {config['ai']['model']}")

    client = OllamaClient(
        base_url=config["ai"]["base_url"],
        model=config["ai"]["model"],
        timeout=10,
    )
    if client.health():
        print("Ollama server: reachable")
        try:
            models = client.list_models()
            print("Installed models: " + (", ".join(models) if models else "(none found)"))
            if not any(
                name == client.model or name.split(":")[0] == client.model
                for name in models
            ):
                print("WARNING: configured chat model was not found in the local model list.")
        except RuntimeError as exc:
            print(f"Model listing failed: {exc}")
    else:
        print("Ollama server: not reachable; start Ollama before using chat.")

    print("Optional offline speech recognition: " + (
        "installed" if importlib.util.find_spec("faster_whisper") else "not installed"
    ))
    print("Microphone and screenshot were not accessed by this diagnostic.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
