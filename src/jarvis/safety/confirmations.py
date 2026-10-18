"""Human confirmation for actions that can change or destroy user data."""
from __future__ import annotations


def confirm_action(description: str) -> bool:
    answer = input(f"\nJARVIS wants to: {description}\nType YES to confirm: ").strip()
    return answer == "YES"
