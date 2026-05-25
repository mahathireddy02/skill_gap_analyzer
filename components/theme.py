"""Shared dark palette and surfaces for the app."""

TEXT_IVORY = "#FFFFF0"
BG_NAVY = "#333F63"
BG_BLACK_OVERLAY = "#000000D6"

BG_ANIMATED = """
    radial-gradient(ellipse 90% 70% at 18% 8%, rgba(255, 255, 240, 0.10) 0%, transparent 54%),
    radial-gradient(ellipse 70% 58% at 88% 92%, rgba(51, 63, 99, 0.55) 0%, transparent 58%),
    linear-gradient(180deg, #000000D6 0%, #333F63 52%, #333F63 100%)
""".strip().replace("\n", " ")

BG_STATIC = """
    radial-gradient(ellipse 82% 48% at 20% 4%, rgba(255, 255, 240, 0.08) 0%, transparent 52%),
    radial-gradient(ellipse 62% 42% at 92% 98%, rgba(51, 63, 99, 0.58) 0%, transparent 48%),
    linear-gradient(180deg, #000000D6 0%, #333F63 56%, #333F63 100%)
""".strip().replace("\n", " ")

BG_LIGHT = BG_STATIC

COLOR_BG_DARK = BG_NAVY
COLOR_NAV_DARK = BG_BLACK_OVERLAY
COLOR_BG_LIGHT = BG_NAVY
COLOR_SURFACE_LIGHT = "rgba(0, 0, 0, 0.30)"
