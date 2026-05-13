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


# ═══════════════════════════════════════════════════════════════════════════
# CLASSIC — dedicated builder: centered header, double-rule, centered section
#           headers sandwiched between two HR lines, traditional spacing
# ═══════════════════════════════════════════════════════════════════════════

def _classic_styles() -> dict:
    BLACK  = colors.HexColor("#000000")
    DARK   = colors.HexColor("#1a1a1a")
    GRAY   = colors.HexColor("#444444")
    LGRAY  = colors.HexColor("#666666")
    return {
        "name": ParagraphStyle("c_name",
            fontSize=22, fontName="Times-Bold",
            textColor=BLACK, alignment=TA_CENTER,
            spaceAfter=4, leading=26),
        "title_line": ParagraphStyle("c_title_line",
            fontSize=10, fontName="Times-Italic",
            textColor=GRAY, alignment=TA_CENTER,
            spaceAfter=3, leading=14),
        "contact": ParagraphStyle("c_contact",
            fontSize=9, fontName="Times-Roman",
            textColor=GRAY, alignment=TA_CENTER,
            spaceAfter=2, leading=14),
        "sec_hdr": ParagraphStyle("c_sec_hdr",
            fontSize=10.5, fontName="Times-Bold",
            textColor=BLACK, alignment=TA_CENTER,
            spaceBefore=0, spaceAfter=0, leading=14),
        "body": ParagraphStyle("c_body",
            fontSize=10, fontName="Times-Roman",
            textColor=DARK, spaceAfter=4, leading=15),
        "bullet": ParagraphStyle("c_bullet",
            fontSize=10, fontName="Times-Roman",
            textColor=DARK, spaceAfter=3, leading=14, leftIndent=14),
        "job_title": ParagraphStyle("c_job_title",
            fontSize=10.5, fontName="Times-Bold",
            textColor=BLACK, spaceAfter=1, leading=14),
        "company": ParagraphStyle("c_company",
            fontSize=10, fontName="Times-Italic",
            textColor=GRAY, spaceAfter=3, leading=13),
        "sub": ParagraphStyle("c_sub",
            fontSize=9.5, fontName="Times-Italic",
            textColor=LGRAY, spaceAfter=3, leading=13),
        "skill_cat": ParagraphStyle("c_skill_cat",
            fontSize=10, fontName="Times-Bold",
            textColor=BLACK, spaceAfter=2, leading=14),
        "skill_val": ParagraphStyle("c_skill_val",
            fontSize=10, fontName="Times-Roman",
            textColor=DARK, spaceAfter=2, leading=14),
    }


def _classic_sec(title: str, s: dict) -> list:
    """Section header: thin HR · CENTERED ALL-CAPS TITLE · thick HR"""
    return [
        Spacer(1, 10),
        HRFlowable(width="100%", thickness=0.5, color=colors.black, spaceAfter=3),
        Paragraph(title.upper(), s["sec_hdr"]),
        HRFlowable(width="100%", thickness=1.5, color=colors.black, spaceAfter=6),
    ]


def _classic_header(data: dict, s: dict, W: float) -> list:
    name     = data.get("name", "").strip()
    email    = data.get("email", "").strip()
    phone    = data.get("phone", "").strip()
    location = data.get("location", "").strip()
    linkedin = data.get("linkedin", "").strip()
    github   = data.get("github", "").strip()

    contacts = "  ·  ".join(filter(None, [email, phone, location]))
    links    = "  ·  ".join(filter(None, [linkedin, github]))

    elems = [
        HRFlowable(width="100%", thickness=2.5, color=colors.black, spaceAfter=6),
        Paragraph(name, s["name"]),
    ]
    if contacts:
        elems.append(Paragraph(contacts, s["contact"]))
    if links:
        elems.append(Paragraph(links, s["contact"]))
    elems += [
        Spacer(1, 5),
        HRFlowable(width="100%", thickness=2.5, color=colors.black, spaceAfter=8),
    ]
    return elems


def _classic_summary(data: dict, s: dict) -> list:
    txt = data.get("summary", "").strip()
    if not txt: return []
    return _classic_sec("Objective", s) + [Paragraph(txt, s["body"]), Spacer(1, 4)]


def _classic_skills(data: dict, s: dict, W: float) -> list:
    skills = data.get("skills", {})
    if not skills: return []
    elems = _classic_sec("Skills", s)
    rows = []
    for cat, val in skills.items():
        lst = val.get("skills", []) if isinstance(val, dict) else val
        if lst:
            rows.append([
                Paragraph(f"{cat}:", s["skill_cat"]),
                Paragraph(", ".join(lst), s["skill_val"]),
            ])
    if rows:
        tbl = Table(rows, colWidths=[3.8*cm, W - 3.8*cm])
        tbl.setStyle(TableStyle([
            ("VALIGN",        (0,0), (-1,-1), "TOP"),
            ("TOPPADDING",    (0,0), (-1,-1), 2),
            ("BOTTOMPADDING", (0,0), (-1,-1), 2),
            ("LEFTPADDING",   (0,0), (0,-1), 0),
        ]))
        elems.append(tbl)
    elems.append(Spacer(1, 4))
    return elems


