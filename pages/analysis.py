"""
pages/analysis.py
Audio upload, transcription, and analysis trigger page for VBCUA.
"""

import streamlit as st
from utils.helpers import load_concepts, save_temp_audio, cleanup_temp_file, format_duration
from components.ui_components import section_header, step_header, error_box, success_box
from models.speech_to_text import transcribe_audio, count_filler_words, calculate_speech_rate
from models.audio_analysis import analyze_audio, compute_fluency_score
from models.semantic_analysis import compute_semantic_similarity, extract_extra_info
from services.scoring import compute_all_scores
from services.feedback import generate_feedback


def render_analysis():
    section_header("🎙️ Voice Analysis", "Upload your audio and let AI evaluate your understanding", "")

    if st.button("← Back to Home"):
        st.session_state.page = "home"
        st.rerun()

    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

    # ── Student name & concept selection ────────────────────────────
    col1, col2 = st.columns(2)
    with col1:
        student_name = st.text_input("👤 Your Name", value=st.session_state.get("student_name", ""))
        st.session_state.student_name = student_name
    with col2:
        concepts = load_concepts()
        concept_name = st.selectbox("📘 Select a Concept to Explain", list(concepts.keys()))
        st.session_state.concept_name = concept_name

    with st.expander("📖 View reference explanation for this concept"):
        st.write(concepts[concept_name]["reference"])
        st.caption("Key concepts: " + ", ".join(concepts[concept_name]["key_concepts"]))

    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

    # ── Audio Upload ─────────────────────────────────────────────────
    step_header(1, "Upload Your Audio", "Supported formats: .wav, .mp3, .m4a")

    uploaded_file = st.file_uploader(
        "Drag and drop your audio file here",
        type=["wav", "mp3", "m4a"],
        label_visibility="collapsed"
    )

    audio_path = None
    if uploaded_file is not None:
        audio_bytes = uploaded_file.read()
        suffix = "." + uploaded_file.name.split(".")[-1]
        audio_path = save_temp_audio(audio_bytes, suffix=suffix)
        st.session_state.audio_path = audio_path
        st.session_state.audio_filename = uploaded_file.name

        st.audio(audio_bytes)
        success_box(f"Audio uploaded: {uploaded_file.name}")

    elif st.session_state.get("audio_path"):
        audio_path = st.session_state.audio_path

    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

    # ── Run Analysis Button ────────────────────────────────────────
    disabled = audio_path is None or not student_name.strip()
    if disabled and audio_path is None:
        st.info("👆 Please upload an audio file to begin.")
    elif disabled and not student_name.strip():
        st.info("👆 Please enter your name to begin.")

    if st.button("🧠 Run Full AI Analysis", disabled=disabled, type="primary", use_container_width=True):
        run_full_analysis(audio_path, concept_name, student_name)


def run_full_analysis(audio_path: str, concept_name: str, student_name: str):
    """Execute the complete analysis pipeline and store results in session state."""

    progress = st.progress(0, text="Starting analysis...")

    try:
        # Step 1: Transcription
        progress.progress(15, text="🎤 Transcribing speech with Whisper...")
        transcription = transcribe_audio(audio_path)
        if not transcription["success"]:
            error_box(f"Transcription failed: {transcription.get('error')}")
            return

        # Step 2: Audio signal analysis
        progress.progress(35, text="🔊 Analyzing audio signal...")
        audio_features = analyze_audio(audio_path)
        if not audio_features.get("success"):
            error_box(f"Audio analysis failed: {audio_features.get('error')}")
            return

        # Step 3: Semantic similarity
        progress.progress(55, text="🧠 Computing semantic similarity...")
        semantic_result = compute_semantic_similarity(transcription["text"], concept_name)

        # Step 4: Fluency metrics
        progress.progress(70, text="📊 Evaluating speech fluency...")
        filler_counts = count_filler_words(transcription["text"])
        speech_rate = calculate_speech_rate(transcription["word_count"], audio_features["duration"])
        fluency_score = compute_fluency_score(
            filler_count=filler_counts["_total"],
            pause_ratio=audio_features["pause_ratio"],
            speech_rate_wpm=speech_rate,
            confidence=audio_features["confidence"],
        )

        # Step 5: Scoring engine
        progress.progress(85, text="🎯 Calculating final scores...")
        scores = compute_all_scores(
            similarity_score=semantic_result["similarity_score"],
            fluency_score=fluency_score,
            filler_count=filler_counts["_total"],
            pause_ratio=audio_features["pause_ratio"],
            speech_rate_wpm=speech_rate,
            confidence=audio_features["confidence"],
            coverage_ratio=semantic_result["coverage_ratio"],
        )

        # Step 6: Feedback generation
        progress.progress(95, text="💡 Generating AI feedback...")
        feedback = generate_feedback(
            concept_name=concept_name,
            overall_score=scores["overall_score"],
            concept_score=scores["concept_score"],
            fluency_score=scores["fluency_score"],
            communication_score=scores["communication_score"],
            covered_concepts=semantic_result["covered_concepts"],
            missing_concepts=semantic_result["missing_concepts"],
            filler_count=filler_counts["_total"],
            speech_rate_wpm=speech_rate,
            pause_ratio=audio_features["pause_ratio"],
            confidence=audio_features["confidence"],
            grade=scores["grade"],
        )

        extra_info = extract_extra_info(transcription["text"], semantic_result["reference_text"])

        progress.progress(100, text="✅ Analysis complete!")

        # Store everything in session state
        st.session_state.analysis_results = {
            "student_name": student_name,
            "concept_name": concept_name,
            "transcription": transcription,
            "audio_features": audio_features,
            "semantic_result": semantic_result,
            "filler_counts": filler_counts,
            "speech_rate": speech_rate,
            "fluency_score": fluency_score,
            "scores": scores,
            "feedback": feedback,
            "extra_info": extra_info,
        }
        st.session_state.page = "dashboard"
        st.rerun()

    except Exception as e:
        error_box(f"An error occurred during analysis: {str(e)}")
