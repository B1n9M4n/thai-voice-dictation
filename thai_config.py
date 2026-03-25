"""Thai-specific configuration and features."""

# Thai hesitation sounds to remove (actual fillers, not sentence particles)
THAI_FILLER_WORDS = [
    "อ่ม", "อืม", "เอ่อ", "อืมม", "อ่ะ", "เอ่",
    "แม่เจ้า", "โอ้โห", "อืมม์"
]

# Custom dictionary for common misrecognitions
CUSTOM_DICTIONARY = {
    "ปิง": "ปิง",
}

# Common Thai ASR misrecognition patterns (Whisper-specific)
THAI_ASR_FIXES = [
    ("เยิน", "เย็น", None),  # evening (common error)
    ("ยินฟาด", "เย็นฟาด", None),  # evening hits
    ("ชาวฟาด", "เช้าฟาด", None),  # morning hits
    ("ชาวฝาด", "เช้าฟาด", None),  # morning hits (variant)
    ("ฝาด", "ฟาด", ["ผัด", "ฟัก"]),  # hits (when near paddle/gourd)
    ("ฟาต", "ฟาด", None),  # hits
    ("พัด", "ผัด", ["ฟัก"]),  # paddle (when near gourd)
    ("ภัต", "ผัด", None),  # paddle (variant)
]

# Thai politeness particles by gender
MALE_PARTICLES = ["ครับ", "ครับผม", "ฮะ"]
FEMALE_PARTICLES = ["ค่ะ", "คะ", "จ้ะ"]
NEUTRAL_PARTICLES = ["นะ", "จ้ะ", "สิ"]

# Context profiles
CONTEXT_PROFILES = {
    "general": {
        "add_politeness": False,
        "formal_spacing": True,
        "remove_fillers": True,
    },
    "email": {
        "add_politeness": True,
        "formal_spacing": True,
        "remove_fillers": True,
        "default_particle": "ครับ",  # or "ค่ะ" for female
    },
    "chat": {
        "add_politeness": False,
        "formal_spacing": False,
        "remove_fillers": False,
    },
    "formal": {
        "add_politeness": True,
        "formal_spacing": True,
        "remove_fillers": True,
        "default_particle": "ครับ",
    },
}

# Thai number words (for potential number conversion)
THAI_NUMBERS = {
    "ศูนย์": 0, "หนึ่ง": 1, "สอง": 2, "สาม": 3, "สี่": 4,
    "ห้า": 5, "หก": 6, "เจ็ด": 7, "แปด": 8, "เก้า": 9,
    "สิบ": 10, "ร้อย": 100, "พัน": 1000, "หมื่น": 10000,
    "แสน": 100000, "ล้าน": 1000000,
}

# Common Thai abbreviations
THAI_ABBREVIATIONS = {
    "ม.": "มหาวิทยาลัย",
    "จ.": "จังหวัด",
    "อ.": "อำเภอ",
    "ต.": "ตำบล",
    "พ.ศ.": "พุทธศักราช",
    "ค.ศ.": "คริสต์ศักราช",
}