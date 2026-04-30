"""
resume_builder.py  —  4 visually distinct templates
"""
import io
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle, KeepTogether
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

W = 17.6 * cm

TEMPLATES = {
    # ── CLASSIC: Black & white, serif-feel, centered name, thick dividers ──
    "Classic": {
        "accent":     colors.HexColor("#000000"),
        "primary":    colors.HexColor("#000000"),
        "gray":       colors.HexColor("#555555"),
        "dark":       colors.HexColor("#222222"),
        "hr_color":   colors.HexColor("#000000"),
        "hr_thick":   1.2,
        "name_size":  22,
        "name_align": TA_CENTER,
        "header_bg":  None,
        "sec_bg":     None,
        "sec_color":  colors.HexColor("#000000"),
        "sec_size":   11,
        "sec_upper":  True,
        "body_size":  10,
        "sub_size":   9.5,
        "margins":    (1.8*cm, 1.8*cm, 2.0*cm, 2.0*cm),
    },
    # ── MODERN: Purple header band, left-aligned, colored section titles ──
    "Modern": {
        "accent":     colors.HexColor("#4f46e5"),
        "primary":    colors.HexColor("#1e1b4b"),
        "gray":       colors.HexColor("#6b7280"),
        "dark":       colors.HexColor("#1f2937"),
        "hr_color":   colors.HexColor("#4f46e5"),
        "hr_thick":   2.0,
        "name_size":  24,
        "name_align": TA_LEFT,
        "header_bg":  colors.HexColor("#4f46e5"),
        "sec_bg":     None,
        "sec_color":  colors.HexColor("#4f46e5"),
        "sec_size":   11,
        "sec_upper":  True,
        "body_size":  10,
        "sub_size":   9.5,
        "margins":    (1.8*cm, 1.8*cm, 1.5*cm, 1.5*cm),
    },
    # ── MINIMAL: Green accents, lots of whitespace, clean lines ──
    "Minimal": {
        "accent":     colors.HexColor("#059669"),
        "primary":    colors.HexColor("#111827"),
        "gray":       colors.HexColor("#6b7280"),
        "dark":       colors.HexColor("#374151"),
        "hr_color":   colors.HexColor("#059669"),
        "hr_thick":   0.8,
        "name_size":  26,
        "name_align": TA_LEFT,
        "header_bg":  None,
        "sec_bg":     None,
        "sec_color":  colors.HexColor("#059669"),
        "sec_size":   10,
        "sec_upper":  False,
        "body_size":  10,
        "sub_size":   9.5,
        "margins":    (2.2*cm, 2.2*cm, 2.0*cm, 2.0*cm),
    },
    # ── CREATIVE: Purple sidebar-style header, bold section labels ──
    "Creative": {
        "accent":     colors.HexColor("#7c3aed"),
        "primary":    colors.HexColor("#1a1a2e"),
        "gray":       colors.HexColor("#6b7280"),
        "dark":       colors.HexColor("#374151"),
        "hr_color":   colors.HexColor("#7c3aed"),
        "hr_thick":   3.0,
        "name_size":  24,
        "name_align": TA_CENTER,
        "header_bg":  colors.HexColor("#7c3aed"),
        "sec_bg":     colors.HexColor("#f5f3ff"),
        "sec_color":  colors.HexColor("#7c3aed"),
        "sec_size":   11,
        "sec_upper":  True,
        "body_size":  10,
        "sub_size":   9.5,
        "margins":    (1.8*cm, 1.8*cm, 1.5*cm, 1.5*cm),
    },
}


