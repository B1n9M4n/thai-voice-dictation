"""Enhanced Thai text processing with context awareness."""

import re
from pythainlp.tokenize import word_tokenize
from pythainlp.util import normalize as thai_normalize

from thai_config import (
    THAI_FILLER_WORDS,
    CUSTOM_DICTIONARY,
    THAI_ASR_FIXES,
    CONTEXT_PROFILES,
    MALE_PARTICLES,
    FEMALE_PARTICLES,
)


def apply_custom_dictionary(text: str) -> str:
    for wrong, correct in CUSTOM_DICTIONARY.items():
        if wrong != correct:
            text = text.replace(wrong, correct)
    return text


def apply_asr_fixes(text: str) -> str:
    """Fix common ASR misrecognitions for Thai."""
    for wrong, correct, context_hint in THAI_ASR_FIXES:
        if context_hint is None:
            text = text.replace(wrong, correct)
        else:
            if any(hint in text for hint in context_hint):
                text = text.replace(wrong, correct)
    return text


def process_thai_text(
    raw_text: str,
    add_spaces: bool = True,
    context: str = "general",
    remove_fillers: bool = True,
) -> str:
    """
    Process Thai text with context-aware options.

    Args:
        raw_text: Raw transcription text
        add_spaces: Add spaces between words
        context: Context profile (general, email, chat, formal)
        remove_fillers: Remove hesitation sounds

    Returns:
        Processed Thai text
    """
    profile = CONTEXT_PROFILES.get(context, CONTEXT_PROFILES["general"])

    # 1. Normalize Thai characters
    text = thai_normalize(raw_text)

    # 2. Apply custom dictionary
    text = apply_custom_dictionary(text)

    # 3. Fix ASR misrecognitions
    text = apply_asr_fixes(text)

    # 4. Remove filler words (if enabled)
    if remove_fillers and profile.get("remove_fillers", True):
        for filler in THAI_FILLER_WORDS:
            text = re.sub(rf"\s*{filler}\s*", " ", text)

    # 4. Word segmentation
    words = word_tokenize(text, engine="newmm")

    # 5. Join with spaces or without
    if add_spaces:
        result = " ".join(words)
    else:
        result = "".join(words)

    # 6. Clean up multiple spaces
    result = re.sub(r"\s+", " ", result).strip()

    # 7. Add politeness particle for email/formal context
    if profile.get("add_politeness") and not any(
        p in result for p in MALE_PARTICLES + FEMALE_PARTICLES
    ):
        default_particle = profile.get("default_particle", "ครับ")
        result = result.rstrip("。.!?:;")
        result += f" {default_particle}"

    return result


def add_punctuation(text: str, context: str = "general") -> str:
    """Add context-appropriate punctuation."""
    text = text.strip()

    if context in ["email", "formal"]:
        if text and text[-1] not in "。.!?:;":
            text += " 。"
    elif context == "chat":
        # Chat can be more casual, no forced punctuation
        pass
    else:
        if text and text[-1] not in "。.!?:;":
            text += " 。"

    return text


def thai_dictation_pipeline(
    raw_text: str,
    context: str = "general",
    add_spaces: bool = True,
    remove_fillers: bool = True,
) -> dict:
    """
    Complete Thai dictation processing pipeline.

    Args:
        raw_text: Raw transcription from ASR
        context: Context profile
        add_spaces: Add word spacing
        remove_fillers: Remove hesitation sounds

    Returns:
        dict with processing results
    """
    processed = process_thai_text(
        raw_text,
        add_spaces=add_spaces,
        context=context,
        remove_fillers=remove_fillers,
    )

    final = add_punctuation(processed, context=context)

    return {
        "raw_text": raw_text,
        "processed_text": processed,
        "final_text": final,
    }