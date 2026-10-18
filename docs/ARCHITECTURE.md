# Architecture

## Data flow

1. A user types in the console or presses the configured global hotkey.
2. The microphone records a bounded turn from the Windows default input device.
3. Optional faster-whisper transcribes the recording locally.
4. The intent router handles a few explicit commands locally; general questions go to Ollama at the configured local endpoint.
5. Speech output uses the Windows system voice.
6. Screen capture is only called for an explicit screen-analysis request, and the image is sent only to a configured local vision model.

## Modules

- `config.py`: YAML settings and environment overrides.
- `core/assistant.py`: deterministic intent routing and chat orchestration.
- `ai/ollama_client.py`: local Ollama API wrapper.
- `voice/`: bounded microphone recording, optional offline transcription, and speech output.
- `vision/screen_capture.py`: on-demand primary-screen capture.
- `desktop/`: allowlisted app launch, read-only process listing, limited keyboard actions, and cautious file helpers.
- `safety/`: confirmation and policy helpers.

## Design constraints

The language model does not receive arbitrary shell execution tools. Model output is treated as text, not as code to execute. Destructive file actions require an explicit confirmation flag, and the current assistant does not automatically invoke deletion. No remote AI fallback is implemented.

## Next development milestones

1. Test the voice turn on the target Windows laptop and tune silence detection.
2. Add a small UI with visible listening/speaking states and a stop button.
3. Add interruption-safe speech playback.
4. Add explicitly confirmed file operations through deterministic intents.
5. Configure and test a local vision model on the available GPU before enabling image analysis.
