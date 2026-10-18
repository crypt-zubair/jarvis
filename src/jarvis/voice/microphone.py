"""Record one bounded microphone turn using the Windows default input device."""
from __future__ import annotations

import tempfile
import wave
from pathlib import Path

import numpy as np


class MicrophoneError(RuntimeError):
    """Raised for microphone or recording failures."""


class Microphone:
    def __init__(
        self,
        sample_rate: int = 16000,
        max_record_seconds: int = 12,
        silence_seconds: float = 1.2,
        energy_threshold: float = 0.012,
    ) -> None:
        self.sample_rate = sample_rate
        self.max_record_seconds = max_record_seconds
        self.silence_seconds = silence_seconds
        self.energy_threshold = energy_threshold

    def record_until_silence(self) -> Path:
        try:
            import sounddevice as sd
        except ImportError as exc:
            raise MicrophoneError("Install sounddevice to enable microphone input.") from exc

        block_seconds = 0.2
        block_size = int(self.sample_rate * block_seconds)
        max_blocks = max(1, int(self.max_record_seconds / block_seconds))
        silence_blocks_needed = max(1, int(self.silence_seconds / block_seconds))
        chunks: list[np.ndarray] = []
        speech_started = False
        silent_blocks = 0
        try:
            with sd.InputStream(
                samplerate=self.sample_rate, channels=1, dtype="float32", blocksize=block_size
            ) as stream:
                for _ in range(max_blocks):
                    block, _overflowed = stream.read(block_size)
                    block = np.asarray(block, dtype=np.float32).reshape(-1)
                    chunks.append(block.copy())
                    rms = float(np.sqrt(np.mean(np.square(block)))) if block.size else 0.0
                    if rms >= self.energy_threshold:
                        speech_started = True
                        silent_blocks = 0
                    elif speech_started:
                        silent_blocks += 1
                        if silent_blocks >= silence_blocks_needed:
                            break
        except Exception as exc:
            raise MicrophoneError(
                "Could not record from the default microphone. Check Windows input permissions and device settings."
            ) from exc

        audio = np.concatenate(chunks) if chunks else np.zeros(1, dtype=np.float32)
        with tempfile.NamedTemporaryFile(prefix="jarvis-", suffix=".wav", delete=False) as handle:
            output_path = Path(handle.name)
        pcm = np.clip(audio * 32767, -32768, 32767).astype("<i2")
        with wave.open(str(output_path), "wb") as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(self.sample_rate)
            wav.writeframes(pcm.tobytes())
        return output_path