def _classic_experience(data: dict, s: dict, W: float) -> list:
    jobs = data.get("experience", [])
    if not jobs: return []
    elems = _classic_sec("Work Experience", s)
    for job in jobs:
        title    = job.get("title", "").strip()
        company  = job.get("company", "").strip()
        duration = job.get("duration", "").strip()
        if title:
            row = Table(
                [[Paragraph(title, s["job_title"]), Paragraph(duration, s["sub"])]],
                colWidths=[W * 0.65, W * 0.35]
            )
            row.setStyle(TableStyle([
                ("ALIGN",         (1,0), (1,0), "RIGHT"),
                ("VALIGN",        (0,0), (-1,-1), "TOP"),
                ("TOPPADDING",    (0,0), (-1,-1), 0),
                ("BOTTOMPADDING", (0,0), (-1,-1), 0),
            ]))
            elems.append(row)
        if company:
            elems.append(Paragraph(company, s["company"]))
        for r in job.get("responsibilities", []):
            if r.strip():
                elems.append(Paragraph(f"• {r.strip()}", s["bullet"]))
        elems.append(Spacer(1, 5))
    return elems


def _classic_education(data: dict, s: dict, W: float) -> list:
    edus = data.get("education", [])
    if not edus: return []
    elems = _classic_sec("Education", s)
    for edu in edus:
        degree = edu.get("degree", "").strip()
        inst   = edu.get("institution", "").strip()
        year   = edu.get("year", "").strip()
        gpa    = edu.get("gpa", "").strip()
        if degree:
            row = Table(
                [[Paragraph(degree, s["job_title"]), Paragraph(year, s["sub"])]],
                colWidths=[W * 0.65, W * 0.35]
            )
            row.setStyle(TableStyle([
                ("ALIGN",         (1,0), (1,0), "RIGHT"),
                ("VALIGN",        (0,0), (-1,-1), "TOP"),
                ("TOPPADDING",    (0,0), (-1,-1), 0),
                ("BOTTOMPADDING", (0,0), (-1,-1), 0),
            ]))
            elems.append(row)
        sub = inst + (f"  |  GPA: {gpa}" if gpa else "")
        if sub:
            elems.append(Paragraph(sub, s["company"]))
        elems.append(Spacer(1, 5))
    return elems


def _classic_projects(data: dict, s: dict) -> list:
    projs = data.get("projects", [])
    if not projs: return []
    elems = _classic_sec("Projects", s)
    for p in projs:
        title = p.get("title", "").strip()
        link  = p.get("link", "").strip()
        tech  = p.get("tech", [])
        desc  = p.get("description", "").strip()
        if title:
            elems.append(Paragraph(f"{title}{' | ' + link if link else ''}", s["job_title"]))
        if tech:
            elems.append(Paragraph(f"Technologies: {', '.join(tech)}", s["company"]))
        for line in desc.split("\n"):
            if line.strip():
                elems.append(Paragraph(f"• {line.strip()}", s["bullet"]))
        elems.append(Spacer(1, 5))
    return elems


def _classic_certifications(data: dict, s: dict) -> list:
    certs = data.get("certifications", [])
    if not certs: return []
    elems = _classic_sec("Certifications", s)
    for c in certs:
        elems.append(Paragraph(f"• {str(c).strip()}", s["bullet"]))
    elems.append(Spacer(1, 4))
    return elems


def _build_classic(resume_data: dict) -> bytes:
    LM = RM = 2.0 * cm
    TM = BM = 2.0 * cm
    page_w = A4[0]
    CW = page_w - LM - RM  # usable content width

    s   = _classic_styles()
    buf = io.BytesIO()
    try:
        doc = SimpleDocTemplate(buf, pagesize=A4,
            leftMargin=LM, rightMargin=RM,
            topMargin=TM, bottomMargin=BM)
        elems = []
        elems += _classic_header(resume_data, s, CW)
        elems += _classic_summary(resume_data, s)
        elems += _classic_skills(resume_data, s, CW)
        elems += _classic_experience(resume_data, s, CW)
        elems += _classic_education(resume_data, s, CW)
        elems += _classic_projects(resume_data, s)
        elems += _classic_certifications(resume_data, s)
        doc.build(elems)
        return buf.getvalue()
    finally:
        buf.close()


# ═══════════════════════════════════════════════════════════════════════════
# MODERN — two-column layout: dark indigo sidebar (contact/skills/education)
#          + white main column (summary/experience/projects/certs)
# ═══════════════════════════════════════════════════════════════════════════

INDIGO      = colors.HexColor("#1e1b4b")
INDIGO_MID  = colors.HexColor("#312e81")
INDIGO_ACC  = colors.HexColor("#818cf8")
WHITE       = colors.white
OFF_WHITE   = colors.HexColor("#f8f9ff")
DARK_TEXT   = colors.HexColor("#1f2937")
GRAY_TEXT   = colors.HexColor("#6b7280")
ACCENT_LINE = colors.HexColor("#4f46e5")


