"""XP progress bar component."""

import reflex as rx
from habit_tracker.styles.theme import (
    SURFACE, BORDER, XP_COLOR, TEXT_PRIMARY, TEXT_MUTED, ACCENT, SURFACE2
)
from habit_tracker.state.gamification_state import GamificationState


def xp_bar() -> rx.Component:
    """Animated XP bar with level, XP count, and progress fill."""
    return rx.box(
        # Header row
        rx.hstack(
            rx.hstack(
                rx.text("⚡", font_size="18px"),
                rx.text(
                    rx.text.span("Level ", color=TEXT_MUTED),
                    rx.text.span(
                        rx.cond(
                            GamificationState.level > 0,
                            GamificationState.level.to_string(),
                            "1",
                        ),
                        color=XP_COLOR,
                        font_weight="700",
                    ),
                    font_size="15px",
                ),
                spacing="1",
                align="center",
            ),
            rx.spacer(),
            rx.text(
                GamificationState.total_xp.to_string() + " XP",
                font_size="13px",
                color=TEXT_MUTED,
            ),
            width="100%",
            align="center",
        ),
        # Progress bar track
        rx.box(
            rx.box(
                width=GamificationState.xp_progress_pct.to_string() + "%",
                height="100%",
                background=f"linear-gradient(90deg, {ACCENT} 0%, {XP_COLOR} 100%)",
                border_radius="99px",
                transition="width 0.6s cubic-bezier(.4,0,.2,1)",
                box_shadow=f"0 0 12px {ACCENT}88",
            ),
            width="100%",
            height="10px",
            background=SURFACE2,
            border_radius="99px",
            overflow="hidden",
            margin_top="8px",
        ),
        # Sub-label
        rx.text(
            "Next level: ", GamificationState.xp_for_next_level.to_string(), " XP",
            font_size="11px",
            color=TEXT_MUTED,
            margin_top="4px",
        ),
        padding="16px",
        background=SURFACE,
        border=f"1px solid {BORDER}",
        border_radius="12px",
        width="100%",
    )
