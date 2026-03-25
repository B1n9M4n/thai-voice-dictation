# Thai Voice Dictation

Thai speech-to-text using MLX-Whisper (optimized for Apple Silicon).

## Features

- Local processing (no internet required after model download)
- Thai word segmentation using PyThaiNLP
- Filler word removal
- **Context-aware output** (email, chat, formal modes)
- **Custom dictionary** for fixing misrecognitions
- **Auto politeness particles** (ครับ/ค่ะ)
- Runs on Apple Silicon GPU
- No API costs - completely free after setup

## Quick Start

```bash
cd ~/thai-voice-dictation

# Test with included Thai audio samples
~/.local/bin/uv run transcribe.py samples/test_thai_1.mp3

# Record your own Thai voice
~/.local/bin/uv run record_thai.py 5
```

## Usage

### Transcribe audio file

```bash
# Basic transcription
~/.local/bin/uv run transcribe.py your_audio.mp3

# Larger model (better accuracy)
~/.local/bin/uv run transcribe.py your_audio.mp3 --model medium

# Context modes (general, email, chat, formal)
~/.local/bin/uv run transcribe.py your_audio.mp3 --context email

# Raw output only (no processing)
~/.local/bin/uv run transcribe.py your_audio.mp3 --raw
```

### Context Modes

| Mode | Behavior | Use Case |
|------|----------|----------|
| `general` | Basic processing, Thai period | Default |
| `email` | Auto-adds ครับ, formal punctuation | Professional emails |
| `chat` | Casual, no forced punctuation | Messaging apps |
| `formal` | Adds ครับ, Thai period | Documents, formal writing |

### Record from microphone

```bash
# Record 5 seconds
~/.local/bin/uv run record_thai.py 5

# Record 10 seconds
~/.local/bin/uv run record_thai.py 10
```

### Generate test audio

```bash
~/.local/bin/uv run generate_test_audio.py
```

## Customization

Edit `thai_config.py` to add your own corrections:

```python
CUSTOM_DICTIONARY = {
    "ปิง": "ปิง",  # Fix misrecognized names
    "มลายู": "มาเลเซีย",
}
```

## Model Sizes

| Size | Speed | Accuracy | VRAM |
|------|-------|----------|------|
| tiny | Fastest | Good | ~1GB |
| base | Fast | Better | ~1GB |
| small | Medium | Good | ~2GB |
| medium | Slower | Best | ~5GB |
| large | Slowest | Best | ~10GB |

## Project Structure

```
~/thai-voice-dictation/
├── transcribe.py          # Main CLI tool
├── thai_processor.py      # Thai text processing
├── thai_config.py         # Customization settings
├── record_thai.py         # Microphone recording
├── generate_test_audio.py # Generate TTS test samples
├── test.sh                # Quick test script
├── samples/               # Audio samples
└── pyproject.toml         # Dependencies
```