def _m_styles() -> dict:
    return {
        # ── header band ──
        "name":      ParagraphStyle("m_name",      fontSize=22, fontName="Helvetica-Bold",
                         textColor=WHITE, alignment=TA_LEFT, spaceAfter=3, leading=26),
        "headline":  ParagraphStyle("m_headline",  fontSize=10, fontName="Helvetica",
                         textColor=INDIGO_ACC, alignment=TA_LEFT, spaceAfter=0, leading=14),
        # ── sidebar ──
        "sb_sec":    ParagraphStyle("m_sb_sec",    fontSize=8, fontName="Helvetica-Bold",
                         textColor=INDIGO_ACC, spaceBefore=10, spaceAfter=4,
                         leading=11),
        "sb_label":  ParagraphStyle("m_sb_label",  fontSize=8, fontName="Helvetica-Bold",
                         textColor=WHITE, spaceAfter=1, leading=11),
        "sb_val":    ParagraphStyle("m_sb_val",    fontSize=8, fontName="Helvetica",
                         textColor=colors.HexColor("#c7d2fe"), spaceAfter=4, leading=12),
        "sb_skill":  ParagraphStyle("m_sb_skill",  fontSize=8, fontName="Helvetica",
                         textColor=WHITE, spaceAfter=3, leading=12),
        "sb_deg":    ParagraphStyle("m_sb_deg",    fontSize=8, fontName="Helvetica-Bold",
                         textColor=WHITE, spaceAfter=1, leading=11),
        "sb_inst":   ParagraphStyle("m_sb_inst",   fontSize=7.5, fontName="Helvetica-Oblique",
                         textColor=colors.HexColor("#c7d2fe"), spaceAfter=4, leading=11),
        # ── main column ──
        "sec_hdr":   ParagraphStyle("m_sec_hdr",   fontSize=10.5, fontName="Helvetica-Bold",
                         textColor=ACCENT_LINE, spaceBefore=0, spaceAfter=3, leading=14),
        "body":      ParagraphStyle("m_body",      fontSize=9.5, fontName="Helvetica",
                         textColor=DARK_TEXT, spaceAfter=4, leading=14),
        "job_title": ParagraphStyle("m_job_title", fontSize=10, fontName="Helvetica-Bold",
                         textColor=DARK_TEXT, spaceAfter=1, leading=13),
        "company":   ParagraphStyle("m_company",   fontSize=9, fontName="Helvetica",
                         textColor=ACCENT_LINE, spaceAfter=3, leading=12),
        "duration":  ParagraphStyle("m_duration",  fontSize=8.5, fontName="Helvetica-Oblique",
                         textColor=GRAY_TEXT, spaceAfter=0, leading=12, alignment=TA_RIGHT),
        "bullet":    ParagraphStyle("m_bullet",    fontSize=9.5, fontName="Helvetica",
                         textColor=DARK_TEXT, spaceAfter=2, leading=13, leftIndent=10),
        "proj_tech": ParagraphStyle("m_proj_tech", fontSize=8.5, fontName="Helvetica-Oblique",
                         textColor=GRAY_TEXT, spaceAfter=3, leading=12),
    }


def _m_sec(title: str, s: dict, col_w: float) -> list:
    """Main-column section header: colored title + indigo underline."""
    return [
        Spacer(1, 10),
        Paragraph(title.upper(), s["sec_hdr"]),
        HRFlowable(width=col_w, thickness=1.5, color=ACCENT_LINE, spaceAfter=5),
    ]


def _m_sb_sec(title: str, s: dict) -> list:
    """Sidebar section header: accent-colored ALL CAPS label."""
    return [
        HRFlowable(width="100%", thickness=0.5,
                   color=colors.HexColor("#4338ca"), spaceAfter=4),
        Paragraph(title.upper(), s["sb_sec"]),
    ]


def _m_sidebar(data: dict, s: dict) -> list:
    """Build all sidebar content: contact → skills → education."""
    elems = [Spacer(1, 6)]

    # Contact
    elems += _m_sb_sec("Contact", s)
    for key, label in [("email", "Email"), ("phone", "Phone"),
                       ("location", "Location"), ("linkedin", "LinkedIn"),
                       ("github", "GitHub")]:
        val = data.get(key, "").strip()
        if val:
            elems.append(Paragraph(label, s["sb_label"]))
            elems.append(Paragraph(val,   s["sb_val"]))

    # Skills
    skills = data.get("skills", {})
    if skills:
        elems += _m_sb_sec("Skills", s)
        for cat, val in skills.items():
            lst = val.get("skills", []) if isinstance(val, dict) else val
            if lst:
                elems.append(Paragraph(cat, s["sb_label"]))
                elems.append(Paragraph(", ".join(lst), s["sb_skill"]))

    # Education
    edus = data.get("education", [])
    if edus:
        elems += _m_sb_sec("Education", s)
        for edu in edus:
            deg  = edu.get("degree", "").strip()
            inst = edu.get("institution", "").strip()
            yr   = edu.get("year", "").strip()
            gpa  = edu.get("gpa", "").strip()
            if deg:
                elems.append(Paragraph(deg, s["sb_deg"]))
            sub = "  |  ".join(filter(None, [inst, yr, (f"GPA {gpa}" if gpa else "")]))
            if sub:
                elems.append(Paragraph(sub, s["sb_inst"]))

    # Certifications
    certs = data.get("certifications", [])
    if certs:
        elems += _m_sb_sec("Certifications", s)
        for c in certs:
            elems.append(Paragraph(f"• {str(c).strip()}", s["sb_skill"]))

    return elems


