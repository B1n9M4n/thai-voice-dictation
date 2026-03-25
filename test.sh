#!/bin/bash
# Thai Voice Dictation - Quick Test Script

set -e

echo "========================================"
echo "THAI VOICE DICTATION TEST"
echo "========================================"

cd ~/thai-voice-dictation

# Check if recording exists
if [ -f "samples/thai_recording.wav" ]; then
    echo ""
    echo "Found existing recording: samples/thai_recording.wav"
    echo ""
    read -p "Record new audio? (y/n): " choice
    if [[ "$choice" == "y" ]]; then
        echo ""
        echo "Recording 5 seconds of Thai audio..."
        ~/.local/bin/uv run record_thai.py 5
    fi
else
    echo ""
    echo "No recording found. Recording 5 seconds of Thai audio..."
    mkdir -p samples
    ~/.local/bin/uv run record_thai.py 5
fi

echo ""
echo "========================================"
echo "TRANSCRIBING..."
echo "========================================"
echo ""

# Transcribe with small model (fast)
echo "--- Small Model (fast) ---"
~/.local/bin/uv run transcribe.py samples/thai_recording.wav --model small

echo ""
echo "========================================"
echo "Done! Try larger model for better accuracy:"
echo "  ~/.local/bin/uv run transcribe.py samples/thai_recording.wav --model medium"
echo "========================================"