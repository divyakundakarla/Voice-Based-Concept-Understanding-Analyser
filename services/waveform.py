"""
services/waveform.py
Waveform and audio chart generation for VBCUA.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import io
from PIL import Image


# ── Colour palette ──────────────────────────────────────────────────────────
BG       = "#0f0f1a"
WAVE_COL = "#6366f1"
ACCENT   = "#8b5cf6"
GRID_COL = "#1e1e3a"
TEXT_COL = "#a0aec0"


def _fig_to_pil(fig) -> Image.Image:
    """Convert a matplotlib Figure to a PIL Image."""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=120, bbox_inches="tight",
                facecolor=BG, edgecolor="none")
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf).copy()


# ── Public generators ────────────────────────────────────────────────────────

def generate_waveform_image(
    waveform: list,
    times: list,
    duration: float,
    title: str = "Audio Waveform"
) -> Image.Image:
    """Return a PIL image of the audio waveform."""
    y = np.array(waveform)
    t = np.array(times)

    fig, ax = plt.subplots(figsize=(10, 3))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    ax.fill_between(t, y, alpha=0.4, color=WAVE_COL)
    ax.plot(t, y, color=WAVE_COL, linewidth=0.6, alpha=0.9)
    ax.axhline(0, color=ACCENT, linewidth=0.5, alpha=0.4)

    ax.set_xlabel("Time (s)", color=TEXT_COL, fontsize=9)
    ax.set_ylabel("Amplitude", color=TEXT_COL, fontsize=9)
    ax.set_title(title, color="white", fontsize=11, fontweight="bold", pad=10)
    ax.tick_params(colors=TEXT_COL, labelsize=8)
    for spine in ax.spines.values():
        spine.set_edgecolor(GRID_COL)
    ax.grid(color=GRID_COL, linewidth=0.4, alpha=0.6)
    ax.set_xlim(0, max(t) if len(t) else 1)

    plt.tight_layout()
    return _fig_to_pil(fig)


def generate_fluency_chart(
    filler_words: dict,
    pause_ratio: float,
    speech_rate: float,
    confidence: float,
) -> Image.Image:
    """Return a PIL image with a 2×2 fluency metrics chart."""
    fig, axes = plt.subplots(1, 4, figsize=(14, 3.5))
    fig.patch.set_facecolor(BG)

    # 1. Filler word bar chart
    ax = axes[0]
    ax.set_facecolor(BG)
    fillers = {k: v for k, v in filler_words.items() if k != "_total" and v > 0}
    if fillers:
        bars = ax.bar(list(fillers.keys()), list(fillers.values()),
                      color=WAVE_COL, edgecolor=ACCENT, linewidth=0.8)
        for bar, val in zip(bars, fillers.values()):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
                    str(val), ha="center", va="bottom", color="white", fontsize=8)
    else:
        ax.text(0.5, 0.5, "No filler\nwords! ✓",
                ha="center", va="center", transform=ax.transAxes,
                color="#10b981", fontsize=12, fontweight="bold")
    ax.set_title("Filler Words", color="white", fontsize=9, pad=6)
    ax.tick_params(colors=TEXT_COL, labelsize=7)
    for spine in ax.spines.values():
        spine.set_edgecolor(GRID_COL)
    ax.set_facecolor(BG)

    # 2. Pause ratio donut
    ax = axes[1]
    ax.set_facecolor(BG)
    speech_frac = max(0, 1 - pause_ratio)
    wedge_colors = [WAVE_COL, "#1e1e3a"]
    ax.pie([speech_frac, pause_ratio], colors=wedge_colors,
           startangle=90, wedgeprops=dict(width=0.45, edgecolor=BG))
    ax.text(0, 0, f"{speech_frac * 100:.0f}%\nSpeech",
            ha="center", va="center", color="white", fontsize=9, fontweight="bold")
    ax.set_title("Speech vs Pause", color="white", fontsize=9, pad=6)

    # 3. Speech rate gauge (horizontal bar)
    ax = axes[2]
    ax.set_facecolor(BG)
    rate_capped = min(speech_rate, 250)
    colors_bar = ["#ef4444", "#f59e0b", "#10b981", "#f59e0b", "#ef4444"]
    ranges = [0, 80, 120, 160, 200, 250]
    for i in range(len(ranges) - 1):
        ax.barh(0, ranges[i + 1] - ranges[i], left=ranges[i],
                color=colors_bar[i], alpha=0.3, height=0.5)
    ax.axvline(rate_capped, color="white", linewidth=2)
    ax.text(rate_capped, 0.35, f"{speech_rate:.0f}\nwpm",
            ha="center", color="white", fontsize=8, fontweight="bold")
    ax.set_xlim(0, 250)
    ax.set_ylim(-0.5, 0.8)
    ax.axis("off")
    ax.set_title("Speech Rate (wpm)", color="white", fontsize=9, pad=6)

    # 4. Confidence arc (simple bar)
    ax = axes[3]
    ax.set_facecolor(BG)
    conf_pct = confidence * 100
    bar_color = "#10b981" if conf_pct >= 70 else ("#f59e0b" if conf_pct >= 45 else "#ef4444")
    ax.barh(0, conf_pct, color=bar_color, alpha=0.85, height=0.5, edgecolor=ACCENT)
    ax.barh(0, 100, color="#1e1e3a", height=0.5)
    ax.barh(0, conf_pct, color=bar_color, alpha=0.85, height=0.5, edgecolor=ACCENT)
    ax.text(50, 0, f"{conf_pct:.0f}%",
            ha="center", va="center", color="white", fontsize=11, fontweight="bold")
    ax.set_xlim(0, 100)
    ax.set_ylim(-0.6, 0.6)
    ax.axis("off")
    ax.set_title("Confidence", color="white", fontsize=9, pad=6)

    plt.tight_layout(pad=1.5)
    return _fig_to_pil(fig)


def generate_score_radar(scores: dict) -> Image.Image:
    """
    Generate a radar / spider chart for multi-dimensional scores.
    scores: {'Concept': x, 'Fluency': y, 'Communication': z}
    """
    import matplotlib.patches as mpatches

    labels = list(scores.keys())
    values = [scores[k] for k in labels]
    N = len(labels)

    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    values_plot = values + values[:1]
    angles_plot = angles + angles[:1]

    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    ax.plot(angles_plot, values_plot, color=WAVE_COL, linewidth=2)
    ax.fill(angles_plot, values_plot, color=WAVE_COL, alpha=0.25)

    ax.set_xticks(angles)
    ax.set_xticklabels(labels, color="white", size=10)
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(["20", "40", "60", "80", "100"],
                       color=TEXT_COL, size=7)
    ax.set_ylim(0, 100)
    ax.grid(color=GRID_COL, linewidth=0.6)
    ax.spines["polar"].set_color(GRID_COL)
    ax.set_title("Score Breakdown", color="white", size=12,
                 fontweight="bold", pad=15)

    plt.tight_layout()
    return _fig_to_pil(fig)
