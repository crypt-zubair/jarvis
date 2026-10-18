# JARVIS

A local-first Windows desktop assistant. This first foundation focuses on local Ollama chat, bounded microphone recording, offline speech recognition (optional), Windows speech output, on-demand screen capture, and guarded desktop actions.

## Privacy and safety defaults
- AI requests go only to local Ollama at `http://127.0.0.1:11434` by default.
- There is no cloud AI fallback.
- Screenshots are captured only after an explicit screen-analysis request.
- Image understanding stays disabled until a local vision model is configured.
- The app launcher uses an allowlist and never executes arbitrary model-generated shell commands.
- Never commit `.env`, credentials, screenshots, recordings, or personal files.

## Requirements
- Windows 10/11 and Python 3.11 or 3.12 recommended.
- Ollama installed and running with a local chat model, e.g. `llama3.2:3b`.
- Microphone and speakers/headphones.
- Optional offline speech-to-text: `pip install faster-whisper`.

## Setup (PowerShell)
```powershell
git clone https://github.com/crypt-zubair/jarvis.git
cd jarvis
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e .
Copy-Item .env.example .env
```
Start Ollama, then run `jarvis` or `python -m jarvis.main`. If running from source without installing the package, set `$env:PYTHONPATH = "src"` first.

## Controls
- `Ctrl+Alt+J`: start a bounded voice turn (requires optional voice dependencies and Windows global-hotkey support).
- Type messages in the console as a fallback.
- `/help`, `/models`, `/quit` are available.
- Say/type `stop` to end the session.

## Scope
This is a working foundation, not a claim that every planned desktop feature is complete. Advanced interruption, file operations, and screen-image understanding require further Windows/model testing. See `docs/` for setup, privacy, and troubleshooting.