def _m_main(data: dict, s: dict, col_w: float) -> list:
    """Build main-column content: summary → experience → projects."""
    elems = [Spacer(1, 6)]

    # Summary
    summary = data.get("summary", "").strip()
    if summary:
        elems += _m_sec("Profile", s, col_w)
        elems.append(Paragraph(summary, s["body"]))

    # Experience
    jobs = data.get("experience", [])
    if jobs:
        elems += _m_sec("Experience", s, col_w)
        for job in jobs:
            title    = job.get("title", "").strip()
            company  = job.get("company", "").strip()
            duration = job.get("duration", "").strip()
            if title:
                row = Table(
                    [[Paragraph(title, s["job_title"]),
                      Paragraph(duration, s["duration"])]],
                    colWidths=[col_w * 0.62, col_w * 0.38]
                )
                row.setStyle(TableStyle([
                    ("VALIGN",        (0,0), (-1,-1), "TOP"),
                    ("TOPPADDING",    (0,0), (-1,-1), 0),
                    ("BOTTOMPADDING", (0,0), (-1,-1), 0),
                    ("LEFTPADDING",   (0,0), (-1,-1), 0),
                    ("RIGHTPADDING",  (0,0), (-1,-1), 0),
                ]))
                elems.append(row)
            if company:
                elems.append(Paragraph(company, s["company"]))
            for r in job.get("responsibilities", []):
                if r.strip():
                    elems.append(Paragraph(f"• {r.strip()}", s["bullet"]))
            elems.append(Spacer(1, 5))

    # Projects
    projs = data.get("projects", [])
    if projs:
        elems += _m_sec("Projects", s, col_w)
        for p in projs:
            title = p.get("title", "").strip()
            link  = p.get("link", "").strip()
            tech  = p.get("tech", [])
            desc  = p.get("description", "").strip()
            if title:
                elems.append(Paragraph(
                    f"{title}{' · ' + link if link else ''}", s["job_title"]))
            if tech:
                elems.append(Paragraph(f"Stack: {', '.join(tech)}", s["proj_tech"]))
            for line in desc.split("\n"):
                if line.strip():
                    elems.append(Paragraph(f"• {line.strip()}", s["bullet"]))
            elems.append(Spacer(1, 5))

    return elems


def _build_modern(resume_data: dict) -> bytes:
    PAGE_W    = A4[0]
    OUTER_PAD = 1.5 * cm
    SB_W      = 5.8 * cm
    GUTTER    = 0.35 * cm
    MAIN_W    = PAGE_W - (2 * OUTER_PAD) - SB_W - GUTTER

    s = _m_styles()

    # ── Full-width header band ────────────────────────────────────────────
    name     = resume_data.get("name", "").strip()
    headline = resume_data.get("summary", "").strip()
    headline_short = (headline[:90] + "…") if len(headline) > 90 else headline

    header_content = [Paragraph(name, s["name"])]
    if headline_short:
        header_content.append(Paragraph(headline_short, s["headline"]))

    header_tbl = Table([[header_content]], colWidths=[PAGE_W - 2 * OUTER_PAD])
    header_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), INDIGO),
        ("TOPPADDING",    (0,0), (-1,-1), 14),
        ("BOTTOMPADDING", (0,0), (-1,-1), 14),
        ("LEFTPADDING",   (0,0), (-1,-1), 14),
        ("RIGHTPADDING",  (0,0), (-1,-1), 14),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ]))

    # ── Sidebar & main column ─────────────────────────────────────────────
    sb_elems   = _m_sidebar(resume_data, s)
    main_elems = _m_main(resume_data, s, MAIN_W)

    body_tbl = Table(
        [[sb_elems, main_elems]],
        colWidths=[SB_W, MAIN_W + GUTTER]
    )
    body_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (0,-1), INDIGO_MID),   # sidebar bg
        ("BACKGROUND",    (1,0), (1,-1), OFF_WHITE),     # main bg
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ("TOPPADDING",    (0,0), (0,-1), 10),
        ("BOTTOMPADDING", (0,0), (0,-1), 14),
        ("LEFTPADDING",   (0,0), (0,-1), 10),
        ("RIGHTPADDING",  (0,0), (0,-1), 10),
        ("TOPPADDING",    (1,0), (1,-1), 6),
        ("BOTTOMPADDING", (1,0), (1,-1), 14),
        ("LEFTPADDING",   (1,0), (1,-1), 14),
        ("RIGHTPADDING",  (1,0), (1,-1), 10),
    ]))

    buf = io.BytesIO()
    try:
        doc = SimpleDocTemplate(buf, pagesize=A4,
            leftMargin=OUTER_PAD, rightMargin=OUTER_PAD,
            topMargin=OUTER_PAD, bottomMargin=OUTER_PAD)
        doc.build([header_tbl, Spacer(1, 4), body_tbl])
        return buf.getvalue()
    finally:
        buf.close()


# ═══════════════════════════════════════════════════════════════════════════
# MINIMAL — ultra-clean, left-aligned, thin green accent lines only,
#           no background blocks, left-border accent on entries
# ═══════════════════════════════════════════════════════════════════════════

GREEN       = colors.HexColor("#059669")
GREEN_LIGHT = colors.HexColor("#d1fae5")
MIN_DARK    = colors.HexColor("#111827")
MIN_BODY    = colors.HexColor("#374151")
MIN_GRAY    = colors.HexColor("#6b7280")
MIN_LGRAY   = colors.HexColor("#9ca3af")


