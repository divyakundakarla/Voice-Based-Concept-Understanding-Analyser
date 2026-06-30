"""
models/semantic_analysis.py
Sentence-BERT semantic similarity analysis for VBCUA.
"""

import re
import streamlit as st
from utils.helpers import load_concepts


@st.cache_resource(show_spinner=False)
def load_sbert_model():
    """Load and cache the Sentence-BERT model."""
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer("all-MiniLM-L6-v2")
        return model
    except ImportError:
        st.warning("sentence-transformers not installed. Using fallback similarity.")
        return None


def compute_semantic_similarity(student_text: str, concept_name: str) -> dict:
    """
    Compute semantic similarity between student text and reference explanation.

    Args:
        student_text: Transcribed student explanation
        concept_name: Selected concept key from concepts.json

    Returns:
        dict with similarity_score (0–1), understanding_analysis, key_concept_coverage
    """
    concepts = load_concepts()
    if concept_name not in concepts:
        return {"error": f"Concept '{concept_name}' not found"}

    reference = concepts[concept_name]["reference"]
    key_concepts = concepts[concept_name].get("key_concepts", [])

    # Compute cosine similarity with SBERT
    model = load_sbert_model()
    if model is not None:
        similarity = _sbert_similarity(model, student_text, reference)
    else:
        similarity = _keyword_fallback_similarity(student_text, reference)

    # Key concept coverage
    coverage = _check_key_concepts(student_text, key_concepts)

    return {
        "similarity_score": round(similarity, 4),
        "similarity_pct": round(similarity * 100, 1),
        "reference_text": reference,
        "key_concepts": key_concepts,
        "covered_concepts": coverage["covered"],
        "missing_concepts": coverage["missing"],
        "coverage_ratio": coverage["ratio"],
        "success": True
    }


def _sbert_similarity(model, text_a: str, text_b: str) -> float:
    """Compute cosine similarity between two texts using SBERT embeddings."""
    import numpy as np
    embeddings = model.encode([text_a, text_b], convert_to_numpy=True)
    # Cosine similarity
    dot = np.dot(embeddings[0], embeddings[1])
    norm = np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1])
    if norm == 0:
        return 0.0
    return float(dot / norm)


def _keyword_fallback_similarity(student_text: str, reference: str) -> float:
    """Simple keyword-overlap fallback when SBERT is unavailable."""
    import re
    def tokenize(t):
        return set(re.findall(r'\b[a-z]{3,}\b', t.lower()))

    student_words = tokenize(student_text)
    ref_words = tokenize(reference)
    if not ref_words:
        return 0.0
    intersection = student_words & ref_words
    return len(intersection) / len(ref_words)


def _check_key_concepts(student_text: str, key_concepts: list) -> dict:
    """Check which key concepts appear in student text."""
    text_lower = student_text.lower()
    covered = []
    missing = []
    for kc in key_concepts:
        if kc.lower() in text_lower:
            covered.append(kc)
        else:
            missing.append(kc)
    ratio = len(covered) / len(key_concepts) if key_concepts else 0
    return {"covered": covered, "missing": missing, "ratio": round(ratio, 3)}


def extract_extra_info(student_text: str, reference: str) -> list[str]:
    """
    Find sentences in student text that contain unique information
    not closely related to the reference (potential extra points or errors).
    """
    import re
    student_sentences = [s.strip() for s in re.split(r'[.!?]', student_text) if len(s.strip()) > 20]
    ref_words = set(re.findall(r'\b[a-z]{4,}\b', reference.lower()))
    extra = []
    for sent in student_sentences:
        sent_words = set(re.findall(r'\b[a-z]{4,}\b', sent.lower()))
        overlap = len(sent_words & ref_words) / max(len(sent_words), 1)
        if overlap < 0.2:
            extra.append(sent)
    return extra[:3]   # return top 3 unique sentences
