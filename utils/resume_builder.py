"""
resume_builder.py
Generates ATS-friendly PDF resumes from structured form data.
Uses reportlab for clean, professional formatting.
"""

import io
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER

# ── Color Palette ─────────────────────────────────────────────────────────────
PRIMARY   = colors.HexColor("#1a1a2e")
ACCENT    = colors.HexColor("#4f46e5")
LIGHT_BG  = colors.HexColor("#f8f7ff")
GRAY      = colors.HexColor("#6b7280")
DARK_GRAY = colors.HexColor("#374151")


# ── Style Definitions ─────────────────────────────────────────────────────────

def _build_styles():
    base = getSampleStyleSheet()
    return {
        "name": ParagraphStyle(
            "name", fontSize=18, fontName="Helvetica-Bold",
            textColor=PRIMARY, spaceAfter=3, alignment=TA_CENTER,
        ),
        "contact": ParagraphStyle(
            "contact", fontSize=8.5, fontName="Helvetica",
            textColor=GRAY, spaceAfter=6, alignment=TA_CENTER, leading=13,
        ),
        "section_header": ParagraphStyle(
            "section_header", fontSize=11, fontName="Helvetica-Bold",
            textColor=ACCENT, spaceBefore=10, spaceAfter=3,
        ),
        "body": ParagraphStyle(
            "body", fontSize=9.5, fontName="Helvetica",
            textColor=DARK_GRAY, spaceAfter=3, leading=14,
        ),
        "bullet": ParagraphStyle(
            "bullet", fontSize=9.5, fontName="Helvetica",
            textColor=DARK_GRAY, spaceAfter=2, leading=13,
            leftIndent=12, bulletIndent=0,
        ),
        "job_title": ParagraphStyle(
            "job_title", fontSize=10, fontName="Helvetica-Bold",
            textColor=PRIMARY, spaceAfter=1,
        ),
        "sub_info": ParagraphStyle(
            "sub_info", fontSize=9, fontName="Helvetica-Oblique",
            textColor=GRAY, spaceAfter=3,
        ),
        "skill_tag": ParagraphStyle(
            "skill_tag", fontSize=9, fontName="Helvetica",
            textColor=DARK_GRAY, spaceAfter=2,
        ),
        "summary": ParagraphStyle(
            "summary", fontSize=9.5, fontName="Helvetica",
            textColor=DARK_GRAY, spaceAfter=4, leading=14,
            leftIndent=4,
        ),
    }


def _section_divider(styles) -> list:
    """Returns a section header divider line."""
    return [HRFlowable(width="100%", thickness=0.5, color=ACCENT, spaceAfter=4)]


# ── Section Builders ──────────────────────────────────────────────────────────

def _build_header(data: dict, styles: dict) -> list:
    elements = []
    name = data.get("name", "Your Name").strip()
    elements.append(Paragraph(name, styles["name"]))

    contact_parts = []
    for field in ["email", "phone", "location"]:
        val = data.get(field, "").strip()
        if val:
            contact_parts.append(val)
    if contact_parts:
        elements.append(Paragraph("  |  ".join(contact_parts), styles["contact"]))

    link_parts = []
    for field in ["linkedin", "github"]:
        val = data.get(field, "").strip()
        if val:
            link_parts.append(val)
    if link_parts:
        elements.append(Paragraph("  |  ".join(link_parts), styles["contact"]))

    elements.append(HRFlowable(width="100%", thickness=1.5, color=ACCENT, spaceAfter=6))
    return elements


def _build_summary(summary: str, styles: dict) -> list:
    if not summary.strip():
        return []
    elements = [Paragraph("PROFESSIONAL SUMMARY", styles["section_header"])]
    elements += _section_divider(styles)
    elements.append(Paragraph(summary.strip(), styles["summary"]))
    return elements


