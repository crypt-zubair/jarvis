# Troubleshooting

## Ollama is not reachable
- Run `ollama list` in PowerShell.
- Ensure Ollama is running and `http://127.0.0.1:11434` is configured.
- Confirm the model name matches the output of `ollama list`.

## Voice shortcut does not register
- Try running PowerShell normally first. Some global keyboard hooks are blocked by permissions or security software.
- Console text mode should still work even if the shortcut fails.
- Ensure the `keyboard` package is installed in the same Python environment.

## No speech transcription
Install the optional offline recognizer:
```powershell
pip install faster-whisper
```
The first run may download the Whisper model. Transcription itself runs locally after download.

## Microphone is silent or wrong
- Set the intended device as the Windows default input.
- Check Windows microphone permissions and the input meter in Sound Settings.
- Adjust `voice.energy_threshold` in `config/settings.yaml`; lower it for a quiet microphone and raise it if background noise triggers recording.
- JARVIS intentionally uses the default input rather than a fixed device index.

## Screen analysis is disabled
A chat model such as `llama3.2:3b` is not necessarily a vision model. Install a vision-capable model locally in Ollama and set `ai.vision_model` in YAML. A text-only model cannot interpret images.