def _styles(t: dict) -> dict:
    name_color = colors.white if t["header_bg"] else t["primary"]
    contact_color = colors.white if t["header_bg"] else t["gray"]
    return {
        "name": ParagraphStyle("name",
            fontSize=t["name_size"], fontName="Helvetica-Bold",
            textColor=name_color, spaceAfter=6,
            alignment=t["name_align"]),
        "contact": ParagraphStyle("contact",
            fontSize=9, fontName="Helvetica",
            textColor=contact_color,
            spaceAfter=5, alignment=t["name_align"], leading=16),
        "sec_hdr": ParagraphStyle("sec_hdr",
            fontSize=t["sec_size"], fontName="Helvetica-Bold",
            textColor=t["sec_color"],
            spaceBefore=0, spaceAfter=4),
        "body": ParagraphStyle("body",
            fontSize=t["body_size"], fontName="Helvetica",
            textColor=t["dark"], spaceAfter=4, leading=15),
        "bullet": ParagraphStyle("bullet",
            fontSize=t["body_size"], fontName="Helvetica",
            textColor=t["dark"], spaceAfter=3, leading=14, leftIndent=12),
        "job_title": ParagraphStyle("job_title",
            fontSize=t["body_size"]+0.5, fontName="Helvetica-Bold",
            textColor=t["primary"], spaceAfter=2),
        "sub": ParagraphStyle("sub",
            fontSize=t["sub_size"], fontName="Helvetica-Oblique",
            textColor=t["gray"], spaceAfter=4),
        "skill_cat": ParagraphStyle("skill_cat",
            fontSize=t["sub_size"], fontName="Helvetica-Bold",
            textColor=t["accent"], spaceAfter=2),
        "skill_val": ParagraphStyle("skill_val",
            fontSize=t["sub_size"], fontName="Helvetica",
            textColor=t["dark"], spaceAfter=2),
    }


def _divider(t, space_before=2, space_after=6):
    return [
        Spacer(1, space_before),
        HRFlowable(width="100%", thickness=t["hr_thick"],
                   color=t["hr_color"], spaceAfter=space_after),
    ]


def _sec_header(title, s, t, extra_top=0):
    label = title.upper() if t["sec_upper"] else title
    hdr = Paragraph(label, s["sec_hdr"])
    top_space = 14 + extra_top
    if t["sec_bg"]:
        tbl = Table([[hdr]], colWidths=[W])
        tbl.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (-1,-1), t["sec_bg"]),
            ("TOPPADDING",    (0,0), (-1,-1), 4),
            ("BOTTOMPADDING", (0,0), (-1,-1), 4),
            ("LEFTPADDING",   (0,0), (-1,-1), 6),
            ("RIGHTPADDING",  (0,0), (-1,-1), 6),
        ]))
        return [Spacer(1, top_space), tbl, Spacer(1, 6)]
    return [Spacer(1, top_space), hdr] + _divider(t, space_before=2, space_after=6)


def _header(data, s, t):
    name = data.get("name", "").strip()
    contacts = [v for k in ["email","phone","location"] if (v := data.get(k,"").strip())]
    links    = [v for k in ["linkedin","github"]        if (v := data.get(k,"").strip())]

    if t["header_bg"]:
        rows = [[Paragraph(name, s["name"])]]
        if contacts:
            rows.append([Paragraph("  |  ".join(contacts), s["contact"])])
        if links:
            rows.append([Paragraph("  |  ".join(links), s["contact"])])
        tbl = Table(rows, colWidths=[W])
        tbl.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (-1,-1), t["header_bg"]),
            ("TOPPADDING",    (0,0), (-1,-1), 14),
            ("BOTTOMPADDING", (0,0), (-1,-1), 14),
            ("LEFTPADDING",   (0,0), (-1,-1), 16),
            ("RIGHTPADDING",  (0,0), (-1,-1), 16),
        ]))
        return [tbl, Spacer(1, 10)]
    else:
        elems = [Paragraph(name, s["name"]), Spacer(1, 14)]
        if contacts:
            elems.append(Paragraph("  |  ".join(contacts), s["contact"]))
        if links:
            elems.append(Paragraph("  |  ".join(links), s["contact"]))
        elems.append(Spacer(1, 8))
        elems += _divider(t, space_before=0, space_after=10)
        return elems


def _summary(data, s, t, extra=0):
    txt = data.get("summary","").strip()
    if not txt: return []
    return _sec_header("Professional Summary", s, t, extra) + \
           [Paragraph(txt, s["body"]), Spacer(1, 8)]


def _skills(data, s, t, extra=0):
    skills = data.get("skills", {})
    if not skills: return []
    elems = _sec_header("Technical Skills", s, t, extra)
    if isinstance(skills, dict):
        rows = []
        for cat, val in skills.items():
            lst = val.get("skills", []) if isinstance(val, dict) else val
            if lst:
                rows.append([
                    Paragraph(f"{cat}:", s["skill_cat"]),
                    Paragraph(", ".join(lst), s["skill_val"]),
                ])
        if rows:
            tbl = Table(rows, colWidths=[3.5*cm, W-3.5*cm])
            tbl.setStyle(TableStyle([
                ("VALIGN",        (0,0), (-1,-1), "TOP"),
                ("TOPPADDING",    (0,0), (-1,-1), 3),
                ("BOTTOMPADDING", (0,0), (-1,-1), 3),
            ]))
            elems.append(tbl)
    else:
        elems.append(Paragraph(", ".join(skills), s["body"]))
    elems.append(Spacer(1, 4))
    return elems


