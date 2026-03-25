#!/usr/bin/env python3
"""Record Thai audio for testing."""

import sys
import time
from pathlib import Path

import sounddevice as sd
import soundfile as sf


def record_audio(duration: int = 5, sample_rate: int = 16000) -> str:
    output_dir = Path(__file__).parent / "samples"
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / "thai_recording.wav"
    
    print(f"\n{'='*50}")
    print("RECORDING THAI AUDIO")
    print(f"{'='*50}")
    print(f"Duration: {duration} seconds")
    print("\nStarting in 2 seconds...")
    time.sleep(2)
    
    print("\n🔴 RECORDING NOW - SPEAK THAI!")
    
    recording = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype='float32'
    )
    sd.wait()
    
    print("✓ Recording complete!")
    
    sf.write(str(output_file), recording, sample_rate)
    print(f"\nSaved to: {output_file}")
    
    return str(output_file)


if __name__ == "__main__":
    duration = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    audio_file = record_audio(duration)
    
    print(f"\n{'='*50}")
    print("NEXT: Transcribe your recording")
    print(f"{'='*50}")
    print(f"\n  ~/.local/bin/uv run transcribe.py {audio_file}")