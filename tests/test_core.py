"""
tests/test_core.py
Basic unit tests for VBCUA core logic (no audio/model dependencies required).

Run with: pytest tests/test_core.py -v
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.helpers import get_understanding_level, get_grade, format_duration, score_color
from services.scoring import compute_all_scores
from models.speech_to_text import count_filler_words, calculate_speech_rate
from models.audio_analysis import compute_fluency_score


def test_understanding_level_excellent():
    level, color = get_understanding_level(0.85)
    assert level == "Excellent"


def test_understanding_level_poor():
    level, color = get_understanding_level(0.10)
    assert level == "Poor"


def test_grade_mapping():
    assert get_grade(95) == "A+"
    assert get_grade(85) == "A"
    assert get_grade(75) == "B"
    assert get_grade(65) == "C"
    assert get_grade(40) == "D"


def test_format_duration():
    assert format_duration(65) == "01:05"
    assert format_duration(5) == "00:05"


def test_count_filler_words():
    text = "Um, so this is like, you know, a basic concept, um."
    result = count_filler_words(text)
    assert result["_total"] > 0
    assert "um" in result
    assert result["um"] == 2


def test_count_filler_words_clean():
    text = "Machine learning enables computers to learn patterns from data."
    result = count_filler_words(text)
    assert result["_total"] == 0


def test_calculate_speech_rate():
    rate = calculate_speech_rate(word_count=150, duration_seconds=60)
    assert rate == 150.0


def test_calculate_speech_rate_zero_duration():
    rate = calculate_speech_rate(word_count=10, duration_seconds=0)
    assert rate == 0.0


def test_compute_fluency_score_range():
    score = compute_fluency_score(
        filler_count=2, pause_ratio=0.15, speech_rate_wpm=140, confidence=0.8
    )
    assert 0 <= score <= 100


def test_compute_all_scores():
    result = compute_all_scores(
        similarity_score=0.75,
        fluency_score=80,
        filler_count=2,
        pause_ratio=0.15,
        speech_rate_wpm=140,
        confidence=0.8,
        coverage_ratio=0.6,
    )
    assert "overall_score" in result
    assert "grade" in result
    assert 0 <= result["overall_score"] <= 100
    assert result["grade"] in ["A+", "A", "B", "C", "D"]


def test_score_color():
    assert score_color(90) == "#00C851"
    assert score_color(20) == "#ff4444"


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