def _min_styles() -> dict:
    return {
        "name":      ParagraphStyle("mn_name",     fontSize=28, fontName="Helvetica-Bold",
                         textColor=MIN_DARK, alignment=TA_LEFT, spaceAfter=2, leading=32),
        "tagline":   ParagraphStyle("mn_tagline",  fontSize=10, fontName="Helvetica",
                         textColor=MIN_GRAY, alignment=TA_LEFT, spaceAfter=0, leading=14),
        "contact":   ParagraphStyle("mn_contact",  fontSize=9, fontName="Helvetica",
                         textColor=MIN_GRAY, alignment=TA_LEFT, spaceAfter=0, leading=13),
        "sec_hdr":   ParagraphStyle("mn_sec_hdr",  fontSize=11, fontName="Helvetica-Bold",
                         textColor=GREEN, alignment=TA_LEFT, spaceAfter=2, leading=14),
        "body":      ParagraphStyle("mn_body",     fontSize=9.5, fontName="Helvetica",
                         textColor=MIN_BODY, spaceAfter=4, leading=15),
        "job_title": ParagraphStyle("mn_jobtitle", fontSize=10, fontName="Helvetica-Bold",
                         textColor=MIN_DARK, spaceAfter=1, leading=13),
        "company":   ParagraphStyle("mn_company",  fontSize=9.5, fontName="Helvetica",
                         textColor=GREEN, spaceAfter=1, leading=13),
        "duration":  ParagraphStyle("mn_duration", fontSize=9, fontName="Helvetica-Oblique",
                         textColor=MIN_LGRAY, spaceAfter=0, leading=12, alignment=TA_RIGHT),
        "bullet":    ParagraphStyle("mn_bullet",   fontSize=9.5, fontName="Helvetica",
                         textColor=MIN_BODY, spaceAfter=2, leading=14, leftIndent=10),
        "skill_cat": ParagraphStyle("mn_skillcat", fontSize=9.5, fontName="Helvetica-Bold",
                         textColor=MIN_DARK, spaceAfter=3, leading=14),
        "skill_val": ParagraphStyle("mn_skillval", fontSize=9.5, fontName="Helvetica",
                         textColor=MIN_BODY, spaceAfter=3, leading=14),
        "cert":      ParagraphStyle("mn_cert",     fontSize=9.5, fontName="Helvetica",
                         textColor=MIN_BODY, spaceAfter=3, leading=14),
    }


def _min_sec(title: str, s: dict) -> list:
    """Section: green title + single thin green HR — no background, no uppercase."""
    return [
        Spacer(1, 14),
        Paragraph(title, s["sec_hdr"]),
        HRFlowable(width="100%", thickness=0.6, color=GREEN, spaceAfter=7),
    ]


