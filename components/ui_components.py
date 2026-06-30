"""
components/ui_components.py
Reusable Streamlit UI components for VBCUA.
"""

import streamlit as st
from utils.helpers import score_color


def metric_card(label: str, value: str, sub: str = "", icon: str = ""):
    """Render a single metric card."""
    st.markdown(f"""
    <div class="metric-card">
        <div class="label">{icon} {label}</div>
        <div class="value">{value}</div>
        <div class="sub">{sub}</div>
    </div>
    """, unsafe_allow_html=True)


def gradient_card(title: str, content_html: str, variant: str = "purple", icon: str = ""):
    """Render a gradient-bordered content card."""
    st.markdown(f"""
    <div class="gradient-card gradient-card-{variant}">
        <div class="section-header">{icon} {title}</div>
        {content_html}
    </div>
    """, unsafe_allow_html=True)


def section_header(title: str, subtitle: str = "", icon: str = ""):
    """Render a styled section header with optional subtitle."""
    st.markdown(f"""
    <div class="section-header">{icon} {title}</div>
    {f'<div class="section-subtitle">{subtitle}</div>' if subtitle else ''}
    """, unsafe_allow_html=True)


def step_header(step_number: int, title: str, subtitle: str = ""):
    """Render a numbered step header (Step 1, Step 2, etc.)."""
    st.markdown(f"""
    <div style="display:flex; align-items:center; margin: 20px 0 10px 0;">
        <span class="step-badge">{step_number}</span>
        <div>
            <div style="font-size:1.3rem; font-weight:700; color:white;">{title}</div>
            {f'<div style="color:rgba(255,255,255,0.5); font-size:0.85rem;">{subtitle}</div>' if subtitle else ''}
        </div>
    </div>
    """, unsafe_allow_html=True)


def pill(text: str, variant: str = "blue"):
    """Render an inline pill badge. variant: green/red/blue/orange"""
    return f'<span class="pill pill-{variant}">{text}</span>'

def pill_group(items: list, variant: str = "blue") -> str:
    """Render a group of pills as HTML string."""
    return " ".join(pill(item, variant) for item in items)


def circular_score(score: float, label: str = "Overall Score", size_px: int = 130):
    """Render a circular score indicator using conic-gradient CSS."""
    color = score_color(score)
    pct = max(0, min(100, score))
    st.markdown(f"""
    <div class="circular-score">
        <div class="score-ring" style="
            background: conic-gradient({color} {pct * 3.6}deg, rgba(255,255,255,0.08) 0deg);
            width:{size_px}px; height:{size_px}px;
        ">
            <div style="
                background:#16213e; width:{size_px - 18}px; height:{size_px - 18}px;
                border-radius:50%; display:flex; align-items:center; justify-content:center;
                flex-direction:column;
            ">
                <span style="font-size:1.6rem; font-weight:800; color:{color};">{pct:.0f}</span>
                <span style="font-size:0.65rem; color:rgba(255,255,255,0.4);">/100</span>
            </div>
        </div>
        <div style="color:white; font-weight:600; font-size:0.9rem; text-align:center;">{label}</div>
    </div>
    """, unsafe_allow_html=True)


def understanding_badge(level: str):
    """Render the Excellent/Good/Average/Poor badge."""
    variant_map = {
        "Excellent": "green",
        "Good": "blue",
        "Average": "orange",
        "Poor": "red",
    }
    variant = variant_map.get(level, "blue")
    st.markdown(f"""
    <div style="text-align:center; margin: 12px 0;">
        {pill(f"Understanding Level: {level}", variant)}
    </div>
    """, unsafe_allow_html=True)


def feature_card(icon: str, title: str, desc: str):
    """Landing page feature card."""
    st.markdown(f"""
    <div class="gradient-card gradient-card-purple" style="text-align:center; min-height:180px;">
        <div style="font-size:2.2rem; margin-bottom:10px;">{icon}</div>
        <div style="font-weight:700; color:white; font-size:1.05rem; margin-bottom:8px;">{title}</div>
        <div style="color:rgba(255,255,255,0.6); font-size:0.85rem; line-height:1.5;">{desc}</div>
    </div>
    """, unsafe_allow_html=True)


def how_it_works_step(number: int, title: str, desc: str):
    """Landing page 'how it works' step card."""
    st.markdown(f"""
    <div style="text-align:center; padding: 16px;">
        <div style="
            width:50px; height:50px; border-radius:50%;
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            display:flex; align-items:center; justify-content:center;
            margin: 0 auto 12px auto; font-weight:800; color:white; font-size:1.3rem;
        ">{number}</div>
        <div style="font-weight:700; color:white; margin-bottom:6px;">{title}</div>
        <div style="color:rgba(255,255,255,0.55); font-size:0.82rem;">{desc}</div>
    </div>
    """, unsafe_allow_html=True)


def loading_animation(message: str = "Analyzing..."):
    """Display a loading spinner context manager wrapper."""
    return st.spinner(f"🔄 {message}")


def error_box(message: str):
    """Render an error message box."""
    st.markdown(f"""
    <div style="
        background: rgba(239,68,68,0.15); border: 1px solid rgba(239,68,68,0.4);
        border-radius: 10px; padding: 14px 18px; color:#ef4444; margin: 10px 0;
    ">⚠️ {message}</div>
    """, unsafe_allow_html=True)


def success_box(message: str):
    """Render a success message box."""
    st.markdown(f"""
    <div style="
        background: rgba(16,185,129,0.15); border: 1px solid rgba(16,185,129,0.4);
        border-radius: 10px; padding: 14px 18px; color:#10b981; margin: 10px 0;
    ">✅ {message}</div>
    """, unsafe_allow_html=True)
