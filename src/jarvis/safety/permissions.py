"""Simple policy checks for actions that may affect user data."""
from __future__ import annotations

DESTRUCTIVE_ACTIONS = {"delete_file", "overwrite_file", "upload", "share", "install", "system_change"}


def requires_confirmation(action: str) -> bool:
    return action.strip().lower() in DESTRUCTIVE_ACTIONS


def cloud_access_allowed() -> bool:
    # No cloud path is implemented in this release.
    return False


def arbitrary_shell_allowed() -> bool:
    return False