def _build_skills(skills_data: dict, styles: dict) -> list:
    """
    skills_data: { "Languages": ["Python", "Java"], "Frontend": ["React"] }
    or flat list of strings
    """
    if not skills_data:
        return []

    elements = [Paragraph("TECHNICAL SKILLS", styles["section_header"])]
    elements += _section_divider(styles)

    if isinstance(skills_data, dict):
        rows = []
        for category, skill_list in skills_data.items():
            if skill_list:
                cat_text  = Paragraph(f"<b>{category}:</b>", styles["skill_tag"])
                skill_text = Paragraph(", ".join(skill_list), styles["skill_tag"])
                rows.append([cat_text, skill_text])
        if rows:
            table = Table(rows, colWidths=[3.5 * cm, 14 * cm])
            table.setStyle(TableStyle([
                ("VALIGN",    (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING",  (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ]))
            elements.append(table)
    else:
        # Flat list
        elements.append(Paragraph(", ".join(skills_data), styles["body"]))

    return elements


def _build_experience(experience: list, styles: dict) -> list:
    if not experience:
        return []

    elements = [Paragraph("WORK EXPERIENCE", styles["section_header"])]
    elements += _section_divider(styles)

    for job in experience:
        title   = job.get("title", "").strip()
        company = job.get("company", "").strip()
        duration = job.get("duration", "").strip()
        responsibilities = job.get("responsibilities", [])

        # Title row with duration on right
        if title:
            title_table = Table(
                [[Paragraph(title, styles["job_title"]),
                  Paragraph(duration, styles["sub_info"])]],
                colWidths=[12 * cm, 5.5 * cm]
            )
            title_table.setStyle(TableStyle([
                ("ALIGN",  (1, 0), (1, 0), "RIGHT"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING",    (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]))
            elements.append(title_table)

        if company:
            elements.append(Paragraph(company, styles["sub_info"]))

        for resp in responsibilities:
            if resp.strip():
                elements.append(Paragraph(f"• {resp.strip()}", styles["bullet"]))

        elements.append(Spacer(1, 4))

    return elements


def _build_education(education: list, styles: dict) -> list:
    if not education:
        return []

    elements = [Paragraph("EDUCATION", styles["section_header"])]
    elements += _section_divider(styles)

    for edu in education:
        degree      = edu.get("degree", "").strip()
        institution = edu.get("institution", "").strip()
        year        = edu.get("year", "").strip()
        gpa         = edu.get("gpa", "").strip()

        if degree:
            row = Table(
                [[Paragraph(degree, styles["job_title"]),
                  Paragraph(year, styles["sub_info"])]],
                colWidths=[12 * cm, 5.5 * cm]
            )
            row.setStyle(TableStyle([
                ("ALIGN",  (1, 0), (1, 0), "RIGHT"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING",    (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]))
            elements.append(row)

        sub = institution
        if gpa:
            sub += f"  |  GPA: {gpa}"
        if sub:
            elements.append(Paragraph(sub, styles["sub_info"]))
        elements.append(Spacer(1, 3))

    return elements


def _build_projects(projects: list, styles: dict) -> list:
    if not projects:
        return []

    elements = [Paragraph("PROJECTS", styles["section_header"])]
    elements += _section_divider(styles)

    for proj in projects:
        title       = proj.get("title", "").strip()
        description = proj.get("description", "").strip()
        tech        = proj.get("tech", [])
        link        = proj.get("link", "").strip()

        if title:
            title_str = title
            if link:
                title_str += f" | {link}"
            elements.append(Paragraph(title_str, styles["job_title"]))

        if tech:
            tech_str = ", ".join(tech) if isinstance(tech, list) else tech
            elements.append(Paragraph(f"<i>Tech: {tech_str}</i>", styles["sub_info"]))

        if description:
            for line in description.split("\n"):
                if line.strip():
                    elements.append(Paragraph(f"• {line.strip()}", styles["bullet"]))

        elements.append(Spacer(1, 4))

    return elements


def _build_certifications(certs: list, styles: dict) -> list:
    if not certs:
        return []

    elements = [Paragraph("CERTIFICATIONS", styles["section_header"])]
    elements += _section_divider(styles)

    for cert in certs:
        if isinstance(cert, dict):
            name   = cert.get("name", "").strip()
            issuer = cert.get("issuer", "").strip()
            year   = cert.get("year", "").strip()
            line   = name
            if issuer:
                line += f" — {issuer}"
            if year:
                line += f" ({year})"
            elements.append(Paragraph(f"• {line}", styles["bullet"]))
        else:
            elements.append(Paragraph(f"• {str(cert).strip()}", styles["bullet"]))

    return elements


# ── Master Builder ────────────────────────────────────────────────────────────

def build_resume_pdf(resume_data: dict) -> bytes:
    """
    Build a complete ATS-friendly PDF resume.

    resume_data structure:
    {
        "name": str,
        "email": str,
        "phone": str,
        "linkedin": str,       # optional
        "github": str,         # optional
        "location": str,       # optional
        "summary": str,        # optional
        "skills": dict | list, # { "Languages": [...] } or flat list
        "experience": [
            {
                "title": str,
                "company": str,
                "duration": str,
                "responsibilities": [str, ...]
            }
        ],
        "education": [
            {
                "degree": str,
                "institution": str,
                "year": str,
                "gpa": str      # optional
            }
        ],
        "projects": [
            {
                "title": str,
                "description": str,
                "tech": [str, ...],
                "link": str     # optional
            }
        ],
        "certifications": [str | dict, ...]  # optional
    }

    Returns: bytes (PDF content)
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=1.8 * cm,
        rightMargin=1.8 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm,
    )

    styles   = _build_styles()
    elements = []

    # Build sections in order
    elements += _build_header(resume_data, styles)
    elements += _build_summary(resume_data.get("summary", ""), styles)
    elements += _build_skills(resume_data.get("skills", {}), styles)
    elements += _build_experience(resume_data.get("experience", []), styles)
    elements += _build_education(resume_data.get("education", []), styles)
    elements += _build_projects(resume_data.get("projects", []), styles)
    elements += _build_certifications(resume_data.get("certifications", []), styles)

    doc.build(elements)
    return buffer.getvalue()


def validate_resume_data(data: dict) -> list[str]:
    """
    Validate resume form data before building.
    Returns list of error messages (empty = valid).
    """
    errors = []
    if not data.get("name", "").strip():
        errors.append("Name is required.")
    if not data.get("email", "").strip():
        errors.append("Email is required.")
    if not data.get("skills"):
        errors.append("At least one skill is required.")
    if not data.get("education"):
        errors.append("At least one education entry is required.")
    return errors
