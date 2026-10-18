"""Conservative file operations. No recursive deletion or shell commands."""
from __future__ import annotations

from pathlib import Path


class FileManager:
    def list_directory(self, path: str | Path = Path.home(), limit: int = 50) -> list[str]:
        target = Path(path).expanduser().resolve()
        if not target.exists() or not target.is_dir():
            raise ValueError("The requested path is not an existing directory.")
        items = sorted(target.iterdir(), key=lambda item: (not item.is_dir(), item.name.casefold()))
        return [f"{'[DIR] ' if item.is_dir() else '[FILE] '}{item.name}" for item in items[:max(1, limit)]]

    def read_text(self, path: str | Path, max_chars: int = 12000) -> str:
        target = Path(path).expanduser().resolve()
        if not target.exists() or not target.is_file():
            raise ValueError("The requested path is not an existing file.")
        if target.stat().st_size > max_chars * 4:
            raise ValueError("File is too large for a safe text preview.")
        try:
            return target.read_text(encoding="utf-8")[:max_chars]
        except UnicodeDecodeError as exc:
            raise ValueError("This file is not UTF-8 text; refusing to decode it as text.") from exc

    def delete_file(self, path: str | Path, confirmed: bool = False) -> str:
        target = Path(path).expanduser().resolve()
        if not confirmed:
            raise PermissionError("Deletion requires an explicit confirmation from the user.")
        if not target.exists() or not target.is_file():
            raise ValueError("Only an existing individual file can be deleted.")
        target.unlink()
        return f"Deleted file: {target.name}"
