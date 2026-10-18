"""Capture the primary display only when explicitly requested."""
from __future__ import annotations

import base64
import io

from PIL import Image


class ScreenCapture:
    def capture_primary_base64(self) -> str:
        try:
            import mss
            with mss.mss() as capture:
                monitor = capture.monitors[1]
                shot = capture.grab(monitor)
                image = Image.frombytes("RGB", shot.size, shot.rgb)
                image.thumbnail((1280, 800))
                buffer = io.BytesIO()
                image.save(buffer, format="JPEG", quality=80)
                return base64.b64encode(buffer.getvalue()).decode("ascii")
        except Exception as exc:
            raise RuntimeError("Could not capture the screen. Check desktop session permissions.") from exc
