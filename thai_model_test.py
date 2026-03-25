#!/usr/bin/env python3
"""Test Thai Whisper model (fine-tuned)."""

import sys
from pathlib import Path

from transformers import pipeline


def transcribe_thai_model(audio_path: str, model_size: str = "base"):
    """Transcribe using Thai-fine-tuned Whisper."""
    models = {
        "base": "juierror/whisper-base-thai",
        "tiny": "juierror/whisper-tiny-thai",
        "small": "napatswift/whisper-small-thai",
        "large": "cwany/whisper-large-v2-thai",
    }
    
    model_name = models.get(model_size, models["base"])
    
    print(f"Loading model: {model_name}")
    print(f"Transcribing: {audio_path}")
    
    pipe = pipeline(
        "automatic-speech-recognition",
        model=model_name,
        chunk_length_s=30,
        return_timestamps=True,
    )
    
    result = pipe(audio_path, language="th")
    
    return result["text"]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: uv run thai_model_test.py <audio_file> [large-v3|medium|small]")
        sys.exit(1)
    
    audio_path = sys.argv[1]
    model_size = sys.argv[2] if len(sys.argv) > 2 else "large-v3"
    
    if not Path(audio_path).exists():
        print(f"Error: File not found: {audio_path}")
        sys.exit(1)
    
    text = transcribe_thai_model(audio_path, model_size)
    
    print("\n" + "=" * 60)
    print("THAI MODEL OUTPUT:")
    print("-" * 60)
    print(text)
    print("=" * 60)