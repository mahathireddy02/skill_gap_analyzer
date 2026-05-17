"""Shared background and surface colors for the app."""

# Deep slate-navy with subtle sky/indigo ambient light
BG_ANIMATED = """
    radial-gradient(ellipse 90% 70% at 15% 0%, rgba(14, 165, 233, 0.09) 0%, transparent 55%),
    radial-gradient(ellipse 70% 60% at 85% 100%, rgba(99, 102, 241, 0.08) 0%, transparent 50%),
    linear-gradient(-45deg, #0a0e17, #0f172a, #152238, #0c1929)
""".strip().replace("\n", " ")

BG_STATIC = """
    radial-gradient(ellipse 80% 50% at 20% 0%, rgba(14, 165, 233, 0.07) 0%, transparent 50%),
    radial-gradient(ellipse 60% 40% at 90% 100%, rgba(99, 102, 241, 0.06) 0%, transparent 45%),
    linear-gradient(160deg, #0a0e17 0%, #0f172a 50%, #0c1929 100%)
""".strip().replace("\n", " ")

BG_LIGHT = "linear-gradient(180deg, #f8fafc 0%, #f1f5f9 55%, #e8f0f8 100%)"

COLOR_BG_DARK = "#0a0e17"
COLOR_NAV_DARK = "#080c14"
COLOR_BG_LIGHT = "#f8fafc"
COLOR_SURFACE_LIGHT = "#e8f0f8"
