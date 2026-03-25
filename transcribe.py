#!/usr/bin/env python3
"""
Thai Voice Dictation using MLX-Whisper (Apple Silicon Optimized)

This module provides:
1. Thai speech-to-text using MLX-Whisper (runs locally on Apple Silicon)
2. Thai text processing (word segmentation, normalization)
3. Post-processing (filler removal, punctuation)

Usage:
    uv run transcribe.py audio_file.mp3
    uv run transcribe.py --live  # Record from microphone
"""

import argparse
import sys
from pathlib import Path

import mlx_whisper
from thai_processor import process_thai_text, add_punctuation


def transcribe_thai(audio_path: str, model_size: str = "small") -> dict:
    """
    Transcribe Thai audio using MLX-Whisper.
    
    Args:
        audio_path: Path to audio file (mp3, wav, m4a, etc.)
        model_size: Model size - "tiny", "base", "small", "medium", "large"
        
    Returns:
        dict with 'text', 'segments', 'language', 'duration'
    """
    # MLX-Whisper uses HuggingFace model names
    # "small" = mlx-community/whisper-small-mlx
    model_name = f"mlx-community/whisper-{model_size}-mlx"
    
    print(f"Loading model: {model_name}")
    print(f"Transcribing: {audio_path}")
    
    result = mlx_whisper.transcribe(
        audio_path,
        path_or_hf_repo=model_name,
        language="th",  # Force Thai language
        verbose=True
    )
    
    return result


def dictation_pipeline(audio_path: str, model_size: str = "small", context: str = "general") -> dict:
    """
    Complete Thai dictation pipeline.
    
    Args:
        audio_path: Path to audio file
        model_size: Whisper model size
        context: Context mode (general, email, chat, formal)
        
    Returns:
        dict with 'raw_text', 'processed_text', 'final_text'
    """
    # 1. Transcribe
    result = transcribe_thai(audio_path, model_size)
    raw_text = result.get("text", "")
    
    # 2. Process Thai text with context
    processed_text = process_thai_text(raw_text, context=context)
    
    # 3. Add punctuation with context
    final_text = add_punctuation(processed_text, context=context)
    
    return {
        "raw_text": raw_text,
        "processed_text": processed_text,
        "final_text": final_text,
        "segments": result.get("segments", []),
        "language": result.get("language", "th")
    }


def live_record(duration: int = 10, sample_rate: int = 16000) -> str:
    """
    Record audio from microphone.
    
    Args:
        duration: Recording duration in seconds
        sample_rate: Audio sample rate
        
    Returns:
        Path to recorded audio file
    """
    try:
        import sounddevice as sd
        import soundfile as sf
        import tempfile
    except ImportError:
        print("Error: Install recording dependencies:")
        print("  uv add sounddevice soundfile")
        sys.exit(1)
    
    print(f"Recording for {duration} seconds...")
    print("Speak now!")
    
    recording = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1
    )
    sd.wait()
    
    # Save to temp file
    temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    sf.write(temp_file.name, recording, sample_rate)
    
    print(f"Saved to: {temp_file.name}")
    return temp_file.name


def main():
    parser = argparse.ArgumentParser(
        description="Thai Voice Dictation using MLX-Whisper"
    )
    parser.add_argument(
        "audio_file",
        nargs="?",
        help="Path to audio file (mp3, wav, m4a, etc.)"
    )
    parser.add_argument(
        "--model", "-m",
        default="small",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper model size (default: small)"
    )
    parser.add_argument(
        "--live", "-l",
        action="store_true",
        help="Record from microphone"
    )
    parser.add_argument(
        "--duration", "-d",
        type=int,
        default=10,
        help="Recording duration in seconds (default: 10)"
    )
    parser.add_argument(
        "--no-spaces",
        action="store_true",
        help="Don't add spaces between Thai words"
    )
    parser.add_argument(
        "--raw",
        action="store_true",
        help="Output raw transcription only (no processing)"
    )
    parser.add_argument(
        "--context", "-c",
        default="general",
        choices=["general", "email", "chat", "formal"],
        help="Context mode: general, email (adds ครับ), chat (casual), formal"
    )
    
    args = parser.parse_args()
    
    # Get audio file
    if args.live:
        audio_path = live_record(args.duration)
    elif args.audio_file:
        audio_path = args.audio_file
    else:
        parser.print_help()
        print("\nError: Provide audio file or use --live")
        sys.exit(1)
    
    # Check file exists
    if not Path(audio_path).exists():
        print(f"Error: File not found: {audio_path}")
        sys.exit(1)
    
    # Run dictation pipeline
    result = dictation_pipeline(audio_path, args.model, args.context)
    
    # Output
    print("\n" + "="*60)
    print(f"RAW TRANSCRIPTION (context: {args.context}):")
    print("-"*60)
    print(result["raw_text"])
    
    if not args.raw:
        print("\n" + "="*60)
        print("PROCESSED (segmented, cleaned):")
        print("-"*60)
        print(result["processed_text"])
        
        print("\n" + "="*60)
        print("FINAL OUTPUT:")
        print("-"*60)
        print(result["final_text"])
    
    print("="*60)


if __name__ == "__main__":
    main()