#!/usr/bin/env python3
"""Generate Thai test audio using Google TTS."""

from pathlib import Path
from gtts import gTTS

TEST_SENTENCES = [
    "สวัสดีครับ ผมชื่อสมชาย ยินดีที่ได้รู้จักครับ",
    "วันนี้อากาศดีมาก เหมาะแก่การออกไปเดินเล่นนอกบ้าน",
    "ผมกำลังพัฒนาแอปพลิเคชันสำหรับแปลงเสียงเป็นข้อความภาษาไทย",
]

def generate_test_audio():
    output_dir = Path(__file__).parent / "samples"
    output_dir.mkdir(exist_ok=True)

    for i, sentence in enumerate(TEST_SENTENCES, 1):
        output_file = output_dir / f"test_thai_{i}.mp3"

        print(f"Generating: {sentence[:30]}...")

        tts = gTTS(text=sentence, lang='th')
        tts.save(str(output_file))

        print(f"  Saved: {output_file}")

    print(f"\nGenerated {len(TEST_SENTENCES)} test audio files in samples/")

if __name__ == "__main__":
    generate_test_audio()