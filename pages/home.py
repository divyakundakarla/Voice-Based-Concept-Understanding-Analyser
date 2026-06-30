"""
pages/home.py
Landing page for VBCUA.
"""

import streamlit as st
from components.ui_components import feature_card, how_it_works_step


def render_home():
    # ── Hero Section ──────────────────────────────────────────────
    st.markdown("""
    <div style="text-align:center; padding: 50px 20px 30px 20px;">
        <div style="
            display:inline-block; padding: 6px 18px; border-radius: 20px;
            background: rgba(99,102,241,0.15); border: 1px solid rgba(99,102,241,0.35);
            color:#a5b4fc; font-size:0.8rem; font-weight:600; margin-bottom:20px;
        ">🎙️ AI-Powered Speech Intelligence</div>
        <h1 style="
            font-size: 3rem; font-weight: 800; margin: 10px 0;
            background: linear-gradient(135deg, #818cf8, #c084fc, #f0abfc);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            background-clip: text;
        ">Voice-Based Concept<br/>Understanding Analyser</h1>
        <p style="
            color: rgba(255,255,255,0.6); font-size: 1.15rem; max-width: 680px;
            margin: 16px auto 0 auto; line-height:1.6;
        ">
            Speak your understanding of a concept — our AI evaluates your semantic accuracy,
            speech fluency, and communication quality in real time, then delivers a complete
            performance report.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 Start Analysis", use_container_width=True, type="primary"):
            st.session_state.page = "analysis"
            st.rerun()

    st.markdown("<div style='height:50px;'></div>", unsafe_allow_html=True)

    # ── Features Section ──────────────────────────────────────────
    st.markdown("""
    <div class="section-header" style="justify-content:center; text-align:center; font-size:1.8rem;">
        ✨ Powerful Features
    </div>
    <div class="section-subtitle" style="text-align:center;">
        Everything you need to evaluate spoken concept understanding
    </div>
    """, unsafe_allow_html=True)

    f1, f2, f3 = st.columns(3)
    with f1:
        feature_card("🎤", "Speech-to-Text", "Accurate transcription powered by OpenAI Whisper, supporting multiple audio formats.")
    with f2:
        feature_card("🧠", "Semantic Similarity", "Sentence-BERT embeddings compare your explanation against expert reference answers.")
    with f3:
        feature_card("📊", "Fluency Analysis", "Detects filler words, pauses, speech rate, and vocal confidence from your audio.")

    f4, f5, f6 = st.columns(3)
    with f4:
        feature_card("🎯", "AI Scoring Engine", "Weighted scoring across concept understanding, fluency, and communication quality.")
    with f5:
        feature_card("📈", "Visual Dashboard", "Interactive charts, gauges, and circular progress indicators for instant insight.")
    with f6:
        feature_card("📄", "PDF Reports", "Download a professional, shareable report with transcript, scores, and AI feedback.")

    st.markdown("<div style='height:50px;'></div>", unsafe_allow_html=True)

    # ── How It Works Section ────────────────────────────────────────
    st.markdown("""
    <div class="section-header" style="justify-content:center; text-align:center; font-size:1.8rem;">
        🔄 How It Works
    </div>
    <div class="section-subtitle" style="text-align:center;">
        Four simple steps to evaluate your spoken understanding
    </div>
    """, unsafe_allow_html=True)

    s1, s2, s3, s4 = st.columns(4)
    with s1:
        how_it_works_step(1, "Upload Audio", "Upload a recording or record your voice explaining a concept")
    with s2:
        how_it_works_step(2, "AI Transcribes", "Whisper converts your speech into accurate text")
    with s3:
        how_it_works_step(3, "AI Analyzes", "Semantic similarity, fluency, and confidence are evaluated")
    with s4:
        how_it_works_step(4, "Get Report", "View your dashboard and download a detailed PDF report")

    st.markdown("<div style='height:40px;'></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🎯 Get Started Now", use_container_width=True, key="bottom_cta"):
            st.session_state.page = "analysis"
            st.rerun()

    st.markdown("""
    <div style="text-align:center; padding: 40px 0 10px 0; color:rgba(255,255,255,0.3); font-size:0.8rem;">
        VBCUA · Built with Streamlit, Whisper &amp; Sentence-BERT
    </div>
    """, unsafe_allow_html=True)
