"""
Visual theme for Habit Tracker AI — dark gamified palette.
"""

import reflex as rx

# ── Colour tokens ──────────────────────────────────────────────────────────────
BACKGROUND   = "#0F0F1A"   # deep dark
SURFACE      = "#1A1A2E"   # card / panel
SURFACE2     = "#16213E"   # elevated surface
BORDER       = "#2D2D44"
TEXT_PRIMARY = "#E2E8F0"
TEXT_MUTED   = "#94A3B8"
ACCENT       = "#7C3AED"   # violet
ACCENT_GLOW  = "#A855F7"
SUCCESS      = "#10B981"
WARNING      = "#F59E0B"
DANGER       = "#EF4444"
XP_COLOR     = "#FBBF24"   # golden XP

# ── Typography ─────────────────────────────────────────────────────────────────
FONT_HEADING = "Inter"
FONT_BODY    = "Inter"

# ── Shared style dicts ─────────────────────────────────────────────────────────
card_style = {
    "background": SURFACE,
    "border": f"1px solid {BORDER}",
    "border_radius": "16px",
    "padding": "24px",
    "box_shadow": "0 4px 24px rgba(124, 58, 237, 0.08)",
}

button_primary = {
    "background": f"linear-gradient(135deg, {ACCENT} 0%, {ACCENT_GLOW} 100%)",
    "color": "white",
    "border_radius": "10px",
    "padding": "10px 24px",
    "font_weight": "600",
    "cursor": "pointer",
    "border": "none",
    "_hover": {"opacity": 0.9, "transform": "translateY(-1px)"},
    "transition": "all 0.2s ease",
}

button_ghost = {
    "background": "transparent",
    "color": TEXT_MUTED,
    "border_radius": "10px",
    "padding": "8px 16px",
    "font_weight": "500",
    "cursor": "pointer",
    "border": f"1px solid {BORDER}",
    "_hover": {"color": TEXT_PRIMARY, "border_color": ACCENT},
    "transition": "all 0.2s ease",
}

input_style = {
    "background": SURFACE2,
    "border": f"1px solid {BORDER}",
    "border_radius": "10px",
    "color": TEXT_PRIMARY,
    "padding": "10px 14px",
    "_focus": {"border_color": ACCENT, "outline": "none"},
    "width": "100%",
}

badge_locked_style = {
    "opacity": "0.35",
    "filter": "grayscale(1)",
}
