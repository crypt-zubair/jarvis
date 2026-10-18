"""Speech output through the Windows system voice using pyttsx3."""
from __future__ import annotations

import threading


class SpeechOutput:
    def __init__(self, enabled: bool = True, rate: int = 185) -> None:
        self.enabled = enabled
        self.rate = rate
        self._engine = None
        self._lock = threading.Lock()

    def _get_engine(self):
        if self._engine is None:
            try:
                import pyttsx3
                self._engine = pyttsx3.init()
                self._engine.setProperty("rate", self.rate)
            except Exception as exc:
                raise RuntimeError("Windows speech output could not initialize (pyttsx3/SAPI).") from exc
        return self._engine

    def speak(self, text: str) -> None:
        if not self.enabled or not text.strip():
            return
        with self._lock:
            engine = self._get_engine()
            engine.say(text)
            engine.runAndWait()

    def stop(self) -> None:
        if self._engine is not None:
            try:
                self._engine.stop()
            except Exception:
                pass
