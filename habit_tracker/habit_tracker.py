"""
Habit Tracker AI — main Reflex application entry point.

Routes, global styles, and app assembly.
"""

import reflex as rx
from sqlmodel import SQLModel

# ── Import all models so SQLModel knows about every table ─────────────────────
from habit_tracker.models import User, Habit, HabitLog, Badge, UserBadge, XPEvent  # noqa: F401

from habit_tracker.styles.theme import BACKGROUND, FONT_BODY
from habit_tracker.pages.index import index_page
from habit_tracker.pages.login import login_page
from habit_tracker.pages.register import register_page
from habit_tracker.pages.dashboard import dashboard_page
from habit_tracker.pages.habits import habits_page
from habit_tracker.pages.coach import coach_page
from habit_tracker.pages.profile import profile_page


def create_db_tables():
    """Create all SQLModel tables on startup (idempotent)."""
    from sqlmodel import create_engine
    engine = create_engine("sqlite:///habit_tracker.db")
    SQLModel.metadata.create_all(engine)


# ── Global stylesheet injected into every page ─────────────────────────────────
GLOBAL_STYLE = {
    "body": {
        "background_color": BACKGROUND,
        "font_family": f"'{FONT_BODY}', sans-serif",
        "margin": "0",
        "padding": "0",
        "-webkit-font-smoothing": "antialiased",
    },
    "*": {"box_sizing": "border-box"},
    "::selection": {"background": "#7C3AED44"},
    "::-webkit-scrollbar": {"width": "6px"},
    "::-webkit-scrollbar-track": {"background": "#0F0F1A"},
    "::-webkit-scrollbar-thumb": {"background": "#2D2D44", "border_radius": "3px"},
    "a": {"text_decoration": "none"},
}


# ── App assembly ───────────────────────────────────────────────────────────────
app = rx.App(style=GLOBAL_STYLE)

# Create DB tables once at startup (idempotent — safe to run every time)
create_db_tables()

app.add_page(index_page, route="/")
app.add_page(login_page, route="/login")
app.add_page(register_page, route="/register")
app.add_page(dashboard_page, route="/dashboard")
app.add_page(habits_page, route="/habits")
app.add_page(coach_page, route="/coach")
app.add_page(profile_page, route="/profile")
