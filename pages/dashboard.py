"""
pages/dashboard.py
Results dashboard for VBCUA — shows all scores, charts, and AI feedback.
"""

import streamlit as st
from components.ui_components import (
    metric_card, gradient_card, section_header, step_header,
    pill, pill_group, circular_score, understanding_badge
)
from utils.helpers import get_understanding_level, format_duration
from services.waveform import generate_waveform_image, generate_fluency_chart, generate_score_radar
from services.pdf_generator import generate_pdf_report


def render_dashboard():
    results = st.session_state.get("analysis_results")
    if not results:
        st.warning("No analysis results found. Please run an analysis first.")
        if st.button("← Go to Analysis"):
            st.session_state.page = "analysis"
            st.rerun()
        return

    transcription = results["transcription"]
    audio_features = results["audio_features"]
    semantic_result = results["semantic_result"]
    scores = results["scores"]
    feedback = results["feedback"]
    filler_counts = results["filler_counts"]

    # ── Header ────────────────────────────────────────────────────
    col1, col2 = st.columns([3, 1])
    with col1:
        section_header(
            "📊 Analysis Dashboard",
            f"Results for {results['student_name']} — Concept: {results['concept_name']}",
            ""
        )
    with col2:
        if st.button("🔄 New Analysis", use_container_width=True):
            st.session_state.page = "analysis"
            st.session_state.analysis_results = None
            st.rerun()

    # ── Top Score Row ─────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        circular_score(scores["overall_score"], "Overall Score")
    with c2:
        circular_score(scores["concept_score"], "Concept Understanding")
    with c3:
        circular_score(scores["fluency_score"], "Speech Fluency")
    with c4:
        circular_score(scores["communication_score"], "Communication")

    st.markdown(f"""
    <div style="text-align:center; margin: 10px 0 30px 0;">
        <span style="
            font-size:1.1rem; font-weight:700; color:white;
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            padding: 6px 24px; border-radius: 20px;
        ">Grade: {scores['grade']}</span>
    </div>
    """, unsafe_allow_html=True)

    # ── Quick Stats Row ───────────────────────────────────────────
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        metric_card("Duration", format_duration(audio_features["duration"]), "Audio length", "⏱️")
    with s2:
        metric_card("Word Count", str(transcription["word_count"]), "Words spoken", "📝")
    with s3:
        metric_card("Speech Rate", f"{results['speech_rate']:.0f}", "words/min", "🗣️")
    with s4:
        metric_card("Filler Words", str(filler_counts["_total"]), "Detected", "🔤")

    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

    # ── Tabs ──────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📝 Transcript", "🧠 Concept Understanding", "📈 Fluency Analysis",
        "💡 AI Feedback", "📄 Download Report"
    ])

    # ── Tab 1: Transcript ─────────────────────────────────────────
    with tab1:
        step_header(1, "Speech Transcription", "Converted using OpenAI Whisper")
        st.text_area("Transcribed Text", transcription["text"], height=180, disabled=True)

        if transcription.get("error") and "Demo mode" in str(transcription.get("error", "")):
            st.caption("⚠️ Running in demo mode — install openai-whisper for real transcription.")

        st.markdown("##### Audio Waveform")
        try:
            wf_img = generate_waveform_image(
                audio_features["waveform"], audio_features["waveform_times"],
                audio_features["duration"]
            )
            st.image(wf_img, use_container_width=True)
            st.session_state["_waveform_img"] = wf_img
        except Exception as e:
            st.caption(f"Waveform unavailable: {e}")

    # ── Tab 2: Concept Understanding ─────────────────────────────
    with tab2:
        step_header(2, "Semantic Understanding", f"Compared against reference for '{results['concept_name']}'")

        level, color = get_understanding_level(semantic_result["similarity_score"])

        col1, col2 = st.columns([1, 2])
        with col1:
            circular_score(semantic_result["similarity_pct"], "Similarity Score")
            understanding_badge(level)
        with col2:
            st.markdown("**Reference Explanation**")
            st.info(semantic_result["reference_text"][:400] + "...")

        st.progress(semantic_result["similarity_score"], text=f"Semantic Match: {semantic_result['similarity_pct']:.1f}%")

        colA, colB = st.columns(2)
        with colA:
            st.markdown("**✅ Concepts Covered**")
            if semantic_result["covered_concepts"]:
                st.markdown(pill_group(semantic_result["covered_concepts"], "green"), unsafe_allow_html=True)
            else:
                st.caption("No key concepts detected.")
        with colB:
            st.markdown("**❌ Missing Concepts**")
            if semantic_result["missing_concepts"]:
                st.markdown(pill_group(semantic_result["missing_concepts"], "red"), unsafe_allow_html=True)
            else:
                st.caption("All key concepts covered! 🎉")

        if results.get("extra_info"):
            st.markdown("**ℹ️ Additional Information Mentioned**")
            for info in results["extra_info"]:
                st.markdown(f"- {info}")

    # ── Tab 3: Fluency Analysis ───────────────────────────────────
    with tab3:
        step_header(3, "Speech Fluency Analysis", "Filler words, pauses, pace, and confidence")

        f1, f2, f3, f4 = st.columns(4)
        with f1:
            metric_card("Pause Ratio", f"{audio_features['pause_ratio']*100:.0f}%", "of total audio", "⏸️")
        with f2:
            metric_card("RMS Energy", f"{audio_features['rms_db']:.1f} dB", "Voice volume", "🔊")
        with f3:
            metric_card("Confidence", f"{audio_features['confidence']*100:.0f}%", "Vocal confidence", "💪")
        with f4:
            metric_card("Fluency Score", f"{results['fluency_score']:.0f}/100", "Overall fluency", "🎯")

        st.markdown("##### Filler Word Breakdown")
        fillers_display = {k: v for k, v in filler_counts.items() if k != "_total" and v > 0}
        if fillers_display:
            st.bar_chart(fillers_display)
        else:
            st.success("No filler words detected — excellent clarity!")

        st.markdown("##### Fluency Metrics Charts")
        try:
            fl_img = generate_fluency_chart(
                filler_counts, audio_features["pause_ratio"],
                results["speech_rate"], audio_features["confidence"]
            )
            st.image(fl_img, use_container_width=True)
            st.session_state["_fluency_img"] = fl_img
        except Exception as e:
            st.caption(f"Chart unavailable: {e}")

        st.markdown("##### Score Breakdown Radar")
        try:
            radar_img = generate_score_radar({
                "Concept": scores["concept_score"],
                "Fluency": scores["fluency_score"],
                "Communication": scores["communication_score"],
            })
            st.image(radar_img, width=400)
        except Exception as e:
            st.caption(f"Radar unavailable: {e}")

    # ── Tab 4: AI Feedback ────────────────────────────────────────
    with tab4:
        step_header(4, "AI-Generated Feedback", "Personalized strengths, weaknesses, and recommendations")

        st.info(feedback["summary"])

        col1, col2 = st.columns(2)
        with col1:
            gradient_card("Strengths", "<br/>".join(f"✓ {s}" for s in feedback["strengths"]), "green", "💪")
        with col2:
            gradient_card("Areas for Improvement", "<br/>".join(f"⚠ {w}" for w in feedback["weaknesses"]), "orange", "🎯")

        gradient_card("Suggested Improvements", "<br/>".join(f"→ {i}" for i in feedback["improvements"]), "blue", "💡")
        gradient_card("Practice Recommendations", "<br/>".join(feedback["practice_recommendations"]), "purple", "📚")

    # ── Tab 5: Download Report ────────────────────────────────────
    with tab5:
        step_header(5, "Download PDF Report", "Generate a professional report of your analysis")

        st.markdown("""
        Your report will include: student details, transcript, semantic similarity,
        fluency metrics, waveform, score breakdown, and full AI feedback.
        """)

        if st.button("📄 Generate PDF Report", type="primary", use_container_width=True):
            with st.spinner("Generating your report..."):
                pdf_bytes = generate_pdf_report(
                    student_name=results["student_name"],
                    concept_name=results["concept_name"],
                    transcript=transcription["text"],
                    similarity_pct=semantic_result["similarity_pct"],
                    understanding_level=get_understanding_level(semantic_result["similarity_score"])[0],
                    fluency_metrics={
                        "filler_count": filler_counts["_total"],
                        "pause_ratio": audio_features["pause_ratio"],
                        "speech_rate": results["speech_rate"],
                        "confidence": audio_features["confidence"],
                    },
                    scores=scores,
                    feedback=feedback,
                    waveform_image=st.session_state.get("_waveform_img"),
                    fluency_chart_image=st.session_state.get("_fluency_img"),
                )
                st.session_state["_pdf_bytes"] = pdf_bytes
                st.success("✅ Report generated successfully!")

        if st.session_state.get("_pdf_bytes"):
            st.download_button(
                "⬇️ Download Report (PDF)",
                data=st.session_state["_pdf_bytes"],
                file_name=f"VBCUA_Report_{results['student_name'].replace(' ', '_')}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