def _min_left_border(inner: list, cw: float) -> Table:
    """Wrap content in a table that draws a 3pt green left border — no background."""
    tbl = Table([[inner]], colWidths=[cw])
    tbl.setStyle(TableStyle([
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("RIGHTPADDING",  (0,0), (-1,-1), 0),
        ("TOPPADDING",    (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 0),
        ("LINEBEFORE",    (0,0), (0,-1), 3, GREEN),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
    ]))
    return tbl


def _build_minimal(resume_data: dict) -> bytes:
    LM = RM = 2.2 * cm
    TM = BM = 2.0 * cm
    CW = A4[0] - LM - RM

    s = _min_styles()

    elems = []

    # ── Header ────────────────────────────────────────────────────────────
    name = resume_data.get("name", "").strip()
    elems.append(Paragraph(name, s["name"]))
    elems.append(HRFlowable(width="100%", thickness=1.5, color=GREEN, spaceAfter=6))

    contacts = "  ·  ".join(filter(None, [
        resume_data.get("email", "").strip(),
        resume_data.get("phone", "").strip(),
        resume_data.get("location", "").strip(),
        resume_data.get("linkedin", "").strip(),
        resume_data.get("github", "").strip(),
    ]))
    if contacts:
        elems.append(Paragraph(contacts, s["contact"]))
    elems.append(Spacer(1, 4))

    # ── Summary ───────────────────────────────────────────────────────────
    summary = resume_data.get("summary", "").strip()
    if summary:
        elems += _min_sec("Summary", s)
        elems.append(Paragraph(summary, s["body"]))

    # ── Skills ────────────────────────────────────────────────────────────
    skills = resume_data.get("skills", {})
    if skills:
        elems += _min_sec("Skills", s)
        for cat, val in skills.items():
            lst = val.get("skills", []) if isinstance(val, dict) else val
            if lst:
                row = Table(
                    [[Paragraph(f"{cat}", s["skill_cat"]),
                      Paragraph(", ".join(lst), s["skill_val"])]],
                    colWidths=[3.5 * cm, CW - 3.5 * cm]
                )
                row.setStyle(TableStyle([
                    ("VALIGN",        (0,0), (-1,-1), "TOP"),
                    ("TOPPADDING",    (0,0), (-1,-1), 0),
                    ("BOTTOMPADDING", (0,0), (-1,-1), 0),
                    ("LEFTPADDING",   (0,0), (-1,-1), 0),
                    ("RIGHTPADDING",  (0,0), (-1,-1), 0),
                ]))
                elems.append(row)

    # ── Experience ────────────────────────────────────────────────────────
    jobs = resume_data.get("experience", [])
    if jobs:
        elems += _min_sec("Experience", s)
        for job in jobs:
            title    = job.get("title", "").strip()
            company  = job.get("company", "").strip()
            duration = job.get("duration", "").strip()
            inner = []
            if title:
                hdr = Table(
                    [[Paragraph(title, s["job_title"]),
                      Paragraph(duration, s["duration"])]],
                    colWidths=[CW * 0.62, CW * 0.38 - 8]
                )
                hdr.setStyle(TableStyle([
                    ("VALIGN",        (0,0), (-1,-1), "TOP"),
                    ("TOPPADDING",    (0,0), (-1,-1), 0),
                    ("BOTTOMPADDING", (0,0), (-1,-1), 0),
                    ("LEFTPADDING",   (0,0), (-1,-1), 0),
                    ("RIGHTPADDING",  (0,0), (-1,-1), 0),
                ]))
                inner.append(hdr)
            if company:
                inner.append(Paragraph(company, s["company"]))
            for r in job.get("responsibilities", []):
                if r.strip():
                    inner.append(Paragraph(f"• {r.strip()}", s["bullet"]))
            if inner:
                elems.append(_min_left_border(inner, CW))
                elems.append(Spacer(1, 7))

    # ── Education ─────────────────────────────────────────────────────────
    edus = resume_data.get("education", [])
    if edus:
        elems += _min_sec("Education", s)
        for edu in edus:
            degree = edu.get("degree", "").strip()
            inst   = edu.get("institution", "").strip()
            year   = edu.get("year", "").strip()
            gpa    = edu.get("gpa", "").strip()
            inner = []
            if degree:
                hdr = Table(
                    [[Paragraph(degree, s["job_title"]),
                      Paragraph(year, s["duration"])]],
                    colWidths=[CW * 0.62, CW * 0.38 - 8]
                )
                hdr.setStyle(TableStyle([
                    ("VALIGN",        (0,0), (-1,-1), "TOP"),
                    ("TOPPADDING",    (0,0), (-1,-1), 0),
                    ("BOTTOMPADDING", (0,0), (-1,-1), 0),
                    ("LEFTPADDING",   (0,0), (-1,-1), 0),
                    ("RIGHTPADDING",  (0,0), (-1,-1), 0),
                ]))
                inner.append(hdr)
            sub = "  ·  ".join(filter(None, [inst, f"GPA: {gpa}" if gpa else ""]))
            if sub:
                inner.append(Paragraph(sub, s["company"]))
            if inner:
                elems.append(_min_left_border(inner, CW))
                elems.append(Spacer(1, 7))

    # ── Projects ──────────────────────────────────────────────────────────
    projs = resume_data.get("projects", [])
    if projs:
        elems += _min_sec("Projects", s)
        for p in projs:
            title = p.get("title", "").strip()
            link  = p.get("link", "").strip()
            tech  = p.get("tech", [])
            desc  = p.get("description", "").strip()
            inner = []
            if title:
                inner.append(Paragraph(
                    f"{title}{' — ' + link if link else ''}", s["job_title"]))
            if tech:
                inner.append(Paragraph(
                    f"Stack: {', '.join(tech)}", s["company"]))
            for line in desc.split("\n"):
                if line.strip():
                    inner.append(Paragraph(f"• {line.strip()}", s["bullet"]))
            if inner:
                elems.append(_min_left_border(inner, CW))
                elems.append(Spacer(1, 7))

    # ── Certifications ────────────────────────────────────────────────────
    certs = resume_data.get("certifications", [])
    if certs:
        elems += _min_sec("Certifications", s)
        for c in certs:
            elems.append(Paragraph(f"• {str(c).strip()}", s["cert"]))

    buf = io.BytesIO()
    try:
        doc = SimpleDocTemplate(buf, pagesize=A4,
            leftMargin=LM, rightMargin=RM,
            topMargin=TM, bottomMargin=BM)
        doc.build(elems)
        return buf.getvalue()
    finally:
        buf.close()


# ═══════════════════════════════════════════════════════════════════════════
# CREATIVE — full-width purple header band, 4pt purple left-border sections,
#            pill-style skill tags, tinted entry cards
# ═══════════════════════════════════════════════════════════════════════════

CR_PURPLE     = colors.HexColor("#7c3aed")
CR_PURPLE_MID = colors.HexColor("#6d28d9")
CR_PURPLE_BG  = colors.HexColor("#f5f3ff")
CR_PILL_BG    = colors.HexColor("#ede9fe")
CR_PILL_TEXT  = colors.HexColor("#5b21b6")
CR_DARK       = colors.HexColor("#1e1b4b")
CR_BODY       = colors.HexColor("#374151")
CR_GRAY       = colors.HexColor("#6b7280")
CR_WHITE      = colors.white


def _cr_styles() -> dict:
    return {
        "name":      ParagraphStyle("cr_name",     fontSize=26, fontName="Helvetica-Bold",
                         textColor=CR_WHITE, alignment=TA_LEFT, spaceAfter=3, leading=30),
        "role":      ParagraphStyle("cr_role",     fontSize=11, fontName="Helvetica",
                         textColor=colors.HexColor("#ddd6fe"), alignment=TA_LEFT,
                         spaceAfter=0, leading=15),
        "contact":   ParagraphStyle("cr_contact",  fontSize=8.5, fontName="Helvetica",
                         textColor=colors.HexColor("#c4b5fd"), alignment=TA_LEFT,
                         spaceAfter=0, leading=13),
        "sec_hdr":   ParagraphStyle("cr_sec_hdr",  fontSize=10, fontName="Helvetica-Bold",
                         textColor=CR_WHITE, alignment=TA_LEFT,
                         spaceBefore=0, spaceAfter=0, leading=13),
        "body":      ParagraphStyle("cr_body",     fontSize=9.5, fontName="Helvetica",
                         textColor=CR_BODY, spaceAfter=4, leading=15),
        "job_title": ParagraphStyle("cr_jobtitle", fontSize=10.5, fontName="Helvetica-Bold",
                         textColor=CR_DARK, spaceAfter=1, leading=14),
        "company":   ParagraphStyle("cr_company",  fontSize=9.5, fontName="Helvetica",
                         textColor=CR_PURPLE, spaceAfter=3, leading=13),
        "duration":  ParagraphStyle("cr_duration", fontSize=8.5, fontName="Helvetica-Oblique",
                         textColor=CR_GRAY, spaceAfter=0, leading=12, alignment=TA_RIGHT),
        "bullet":    ParagraphStyle("cr_bullet",   fontSize=9.5, fontName="Helvetica",
                         textColor=CR_BODY, spaceAfter=2, leading=14, leftIndent=10),
        "pill":      ParagraphStyle("cr_pill",     fontSize=8, fontName="Helvetica-Bold",
                         textColor=CR_PILL_TEXT, alignment=TA_CENTER,
                         spaceAfter=0, leading=11),
        "cert":      ParagraphStyle("cr_cert",     fontSize=9.5, fontName="Helvetica",
                         textColor=CR_BODY, spaceAfter=3, leading=14),
    }


def _cr_sec(title: str, s: dict, cw: float) -> list:
    """Section header: full-width purple bg block with 4pt left border + white ALL-CAPS text."""
    hdr_tbl = Table([[Paragraph(title.upper(), s["sec_hdr"])]], colWidths=[cw])
    hdr_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), CR_PURPLE),
        ("LINEBEFORE",    (0,0), (0,-1),  4, CR_PURPLE_MID),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 10),
        ("RIGHTPADDING",  (0,0), (-1,-1), 6),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ]))
    return [Spacer(1, 12), hdr_tbl, Spacer(1, 7)]


