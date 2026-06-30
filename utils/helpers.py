"""
utils/helpers.py
General utility functions for VBCUA
"""

import json
import os
import time
import streamlit as st
from pathlib import Path


def load_concepts() -> dict:
    """Load predefined concept data from JSON file."""
    data_path = Path(__file__).parent.parent / "data" / "concepts.json"
    with open(data_path, "r") as f:
        return json.load(f)


def get_understanding_level(similarity_score: float) -> tuple[str, str]:
    """
    Map similarity score to understanding level and color.
    Returns (level_label, color_hex)
    """
    if similarity_score >= 0.75:
        return "Excellent", "#00C851"
    elif similarity_score >= 0.55:
        return "Good", "#33b5e5"
    elif similarity_score >= 0.35:
        return "Average", "#FF8800"
    else:
        return "Poor", "#ff4444"


def get_grade(overall_score: float) -> str:
    """Convert overall score (0-100) to letter grade."""
    if overall_score >= 90:
        return "A+"
    elif overall_score >= 80:
        return "A"
    elif overall_score >= 70:
        return "B"
    elif overall_score >= 60:
        return "C"
    else:
        return "D"


def format_duration(seconds: float) -> str:
    """Format seconds into mm:ss string."""
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"


def save_temp_audio(audio_bytes: bytes, suffix: str = ".wav") -> str:
    """Save uploaded audio bytes to a temp file, return path."""
    import tempfile
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp.write(audio_bytes)
    tmp.close()
    return tmp.name


def cleanup_temp_file(path: str):
    """Remove a temp file if it exists."""
    try:
        if path and os.path.exists(path):
            os.remove(path)
    except Exception:
        pass


def score_color(score: float) -> str:
    """Return hex color for a 0-100 score."""
    if score >= 80:
        return "#00C851"
    elif score >= 60:
        return "#33b5e5"
    elif score >= 40:
        return "#FF8800"
    else:
        return "#ff4444"


def inject_custom_css():
    """Inject global custom CSS for the app."""
    st.markdown("""
    <style>
    /* ===== GLOBAL ===== */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
        min-height: 100vh;
    }
    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #0f0f1a 100%);
        border-right: 1px solid rgba(99,102,241,0.2);
    }

    /* ===== METRIC CARDS ===== */
    .metric-card {
        background: linear-gradient(135deg, rgba(99,102,241,0.15), rgba(139,92,246,0.10));
        border: 1px solid rgba(99,102,241,0.3);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        margin-bottom: 16px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(99,102,241,0.25);
    }
    .metric-card .label {
        color: rgba(255,255,255,0.6);
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 6px;
    }
    .metric-card .value {
        color: #ffffff;
        font-size: 2rem;
        font-weight: 700;
    }
    .metric-card .sub {
        color: rgba(255,255,255,0.5);
        font-size: 0.75rem;
        margin-top: 4px;
    }

    /* ===== GRADIENT CARDS ===== */
    .gradient-card {
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        border: 1px solid rgba(255,255,255,0.08);
    }
    .gradient-card-purple {
        background: linear-gradient(135deg, rgba(139,92,246,0.2), rgba(99,102,241,0.1));
    }
    .gradient-card-blue {
        background: linear-gradient(135deg, rgba(59,130,246,0.2), rgba(6,182,212,0.1));
    }
    .gradient-card-green {
        background: linear-gradient(135deg, rgba(16,185,129,0.2), rgba(5,150,105,0.1));
    }
    .gradient-card-orange {
        background: linear-gradient(135deg, rgba(245,158,11,0.2), rgba(239,68,68,0.1));
    }

    /* ===== SECTION HEADERS ===== */
    .section-header {
        font-size: 1.4rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .section-subtitle {
        color: rgba(255,255,255,0.5);
        font-size: 0.9rem;
        margin-bottom: 20px;
    }

    /* ===== PILL BADGES ===== */
    .pill {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 600;
        margin: 3px;
    }
    .pill-green  { background: rgba(16,185,129,0.2); color: #10b981; border: 1px solid rgba(16,185,129,0.4); }
    .pill-red    { background: rgba(239,68,68,0.2);  color: #ef4444; border: 1px solid rgba(239,68,68,0.4); }
    .pill-blue   { background: rgba(59,130,246,0.2); color: #3b82f6; border: 1px solid rgba(59,130,246,0.4); }
    .pill-orange { background: rgba(245,158,11,0.2); color: #f59e0b; border: 1px solid rgba(245,158,11,0.4); }

    /* ===== STEP BADGES ===== */
    .step-badge {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white;
        width: 36px; height: 36px;
        border-radius: 50%;
        display: inline-flex; align-items: center; justify-content: center;
        font-weight: 700; font-size: 1rem;
        margin-right: 12px;
    }

    /* ===== CIRCULAR SCORE ===== */
    .circular-score {
        display: flex; flex-direction: column;
        align-items: center; justify-content: center;
        padding: 20px;
    }
    .score-ring {
        width: 120px; height: 120px;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        margin-bottom: 12px;
        font-size: 2rem; font-weight: 800; color: white;
    }

    /* ===== STREAMLIT OVERRIDES ===== */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 28px !important;
        font-weight: 600 !important;
        transition: all 0.2s !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(99,102,241,0.4) !important;
    }
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #6366f1, #8b5cf6) !important;
    }
    .stTextArea textarea, .stSelectbox select {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(99,102,241,0.3) !important;
        color: white !important;
        border-radius: 10px !important;
    }
    div[data-testid="stExpander"] {
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(99,102,241,0.2) !important;
        border-radius: 12px !important;
    }
    </style>
    """, unsafe_allow_html=True)
