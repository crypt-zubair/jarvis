"""JARVIS application entry point."""
from __future__ import annotations

import logging
import threading

from jarvis.ai.ollama_client import OllamaClient
from jarvis.config import load_config
from jarvis.core.assistant import Assistant
from jarvis.core.state import AssistantState
from jarvis.voice.speech_output import SpeechOutput

LOG = logging.getLogger("jarvis")


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    config = load_config()
    ai_config = config["ai"]
    voice_config = config["voice"]
    assistant_config = config["assistant"]

    ai = OllamaClient(
        base_url=ai_config.get("base_url", "http://127.0.0.1:11434"),
        model=ai_config.get("model", "llama3.2:3b"),
        timeout=int(ai_config.get("request_timeout_seconds", 120)),
        temperature=float(ai_config.get("temperature", 0.4)),
    )
    state = AssistantState()
    assistant = Assistant(ai=ai, state=state, vision_model=ai_config.get("vision_model", ""))
    speech = SpeechOutput(enabled=bool(assistant_config.get("speak_replies", True)))

    print("\nJARVIS Local Assistant")
    print("----------------------")
    print("AI endpoint: local Ollama only")
    print(f"Model: {ai.model}")
    print("Type a message. Use /help for commands and /quit to exit.")
    print("Voice mode needs the optional faster-whisper package.\n")
    print("Ollama: " + ("connected" if ai.health() else "not reachable; start Ollama before asking AI questions."))

    hotkey = assistant_config.get("hotkey", "ctrl+alt+j")
    voice_lock = threading.Lock()

    try:
        import keyboard

        def on_hotkey() -> None:
            if not voice_lock.acquire(blocking=False):
                return
            state.listening = True
            audio_path = None
            try:
                from jarvis.voice.microphone import Microphone
                from jarvis.voice.speech_recognition import SpeechRecognizer
                microphone = Microphone(
                    sample_rate=int(voice_config.get("sample_rate", 16000)),
                    max_record_seconds=int(voice_config.get("max_record_seconds", 12)),
                    silence_seconds=float(voice_config.get("silence_seconds", 1.2)),
                    energy_threshold=float(voice_config.get("energy_threshold", 0.012)),
                )
                recognizer = SpeechRecognizer(
                    model_name=str(voice_config.get("whisper_model", "tiny")),
                    device=str(voice_config.get("whisper_device", "cpu")),
                )
                print("\nListening... speak now.")
                audio_path = microphone.record_until_silence()
                transcript = recognizer.transcribe(audio_path)
                if not transcript:
                    print("No speech detected.")
                    return
                print(f"You: {transcript}")
                answer = assistant.handle(transcript)
                print(f"JARVIS: {answer}")
                speech.speak(answer)
            except Exception as exc:
                LOG.exception("Voice turn failed")
                print(f"Voice error: {exc}")
            finally:
                if audio_path is not None:
                    audio_path.unlink(missing_ok=True)
                state.listening = False
                voice_lock.release()

        keyboard.add_hotkey(hotkey, on_hotkey, suppress=False)
        print(f"Voice shortcut registered: {hotkey}")
    except Exception as exc:
        print(f"Global shortcut unavailable ({exc}). Console mode remains available.")

    try:
        while state.running:
            try:
                user_text = input("\nYou: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nEnding session.")
                break
            if not user_text:
                continue
            if user_text.lower() in {"/quit", "/exit"}:
                break
            answer = assistant.handle(user_text)
            print(f"JARVIS: {answer}")
            try:
                speech.speak(answer)
            except RuntimeError as exc:
                print(f"Speech output unavailable: {exc}")
    finally:
        try:
            import keyboard
            keyboard.unhook_all_hotkeys()
        except Exception:
            pass
        speech.stop()
        print("JARVIS closed.")


if __name__ == "__main__":
    main()
