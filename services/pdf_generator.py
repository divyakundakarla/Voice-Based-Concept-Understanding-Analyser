"""
services/pdf_generator.py
Professional PDF report generation for VBCUA using ReportLab.
"""

import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image as RLImage, HRFlowable, PageBreak
)
from reportlab.pdfgen import canvas


PRIMARY = colors.HexColor("#6366f1")
SECONDARY = colors.HexColor("#8b5cf6")
DARK = colors.HexColor("#1a1a2e")
LIGHT_GRAY = colors.HexColor("#f5f5f7")
TEXT_GRAY = colors.HexColor("#444444")
GREEN = colors.HexColor("#10b981")
RED = colors.HexColor("#ef4444")
ORANGE = colors.HexColor("#f59e0b")


def _grade_color(grade: str):
    return {
        "A+": GREEN, "A": GREEN, "B": colors.HexColor("#3b82f6"),
        "C": ORANGE, "D": RED
    }.get(grade, TEXT_GRAY)


def generate_pdf_report(
    student_name: str,
    concept_name: str,
    transcript: str,
    similarity_pct: float,
    understanding_level: str,
    fluency_metrics: dict,
    scores: dict,
    feedback: dict,
    waveform_image=None,
    fluency_chart_image=None,
) -> bytes:
    """
    Generate a complete PDF report and return as bytes.

    Args:
        student_name: Name of the student
        concept_name: Selected concept
        transcript: Transcribed speech text
        similarity_pct: Semantic similarity percentage
        understanding_level: Excellent/Good/Average/Poor
        fluency_metrics: dict with filler_count, pause_ratio, speech_rate, confidence
        scores: dict with concept_score, fluency_score, communication_score, overall_score, grade
        feedback: dict with strengths, weaknesses, improvements, practice_recommendations, summary
        waveform_image: PIL Image of waveform (optional)
        fluency_chart_image: PIL Image of fluency charts (optional)

    Returns:
        PDF file as bytes
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        topMargin=15 * mm, bottomMargin=15 * mm,
        leftMargin=18 * mm, rightMargin=18 * mm,
    )

    styles = getSampleStyleSheet()
    story = []

    # ── Custom styles ──────────────────────────────────────────────
    title_style = ParagraphStyle(
        "TitleStyle", parent=styles["Title"],
        fontSize=22, textColor=PRIMARY, spaceAfter=4, alignment=TA_CENTER
    )
    subtitle_style = ParagraphStyle(
        "SubtitleStyle", parent=styles["Normal"],
        fontSize=10, textColor=TEXT_GRAY, alignment=TA_CENTER, spaceAfter=14
    )
    section_style = ParagraphStyle(
        "SectionStyle", parent=styles["Heading2"],
        fontSize=14, textColor=DARK, spaceBefore=14, spaceAfter=8,
        borderColor=PRIMARY, borderWidth=0,
    )
    body_style = ParagraphStyle(
        "BodyStyle", parent=styles["Normal"],
        fontSize=10, textColor=TEXT_GRAY, leading=15, alignment=TA_LEFT
    )
    label_style = ParagraphStyle(
        "LabelStyle", parent=styles["Normal"],
        fontSize=9, textColor=colors.white, alignment=TA_CENTER
    )

    # ── Header ──────────────────────────────────────────────────────
    story.append(Paragraph("Voice-Based Concept Understanding Report", title_style))
    story.append(Paragraph("AI-Powered Speech &amp; Semantic Evaluation (VBCUA)", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.2, color=PRIMARY, spaceAfter=14))

    # ── Student info table ─────────────────────────────────────────
    info_data = [
        ["Student Name", student_name],
        ["Concept Evaluated", concept_name],
        ["Date", datetime.now().strftime("%B %d, %Y — %I:%M %p")],
        ["Understanding Level", understanding_level],
    ]
    info_table = Table(info_data, colWidths=[55 * mm, 110 * mm])
    info_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), LIGHT_GRAY),
        ("TEXTCOLOR", (0, 0), (0, -1), DARK),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 14))

    # ── Overall Score Banner ───────────────────────────────────────
    grade = scores.get("grade", "-")
    overall = scores.get("overall_score", 0)
    grade_col = _grade_color(grade)

    score_table = Table(
        [[f"Overall Score: {overall:.1f} / 100", f"Grade: {grade}"]],
        colWidths=[110 * mm, 55 * mm]
    )
    score_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), PRIMARY),
        ("BACKGROUND", (1, 0), (1, 0), grade_col),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 13),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("VALIGN", (0, 0), (-1, 0), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, 0), 12),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
    ]))
    story.append(score_table)
    story.append(Spacer(1, 14))

    # ── Score Breakdown Table ──────────────────────────────────────
    story.append(Paragraph("Score Breakdown", section_style))
    breakdown_data = [
        ["Metric", "Score", "Weight"],
        ["Concept Understanding", f"{scores.get('concept_score', 0):.1f}/100", "50%"],
        ["Speech Fluency", f"{scores.get('fluency_score', 0):.1f}/100", "25%"],
        ["Communication Quality", f"{scores.get('communication_score', 0):.1f}/100", "25%"],
    ]
    breakdown_table = Table(breakdown_data, colWidths=[80 * mm, 50 * mm, 35 * mm])
    breakdown_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), DARK),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_GRAY]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    story.append(breakdown_table)
    story.append(Spacer(1, 14))

    # ── Semantic Similarity ────────────────────────────────────────
    story.append(Paragraph("Semantic Understanding Analysis", section_style))
    story.append(Paragraph(
        f"<b>Similarity Score:</b> {similarity_pct:.1f}% &nbsp;&nbsp;|&nbsp;&nbsp; "
        f"<b>Understanding Level:</b> {understanding_level}",
        body_style
    ))
    story.append(Spacer(1, 8))

    # ── Fluency Metrics ─────────────────────────────────────────────
    story.append(Paragraph("Speech Fluency Metrics", section_style))
    fm = fluency_metrics
    fluency_data = [
        ["Metric", "Value"],
        ["Filler Words Detected", str(fm.get("filler_count", 0))],
        ["Pause Ratio", f"{fm.get('pause_ratio', 0) * 100:.1f}%"],
        ["Speech Rate", f"{fm.get('speech_rate', 0):.0f} words/min"],
        ["Confidence Level", f"{fm.get('confidence', 0) * 100:.0f}%"],
    ]
    fluency_table = Table(fluency_data, colWidths=[80 * mm, 85 * mm])
    fluency_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_GRAY]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(fluency_table)
    story.append(Spacer(1, 14))

    # ── Waveform Image ──────────────────────────────────────────────
    if waveform_image is not None:
        story.append(Paragraph("Audio Waveform", section_style))
        img_buf = io.BytesIO()
        waveform_image.save(img_buf, format="PNG")
        img_buf.seek(0)
        story.append(RLImage(img_buf, width=160 * mm, height=48 * mm))
        story.append(Spacer(1, 10))

    # ── Fluency Charts ───────────────────────────────────────────────
    if fluency_chart_image is not None:
        story.append(Paragraph("Fluency Analysis Charts", section_style))
        img_buf2 = io.BytesIO()
        fluency_chart_image.save(img_buf2, format="PNG")
        img_buf2.seek(0)
        story.append(RLImage(img_buf2, width=165 * mm, height=43 * mm))
        story.append(Spacer(1, 10))

    story.append(PageBreak())

    # ── Transcript ───────────────────────────────────────────────────
    story.append(Paragraph("Speech Transcript", section_style))
    transcript_style = ParagraphStyle(
        "TranscriptStyle", parent=body_style,
        backColor=LIGHT_GRAY, borderPadding=10, leading=14
    )
    story.append(Paragraph(transcript or "(No transcript available)", transcript_style))
    story.append(Spacer(1, 14))

    # ── AI Feedback ──────────────────────────────────────────────────
    story.append(Paragraph("AI-Generated Feedback", section_style))
    story.append(Paragraph(f"<i>{feedback.get('summary', '')}</i>", body_style))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Strengths</b>", ParagraphStyle(
        "StrengthHeader", parent=body_style, textColor=GREEN, fontSize=11, spaceBefore=6, spaceAfter=4
    )))
    for s in feedback.get("strengths", []):
        story.append(Paragraph(f"✓ {s}", body_style))
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>Areas for Improvement</b>", ParagraphStyle(
        "WeaknessHeader", parent=body_style, textColor=RED, fontSize=11, spaceBefore=6, spaceAfter=4
    )))
    for w in feedback.get("weaknesses", []):
        story.append(Paragraph(f"⚠ {w}", body_style))
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>Suggested Improvements</b>", ParagraphStyle(
        "ImproveHeader", parent=body_style, textColor=PRIMARY, fontSize=11, spaceBefore=6, spaceAfter=4
    )))
    for imp in feedback.get("improvements", []):
        story.append(Paragraph(f"→ {imp}", body_style))
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>Practice Recommendations</b>", ParagraphStyle(
        "PracticeHeader", parent=body_style, textColor=SECONDARY, fontSize=11, spaceBefore=6, spaceAfter=4
    )))
    for p in feedback.get("practice_recommendations", []):
        story.append(Paragraph(p, body_style))

    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#dddddd")))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Generated by VBCUA — Voice-Based Concept Understanding Analyser | "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        ParagraphStyle("Footer", parent=styles["Normal"], fontSize=8,
                       textColor=colors.HexColor("#999999"), alignment=TA_CENTER)
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
