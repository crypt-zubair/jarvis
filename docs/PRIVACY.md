# Privacy and safety

- The default AI endpoint is `127.0.0.1:11434`, local Ollama on this computer.
- There is no cloud provider client or silent cloud fallback.
- Voice recording begins only after a hotkey press. The temporary WAV is deleted after transcription.
- Screen capture occurs only when the user explicitly asks for screen analysis.
- Screenshot understanding requires an explicitly configured local vision model. Without one, image analysis stays disabled.
- The app launcher uses a small allowlist and does not execute arbitrary shell commands produced by the model.
- Do not commit `.env`, access tokens, API keys, screenshots, audio, or private files.
- Before adding deletion, upload, sharing, system settings, or install actions, require explicit confirmation and add tests.
- Public repositories are visible to everyone. Change this repository to private when the initial build is ready if private access is the intended setup.