def _cr_entry_card(inner: list, cw: float) -> Table:
    """Wrap entry content in a light-purple tinted card with a 4pt purple left border."""
    tbl = Table([[inner]], colWidths=[cw])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), CR_PURPLE_BG),
        ("LINEBEFORE",    (0,0), (0,-1),  4, CR_PURPLE),
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING",   (0,0), (-1,-1), 10),
        ("RIGHTPADDING",  (0,0), (-1,-1), 8),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
    ]))
    return tbl


def _cr_pills(skills: list, s: dict, cw: float) -> Table:
    """Render a list of skills as pill-shaped tags in a wrapping row."""
    PILL_W = 2.6 * cm
    cols   = max(1, int(cw // PILL_W))
    rows   = []
    row    = []
    for i, skill in enumerate(skills):
        cell = Table([[Paragraph(skill, s["pill"])]], colWidths=[PILL_W - 0.15 * cm])
        cell.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (-1,-1), CR_PILL_BG),
            ("ROUNDEDCORNERS", [4, 4, 4, 4]),
            ("TOPPADDING",    (0,0), (-1,-1), 3),
            ("BOTTOMPADDING", (0,0), (-1,-1), 3),
            ("LEFTPADDING",   (0,0), (-1,-1), 5),
            ("RIGHTPADDING",  (0,0), (-1,-1), 5),
        ]))
        row.append(cell)
        if len(row) == cols or i == len(skills) - 1:
            while len(row) < cols:
                row.append("")
            rows.append(row)
            row = []
    if not rows:
        return Spacer(1, 0)
    pill_tbl = Table(rows, colWidths=[PILL_W] * cols)
    pill_tbl.setStyle(TableStyle([
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",    (0,0), (-1,-1), 2),
        ("BOTTOMPADDING", (0,0), (-1,-1), 2),
        ("LEFTPADDING",   (0,0), (-1,-1), 2),
        ("RIGHTPADDING",  (0,0), (-1,-1), 2),
    ]))
    return pill_tbl


