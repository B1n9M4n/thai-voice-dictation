#!/usr/bin/env python3
"""Quick demo of Thai voice dictation pipeline."""

from transcribe import process_thai_text, add_punctuation

# Simulate raw Whisper output (Thai transcription without spaces)
sample_outputs = [
    "สวัสดีครับผมชื่อสมชายอยากทดสอบระบบแปลงเสียงเป็นข้อความ",
    "วันนี้อากาศดีมากเหมาะแก่การออกไปเดินเล่นนอกบ้าน",
    "ผมอ่มอืมกำลังพัฒนาแอปพลิเคชันสำหรับภาษาไทย",
]

print("=" * 60)
print("THAI VOICE DICTATION PIPELINE DEMO")
print("=" * 60)
print()

for i, raw in enumerate(sample_outputs, 1):
    print(f"Sample {i}:")
    print("-" * 40)
    print(f"Raw (no spaces):     {raw}")
    
    processed = process_thai_text(raw)
    print(f"Segmented:           {processed}")
    
    final = add_punctuation(processed)
    print(f"Final (punctuated):  {final}")
    print()

print("=" * 60)
print("Ready to test with real audio!")
print()
print("Usage:")
print("  ~/.local/bin/uv run transcribe.py your_audio.mp3")
print("  ~/.local/bin/uv run transcribe.py --live --duration 5")
print("=" * 60)