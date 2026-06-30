"""
services/scoring.py
AI Scoring Engine for VBCUA — computes all sub-scores and overall grade.
"""

from utils.helpers import get_grade


def compute_all_scores(
    similarity_score: float,
    fluency_score: float,
    filler_count: int,
    pause_ratio: float,
    speech_rate_wpm: float,
    confidence: float,
    coverage_ratio: float,
) -> dict:
    """
    Compute full scoring breakdown.

    Weights:
        Concept Understanding (Semantic Similarity)  : 50%
        Speech Fluency                               : 25%
        Communication Quality                        : 25%

    Args:
        similarity_score  : 0–1 from Sentence-BERT
        fluency_score     : 0–100 from audio analysis
        filler_count      : total filler words used
        pause_ratio       : fraction of audio that is paused
        speech_rate_wpm   : words per minute
        confidence        : 0–1 audio confidence
        coverage_ratio    : 0–1 key concept coverage ratio

    Returns:
        dict with all sub-scores and overall score/grade
    """

    # 1. Concept Understanding Score (0–100)
    concept_score = round(similarity_score * 100, 1)

    # Boost slightly if key concept coverage is high
    concept_score = round(min(100, concept_score * 0.8 + coverage_ratio * 20), 1)

    # 2. Speech Fluency Score (already 0–100)
    fluency = round(float(fluency_score), 1)

    # 3. Communication Quality Score (0–100)
    communication_score = _communication_score(
        filler_count, pause_ratio, speech_rate_wpm, confidence
    )

    # 4. Overall Score
    overall = round(
        concept_score   * 0.50 +
        fluency         * 0.25 +
        communication_score * 0.25,
        1
    )
    overall = float(min(100, max(0, overall)))

    grade = get_grade(overall)

    return {
        "concept_score": concept_score,
        "fluency_score": fluency,
        "communication_score": communication_score,
        "overall_score": overall,
        "grade": grade,
    }


def _communication_score(
    filler_count: int,
    pause_ratio: float,
    speech_rate_wpm: float,
    confidence: float,
) -> float:
    """
    Heuristic communication quality score (0–100).
    Considers filler words, pauses, speaking pace, and voice confidence.
    """
    import numpy as np

    # Penalise too many fillers
    filler_penalty = min(filler_count * 3, 30)

    # Penalise excessive pausing (> 30%)
    pause_penalty = max(0, (pause_ratio - 0.30) * 100)

    # Reward natural speaking pace (120–160 wpm)
    if 100 <= speech_rate_wpm <= 170:
        pace_bonus = 10
    elif 80 <= speech_rate_wpm < 100 or 170 < speech_rate_wpm <= 200:
        pace_bonus = 5
    else:
        pace_bonus = 0

    base = 60
    score = base + pace_bonus + (confidence * 30) - filler_penalty - pause_penalty
    return round(float(np.clip(score, 0, 100)), 1)
