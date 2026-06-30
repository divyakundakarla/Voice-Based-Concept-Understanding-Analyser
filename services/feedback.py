"""
services/feedback.py
AI Feedback Generator for VBCUA — produces detailed, personalised feedback.
"""

from utils.helpers import get_grade


def generate_feedback(
    concept_name: str,
    overall_score: float,
    concept_score: float,
    fluency_score: float,
    communication_score: float,
    covered_concepts: list,
    missing_concepts: list,
    filler_count: int,
    speech_rate_wpm: float,
    pause_ratio: float,
    confidence: float,
    grade: str,
) -> dict:
    """
    Generate structured AI feedback based on all analysis results.

    Returns:
        dict with strengths, weaknesses, improvements, practice_recommendations, summary
    """

    strengths = _identify_strengths(
        concept_score, fluency_score, communication_score,
        covered_concepts, filler_count, confidence
    )

    weaknesses = _identify_weaknesses(
        concept_score, fluency_score, communication_score,
        missing_concepts, filler_count, speech_rate_wpm, pause_ratio
    )

    improvements = _suggest_improvements(
        missing_concepts, filler_count, speech_rate_wpm,
        pause_ratio, concept_score, fluency_score
    )

    practice = _practice_recommendations(overall_score, concept_name)

    summary = _generate_summary(
        concept_name, grade, overall_score, concept_score,
        fluency_score, communication_score
    )

    return {
        "strengths": strengths,
        "weaknesses": weaknesses,
        "improvements": improvements,
        "practice_recommendations": practice,
        "summary": summary,
    }


# ─────────────────────────────────────────────
# Internal helpers
# ─────────────────────────────────────────────

def _identify_strengths(
    concept_score, fluency_score, communication_score,
    covered_concepts, filler_count, confidence
) -> list:
    strengths = []

    if concept_score >= 70:
        strengths.append(
            f"Strong conceptual understanding — your explanation covers the core ideas well "
            f"({concept_score:.0f}/100 concept score)."
        )
    if fluency_score >= 70:
        strengths.append("Good speech fluency with a natural and consistent speaking pace.")
    if communication_score >= 70:
        strengths.append("Effective communication — your delivery is clear and confident.")
    if len(covered_concepts) >= 5:
        strengths.append(
            f"You mentioned {len(covered_concepts)} key technical concepts: "
            f"{', '.join(covered_concepts[:5])}{'...' if len(covered_concepts) > 5 else ''}."
        )
    if filler_count == 0:
        strengths.append("Excellent speech quality — zero filler words detected.")
    elif filler_count <= 3:
        strengths.append("Minimal use of filler words, showing good preparation.")
    if confidence >= 0.7:
        strengths.append(
            f"Strong vocal confidence ({confidence * 100:.0f}%) throughout the explanation."
        )

    if not strengths:
        strengths.append(
            "You made a genuine attempt to explain the concept — keep practising!"
        )
    return strengths


def _identify_weaknesses(
    concept_score, fluency_score, communication_score,
    missing_concepts, filler_count, speech_rate_wpm, pause_ratio
) -> list:
    weaknesses = []

    if concept_score < 50:
        weaknesses.append(
            "The explanation lacks depth on the core concept — "
            "many important ideas were not mentioned."
        )
    if missing_concepts:
        top_missing = missing_concepts[:5]
        weaknesses.append(
            f"Key concepts not covered: {', '.join(top_missing)}. "
            "These are fundamental to a complete explanation."
        )
    if filler_count > 5:
        weaknesses.append(
            f"High filler word usage ({filler_count} detected) reduces overall clarity."
        )
    if fluency_score < 50:
        weaknesses.append(
            "Speech fluency needs improvement — work on maintaining a steady pace."
        )
    if pause_ratio > 0.40:
        weaknesses.append(
            f"Extended pauses ({pause_ratio * 100:.0f}% of speech) suggest hesitation "
            "or uncertainty about the topic."
        )
    if speech_rate_wpm < 80:
        weaknesses.append(
            f"Speaking rate is too slow ({speech_rate_wpm:.0f} wpm). "
            "Aim for 120–160 wpm for natural delivery."
        )
    elif speech_rate_wpm > 200:
        weaknesses.append(
            f"Speaking rate is too fast ({speech_rate_wpm:.0f} wpm). "
            "Slow down to improve listener comprehension."
        )
    if communication_score < 50:
        weaknesses.append(
            "Communication quality needs development — focus on structure and clarity."
        )

    return weaknesses


def _suggest_improvements(
    missing_concepts, filler_count, speech_rate_wpm,
    pause_ratio, concept_score, fluency_score
) -> list:
    improvements = []

    if missing_concepts:
        improvements.append(
            f"Study and articulate: {', '.join(missing_concepts[:4])}. "
            "Try explaining each in one sentence first."
        )
    if filler_count > 3:
        improvements.append(
            "Replace filler words with deliberate pauses. "
            "Record yourself and listen back to identify habits."
        )
    if concept_score < 60:
        improvements.append(
            "Create a mind-map of the concept linking definitions, examples, and applications. "
            "Re-read textbook sections or watch short explainer videos."
        )
    if speech_rate_wpm < 100:
        improvements.append(
            "Practise reading aloud at a faster pace. "
            "Use a metronome or speech-pacing app to build rhythm."
        )
    elif speech_rate_wpm > 190:
        improvements.append(
            "Practise pausing after key sentences. "
            "Use the PREP framework: Point → Reason → Example → Point."
        )
    if pause_ratio > 0.35:
        improvements.append(
            "Improve topic recall by creating flashcards "
            "with key terms and practising until retrieval feels automatic."
        )
    if fluency_score < 60:
        improvements.append(
            "Record daily 60-second explanations of random topics to build fluency muscle memory."
        )

    improvements.append(
        "Use the Feynman Technique: explain the concept to an imaginary audience "
        "as simply as possible, then identify gaps and revisit those areas."
    )
    return improvements


def _practice_recommendations(overall_score: float, concept_name: str) -> list:
    recs = [
        f"🎯 Review official resources or textbook chapters on '{concept_name}'.",
        "🗣️ Practise explaining '{concept_name}' out loud daily for 2 minutes.",
        "📝 Write a one-page summary of the concept without looking at notes.",
    ]

    if overall_score < 50:
        recs += [
            "📚 Start with foundational material — watch 2–3 introductory videos.",
            "👥 Form a study group and take turns explaining concepts to each other.",
        ]
    elif overall_score < 75:
        recs += [
            "🔁 Use spaced repetition (Anki cards) for key terms and definitions.",
            "🧩 Try linking the concept to real-world examples you encounter daily.",
        ]
    else:
        recs += [
            "🚀 Challenge yourself to explain the concept at three levels: "
            "beginner, intermediate, and expert.",
            "✍️ Write a blog post or teach a peer — teaching deepens understanding.",
        ]
    return recs


def _generate_summary(
    concept_name, grade, overall_score,
    concept_score, fluency_score, communication_score
) -> str:
    grade_desc = {
        "A+": "outstanding",
        "A":  "excellent",
        "B":  "good",
        "C":  "average",
        "D":  "below average",
    }.get(grade, "")

    return (
        f"Your performance on '{concept_name}' is {grade_desc} (Grade {grade}, "
        f"Overall: {overall_score:.0f}/100). "
        f"Concept understanding scored {concept_score:.0f}/100, "
        f"speech fluency {fluency_score:.0f}/100, and "
        f"communication quality {communication_score:.0f}/100. "
        "Review the strengths and improvement areas above to plan your next study session."
    )
