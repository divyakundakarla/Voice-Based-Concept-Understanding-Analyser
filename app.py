"""
app.py
Voice-Based Concept Understanding Analyser (VBCUA)
Main Streamlit application entry point.

Run with: streamlit run app.py
"""

import streamlit as st
from utils.helpers import inject_custom_css
from pages.home import render_home
from pages.analysis import render_analysis
from pages.dashboard import render_dashboard


def init_session_state():
    """Initialize all required session state variables."""
    defaults = {
        "page": "home",
        "student_name": "",
        "concept_name": None,
        "audio_path": None,
        "audio_filename": None,
        "analysis_results": None,
        "_waveform_img": None,
        "_fluency_img": None,
        "_pdf_bytes": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def main():
    st.set_page_config(
        page_title="VBCUA — Voice-Based Concept Understanding Analyser",
        page_icon="🎙️",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    init_session_state()
    inject_custom_css()

    # ── Sidebar Navigation ────────────────────────────────────────
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center; padding: 10px 0 20px 0;">
            <div style="font-size:2.5rem;">🎙️</div>
            <div style="font-weight:800; color:white; font-size:1.2rem;">VBCUA</div>
            <div style="color:rgba(255,255,255,0.5); font-size:0.75rem;">
                Voice-Based Concept<br/>Understanding Analyser
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        nav_options = {
            "home": "🏠 Home",
            "analysis": "🎙️ Analysis",
            "dashboard": "📊 Dashboard",
        }

        for key, label in nav_options.items():
            disabled = key == "dashboard" and st.session_state.get("analysis_results") is None
            if st.button(label, use_container_width=True,
                        disabled=disabled,
                        type="primary" if st.session_state.page == key else "secondary"):
                st.session_state.page = key
                st.rerun()

        st.markdown("---")
        st.caption("Built with Streamlit, Whisper & Sentence-BERT")
        st.caption("v1.0.0")

    # ── Page Routing ──────────────────────────────────────────────
    page = st.session_state.page

    if page == "home":
        render_home()
    elif page == "analysis":
        render_analysis()
    elif page == "dashboard":
        render_dashboard()
    else:
        render_home()


if __name__ == "__main__":
    main()
