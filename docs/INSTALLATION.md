# Installation

## 1. Install prerequisites
1. Install Python 3.11 or 3.12 from python.org and enable the Python launcher.
2. Install Ollama for Windows.
3. Pull a small local chat model in PowerShell: `ollama pull llama3.2:3b`.
4. Check it: `ollama run llama3.2:3b`, then exit the model prompt.

## 2. Install JARVIS
From the repository folder:
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e .
```

Optional offline voice transcription:
```powershell
pip install -e ".[speech]"
```

If PowerShell blocks activation, run `.venv\Scripts\python.exe -m jarvis.main` directly.

## 3. Run
```powershell
jarvis
```
Or run `python -m jarvis.main` after installing the package. For source-only execution, set `$env:PYTHONPATH = "src"` first.

## 4. Microphone permissions
Open Windows Settings → Privacy & security → Microphone and enable microphone access for desktop apps. JARVIS records a bounded turn only after the configured hotkey. It uses the Windows default input device rather than a hardcoded headset/device index.
