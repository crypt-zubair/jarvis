"""Offline speech transcription via the optional faster-whisper package."""
from __future__ import annotations

from pathlib import Path


class SpeechRecognitionError(RuntimeError):
    """Raised when local speech recognition is unavailable."""


class SpeechRecognizer:
    def __init__(self, model_name: str = "tiny", device: str = "cpu") -> None:
        self.model_name = model_name
        self.device = device
        self._model = None

    def _get_model(self):
        if self._model is None:
            try:
                from faster_whisper import WhisperModel
            except ImportError as exc:
                raise SpeechRecognitionError(
                    "Offline transcription is optional. Install it with: pip install faster-whisper"
                ) from exc
            try:
                self._model = WhisperModel(
                    self.model_name,
                    device=self.device,
                    compute_type="int8" if self.device == "cpu" else "float16",
                )
            except Exception as exc:
                raise SpeechRecognitionError(
                    "Could not load local Whisper. Try the tiny model on CPU."
                ) from exc
        return self._model

    def transcribe(self, audio_path: str | Path) -> str:
        try:
            segments, _ = self._get_model().transcribe(
                str(audio_path), beam_size=1, vad_filter=True
            )
            return " ".join(segment.text.strip() for segment in segments).strip()
        except SpeechRecognitionError:
            raise
        except Exception as exc:
            raise SpeechRecognitionError("Local transcription failed.") from exc