def _experience(data, s, t):
    jobs = data.get("experience", [])
    if not jobs: return []
    elems = _sec_header("Work Experience", s, t)
    for job in jobs:
        title    = job.get("title","").strip()
        company  = job.get("company","").strip()
        duration = job.get("duration","").strip()
        if title:
            row = Table([[Paragraph(title, s["job_title"]),
                          Paragraph(duration, s["sub"])]],
                        colWidths=[W*0.65, W*0.35])
            row.setStyle(TableStyle([
                ("ALIGN",         (1,0), (1,0), "RIGHT"),
                ("VALIGN",        (0,0), (-1,-1), "TOP"),
                ("TOPPADDING",    (0,0), (-1,-1), 0),
                ("BOTTOMPADDING", (0,0), (-1,-1), 0),
            ]))
            elems.append(row)
        if company:
            elems.append(Paragraph(company, s["sub"]))
        for r in job.get("responsibilities",[]):
            if r.strip():
                elems.append(Paragraph(f"• {r.strip()}", s["bullet"]))
        elems.append(Spacer(1, 6))
    return elems


def _education(data, s, t):
    edus = data.get("education", [])
    if not edus: return []
    elems = _sec_header("Education", s, t)
    for edu in edus:
        degree = edu.get("degree","").strip()
        inst   = edu.get("institution","").strip()
        year   = edu.get("year","").strip()
        gpa    = edu.get("gpa","").strip()
        if degree:
            row = Table([[Paragraph(degree, s["job_title"]),
                          Paragraph(year, s["sub"])]],
                        colWidths=[W*0.65, W*0.35])
            row.setStyle(TableStyle([
                ("ALIGN",         (1,0), (1,0), "RIGHT"),
                ("VALIGN",        (0,0), (-1,-1), "TOP"),
                ("TOPPADDING",    (0,0), (-1,-1), 0),
                ("BOTTOMPADDING", (0,0), (-1,-1), 0),
            ]))
            elems.append(row)
        sub = inst + (f"  |  GPA: {gpa}" if gpa else "")
        if sub: elems.append(Paragraph(sub, s["sub"]))
        elems.append(Spacer(1, 5))
    return elems


def _projects(data, s, t):
    projs = data.get("projects", [])
    if not projs: return []
    elems = _sec_header("Projects", s, t)
    for p in projs:
        title = p.get("title","").strip()
        link  = p.get("link","").strip()
        tech  = p.get("tech",[])
        desc  = p.get("description","").strip()
        if title:
            elems.append(Paragraph(f"{title}{' | '+link if link else ''}", s["job_title"]))
        if tech:
            elems.append(Paragraph(f"Tech: {', '.join(tech)}", s["sub"]))
        for line in desc.split("\n"):
            if line.strip():
                elems.append(Paragraph(f"• {line.strip()}", s["bullet"]))
        elems.append(Spacer(1, 6))
    return elems


def _certifications(data, s, t):
    certs = data.get("certifications", [])
    if not certs: return []
    elems = _sec_header("Certifications", s, t)
    for c in certs:
        elems.append(Paragraph(f"• {str(c).strip()}", s["bullet"]))
    elems.append(Spacer(1, 4))
    return elems


def build_resume_pdf(resume_data: dict, template: str = "Modern") -> bytes:
    t = TEMPLATES.get(template, TEMPLATES["Modern"])
    s = _styles(t)
    lm, rm, tm, bm = t["margins"]

    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
        leftMargin=lm, rightMargin=rm,
        topMargin=tm, bottomMargin=bm)

    extra = 16 if template in ("Minimal", "Creative") else 0

    elems = []
    elems += _header(resume_data, s, t)
    elems += _summary(resume_data, s, t, extra)
    elems += _skills(resume_data, s, t, extra)
    elems += _experience(resume_data, s, t)
    elems += _education(resume_data, s, t)
    elems += _projects(resume_data, s, t)
    elems += _certifications(resume_data, s, t)

    doc.build(elems)
    return buf.getvalue()


def validate_resume_data(data: dict) -> list[str]:
    errors = []
    if not data.get("name","").strip():  errors.append("Name is required.")
    if not data.get("email","").strip(): errors.append("Email is required.")
    if not data.get("education"):        errors.append("At least one education entry is required.")
    return errors
