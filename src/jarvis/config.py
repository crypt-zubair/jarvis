"""Load YAML configuration with environment overrides."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = PROJECT_ROOT / "config" / "settings.yaml"


def load_config(path: str | Path | None = None) -> dict[str, Any]:
    config_path = Path(path) if path else DEFAULT_CONFIG
    if config_path.exists():
        with config_path.open("r", encoding="utf-8") as file:
            config = yaml.safe_load(file) or {}
    else:
        config = {}

    for section in ("assistant", "ai", "voice", "privacy"):
        config.setdefault(section, {})
    config["ai"]["base_url"] = os.getenv(
        "JARVIS_OLLAMA_URL", config["ai"].get("base_url", "http://127.0.0.1:11434")
    ).rstrip("/")
    config["ai"]["model"] = os.getenv("JARVIS_MODEL", config["ai"].get("model", "llama3.2:3b"))
    config["ai"]["vision_model"] = os.getenv(
        "JARVIS_VISION_MODEL", config["ai"].get("vision_model", "")
    )
    config["assistant"]["hotkey"] = os.getenv(
        "JARVIS_HOTKEY", config["assistant"].get("hotkey", "ctrl+alt+j")
    )
    # This release has no cloud client or arbitrary shell executor.
    config["privacy"]["allow_cloud_fallback"] = False
    config["privacy"]["allow_arbitrary_shell_commands"] = False
    return config
