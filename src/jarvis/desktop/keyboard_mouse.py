"""Explicit user-invoked keyboard/mouse helpers.

These helpers are not exposed to the language model as free-form tool calls.
Callers should add confirmation around any action that changes user data.
"""
from __future__ import annotations


def type_text(text: str) -> None:
    import pyautogui
    pyautogui.write(text, interval=0.01)


def press_key(key: str) -> None:
    allowed = {"enter", "esc", "tab", "space", "backspace", "delete", "up", "down", "left", "right"}
    normalized = key.strip().lower()
    if normalized not in allowed:
        raise ValueError(f"Key is not on the safe allowlist: {key}")
    import pyautogui
    pyautogui.press(normalized)
