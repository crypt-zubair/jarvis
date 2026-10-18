"""Allowlisted app launching; never execute arbitrary shell commands."""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

APP_ALIASES = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "paint": "mspaint.exe",
    "file explorer": "explorer.exe",
    "explorer": "explorer.exe",
    "command prompt": "cmd.exe",
    "powershell": "powershell.exe",
}


class ApplicationLauncher:
    def open_app(self, name: str) -> str:
        normalized = name.strip().lower()
        if normalized in APP_ALIASES:
            subprocess.Popen([APP_ALIASES[normalized]], shell=False)
            return f"Opening {normalized}."
        if normalized.startswith(("https://", "http://")):
            if os.name == "nt":
                os.startfile(normalized)  # type: ignore[attr-defined]
            else:
                import webbrowser
                webbrowser.open(normalized)
            return "Opening the website in your default browser."
        candidate = Path(name).expanduser()
        if candidate.exists():
            if os.name == "nt":
                os.startfile(str(candidate))  # type: ignore[attr-defined]
            else:
                import subprocess
                subprocess.Popen(["xdg-open", str(candidate)], shell=False)
            return f"Opening {candidate.name}."
        return (
            f"I don't have '{name}' in my safe app list. Add an explicit alias in "
            "desktop/applications.py rather than allowing arbitrary command execution."
        )
