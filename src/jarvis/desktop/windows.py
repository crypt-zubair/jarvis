"""Basic Windows process inspection helpers (read-only)."""
from __future__ import annotations

import psutil


def list_visible_processes(limit: int = 20) -> list[str]:
    """Return a small list of process names; does not terminate anything."""
    names: list[str] = []
    for process in psutil.process_iter(["name"]):
        try:
            name = process.info.get("name")
            if name and name not in names:
                names.append(name)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return sorted(names, key=str.casefold)[:max(1, limit)]