def _build_creative(resume_data: dict) -> bytes:
    LM = RM = 1.8 * cm
    TM = BM = 0
    CW = A4[0] - LM - RM

    s = _cr_styles()
    elems = []

    # ── Full-width header band ────────────────────────────────────────────
    name     = resume_data.get("name", "").strip()
    summary  = resume_data.get("summary", "").strip()
    role_line = (summary[:80] + "…") if len(summary) > 80 else summary
    contacts = "   |   ".join(filter(None, [
        resume_data.get("email", "").strip(),
        resume_data.get("phone", "").strip(),
        resume_data.get("location", "").strip(),
        resume_data.get("linkedin", "").strip(),
        resume_data.get("github", "").strip(),
    ]))

    hdr_inner = [Paragraph(name, s["name"])]
    if role_line:
        hdr_inner.append(Paragraph(role_line, s["role"]))
    if contacts:
        hdr_inner.append(Spacer(1, 4))
        hdr_inner.append(Paragraph(contacts, s["contact"]))

    hdr_tbl = Table([[hdr_inner]], colWidths=[CW])
    hdr_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), CR_PURPLE),
        ("TOPPADDING",    (0,0), (-1,-1), 18),
        ("BOTTOMPADDING", (0,0), (-1,-1), 18),
        ("LEFTPADDING",   (0,0), (-1,-1), 16),
        ("RIGHTPADDING",  (0,0), (-1,-1), 16),
        ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ]))
    elems.append(hdr_tbl)
    elems.append(Spacer(1, 10))

    # ── Skills (pill tags) ────────────────────────────────────────────────
    skills = resume_data.get("skills", {})
    if skills:
        elems += _cr_sec("Skills", s, CW)
        for cat, val in skills.items():
            lst = val.get("skills", []) if isinstance(val, dict) else val
            if lst:
                cat_label = Table(
                    [[Paragraph(cat, ParagraphStyle("cr_cat",
                        fontSize=9, fontName="Helvetica-Bold",
                        textColor=CR_PURPLE, spaceAfter=2, leading=12))]],
                    colWidths=[CW]
                )
                cat_label.setStyle(TableStyle([
                    ("TOPPADDING",    (0,0), (-1,-1), 0),
                    ("BOTTOMPADDING", (0,0), (-1,-1), 2),
                    ("LEFTPADDING",   (0,0), (-1,-1), 0),
                    ("RIGHTPADDING",  (0,0), (-1,-1), 0),
                ]))
                elems.append(cat_label)
                elems.append(_cr_pills(lst, s, CW))
                elems.append(Spacer(1, 4))

    # ── Experience ────────────────────────────────────────────────────────
    jobs = resume_data.get("experience", [])
    if jobs:
        elems += _cr_sec("Experience", s, CW)
        for job in jobs:
            title    = job.get("title", "").strip()
            company  = job.get("company", "").strip()
            duration = job.get("duration", "").strip()
            inner = []
            if title:
                hdr = Table(
                    [[Paragraph(title, s["job_title"]),
                      Paragraph(duration, s["duration"])]],
                    colWidths=[CW * 0.63, CW * 0.37 - 14]
                )
                hdr.setStyle(TableStyle([
                    ("VALIGN",        (0,0), (-1,-1), "TOP"),
                    ("TOPPADDING",    (0,0), (-1,-1), 0),
                    ("BOTTOMPADDING", (0,0), (-1,-1), 0),
                    ("LEFTPADDING",   (0,0), (-1,-1), 0),
                    ("RIGHTPADDING",  (0,0), (-1,-1), 0),
                ]))
                inner.append(hdr)
            if company:
                inner.append(Paragraph(company, s["company"]))
            for r in job.get("responsibilities", []):
                if r.strip():
                    inner.append(Paragraph(f"• {r.strip()}", s["bullet"]))
            if inner:
                elems.append(_cr_entry_card(inner, CW))
                elems.append(Spacer(1, 6))

    # ── Education ─────────────────────────────────────────────────────────
    edus = resume_data.get("education", [])
    if edus:
        elems += _cr_sec("Education", s, CW)
        for edu in edus:
            degree = edu.get("degree", "").strip()
            inst   = edu.get("institution", "").strip()
            year   = edu.get("year", "").strip()
            gpa    = edu.get("gpa", "").strip()
            inner = []
            if degree:
                hdr = Table(
                    [[Paragraph(degree, s["job_title"]),
                      Paragraph(year, s["duration"])]],
                    colWidths=[CW * 0.63, CW * 0.37 - 14]
                )
                hdr.setStyle(TableStyle([
                    ("VALIGN",        (0,0), (-1,-1), "TOP"),
                    ("TOPPADDING",    (0,0), (-1,-1), 0),
                    ("BOTTOMPADDING", (0,0), (-1,-1), 0),
                    ("LEFTPADDING",   (0,0), (-1,-1), 0),
                    ("RIGHTPADDING",  (0,0), (-1,-1), 0),
                ]))
                inner.append(hdr)
            sub = "  |  ".join(filter(None, [inst, f"GPA: {gpa}" if gpa else ""]))
            if sub:
                inner.append(Paragraph(sub, s["company"]))
            if inner:
                elems.append(_cr_entry_card(inner, CW))
                elems.append(Spacer(1, 6))

    # ── Projects ──────────────────────────────────────────────────────────
    projs = resume_data.get("projects", [])
    if projs:
        elems += _cr_sec("Projects", s, CW)
        for p in projs:
            title = p.get("title", "").strip()
            link  = p.get("link", "").strip()
            tech  = p.get("tech", [])
            desc  = p.get("description", "").strip()
            inner = []
            if title:
                inner.append(Paragraph(
                    f"{title}{' — ' + link if link else ''}", s["job_title"]))
            if tech:
                inner.append(_cr_pills(tech, s, CW - 18))
                inner.append(Spacer(1, 3))
            for line in desc.split("\n"):
                if line.strip():
                    inner.append(Paragraph(f"• {line.strip()}", s["bullet"]))
            if inner:
                elems.append(_cr_entry_card(inner, CW))
                elems.append(Spacer(1, 6))

    # ── Certifications ────────────────────────────────────────────────────
    certs = resume_data.get("certifications", [])
    if certs:
        elems += _cr_sec("Certifications", s, CW)
        all_certs = [str(c).strip() for c in certs if str(c).strip()]
        if all_certs:
            elems.append(_cr_pills(all_certs, s, CW))

    buf = io.BytesIO()
    try:
        doc = SimpleDocTemplate(buf, pagesize=A4,
            leftMargin=LM, rightMargin=RM,
            topMargin=TM, bottomMargin=1.5 * cm)
        doc.build(elems)
        return buf.getvalue()
    finally:
        buf.close()


def build_resume_pdf(resume_data: dict, template: str = "Modern") -> bytes:
    if template == "Classic":
        return _build_classic(resume_data)
    if template == "Modern":
        return _build_modern(resume_data)
    if template == "Minimal":
        return _build_minimal(resume_data)
    if template == "Creative":
        return _build_creative(resume_data)

    t = TEMPLATES.get(template, TEMPLATES["Minimal"])
    s = _styles(t)
    lm, rm, tm, bm = t["margins"]

    buf = io.BytesIO()
    try:
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
    finally:
        buf.close()


def validate_resume_data(data: dict) -> list[str]:
    errors = []
    if not data.get("name","").strip():  errors.append("Name is required.")
    if not data.get("email","").strip(): errors.append("Email is required.")
    if not data.get("education"):        errors.append("At least one education entry is required.")
    return errors
