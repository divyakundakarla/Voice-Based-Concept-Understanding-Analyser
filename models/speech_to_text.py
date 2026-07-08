"""
models/speech_to_text.py
Whisper-based speech transcription module for VBCUA.
"""

import os
import re
import streamlit as st


@st.cache_resource(show_spinner=False)
def load_whisper_model(model_size: str = "base"):
    """Load and cache the Whisper model."""
    try:
        import whisper
        model = whisper.load_model(model_size)
        return model
    except ImportError:
        st.error("openai-whisper is not installed. Run: pip install openai-whisper")
        return None

def transcribe_audio(audio_path: str, model_size: str = "base") -> dict:
    """
    Transcribe audio file using Whisper.

    Args:
        audio_path: Path to the audio file (.wav/.mp3/.m4a)
        model_size: Whisper model size ('tiny','base','small','medium','large')

    Returns:
        dict with keys: text, word_count, language, segments
    """
    model = load_whisper_model(model_size)
    if model is None:
        return _dummy_transcription()

    try:
        result = model.transcribe(audio_path, fp16=False)
        text = result.get("text", "").strip()
        words = [w for w in text.split() if w.strip()]

        return {
            "text": text,
            "word_count": len(words),
            "language": result.get("language", "en"),
            "segments": result.get("segments", []),
            "success": True,
            "error": None
        }
    except Exception as e:
        return {
            "text": "",
            "word_count": 0,
            "language": "unknown",
            "segments": [],
            "success": False,
            "error": str(e)
        }


def _dummy_transcription() -> dict:
    """Return a placeholder when model fails to load (for demo/testing)."""
    return {
        "text": "Machine learning is a subset of artificial intelligence that enables computers to learn from data without being explicitly programmed.",
        "word_count": 22,
        "language": "en",
        "segments": [],
        "success": True,
        "error": "Demo mode — Whisper not available"
    }


def count_filler_words(text: str) -> dict:
    """
    Count filler words in the transcribed text.

    Args:
        text: Transcribed text

    Returns:
        dict mapping filler_word -> count, plus total
    """
    FILLERS = ["um", "uh", "like", "you know", "basically", "literally",
               "actually", "i mean", "sort of", "kind of", "you see"]

    text_lower = text.lower()
    counts = {}
    total = 0

    for filler in FILLERS:
        pattern = r'\b' + re.escape(filler) + r'\b'
        matches = re.findall(pattern, text_lower)
        if matches:
            counts[filler] = len(matches)
            total += len(matches)

    counts["_total"] = total
    return counts


def calculate_speech_rate(word_count: int, duration_seconds: float) -> float:
    """
    Calculate words per minute.

    Args:
        word_count: Number of words spoken
        duration_seconds: Duration of audio in seconds

    Returns:
        Words per minute (float)
    """
    if duration_seconds <= 0:
        return 0.0
    return (word_count / duration_seconds) * 60
