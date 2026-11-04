"""Badge panel and toast notification component."""

import reflex as rx
from typing import Dict, Any
from habit_tracker.styles.theme import (
    SURFACE, BORDER, TEXT_PRIMARY, TEXT_MUTED, ACCENT, SUCCESS, badge_locked_style
)
from habit_tracker.state.gamification_state import GamificationState
from habit_tracker.state.habit_state import HabitState


def _badge_tile(badge: Dict[str, Any]) -> rx.Component:
    """Single badge tile: shows icon + name, greyed out if not earned."""
    return rx.box(
        rx.vstack(
            rx.text(badge["icon"], font_size="28px"),
            rx.text(badge["name"], font_size="11px", font_weight="600", color=TEXT_PRIMARY),
            rx.text(badge["description"], font_size="10px", color=TEXT_MUTED, text_align="center"),
            spacing="1",
            align="center",
        ),
        padding="14px 10px",
        background=SURFACE,
        border=f"1px solid {BORDER}",
        border_radius="12px",
        style=rx.cond(badge["earned"], {}, badge_locked_style),
        min_width="100px",
        max_width="120px",
        text_align="center",
    )


def badge_panel() -> rx.Component:
    """Grid of all badges with earned/locked state."""
    return rx.box(
        rx.text("Achievements", font_size="18px", font_weight="700", color=TEXT_PRIMARY),
        rx.text(
            GamificationState.earned_badges.length().to_string()
            + " / "
            + GamificationState.all_badges.length().to_string()
            + " earned",
            font_size="13px",
            color=TEXT_MUTED,
            margin_bottom="14px",
        ),
        rx.flex(
            rx.foreach(GamificationState.all_badges, _badge_tile),
            wrap="wrap",
            gap="10px",
        ),
        padding="20px",
        background=SURFACE,
        border=f"1px solid {BORDER}",
        border_radius="16px",
        width="100%",
    )


def badge_toast() -> rx.Component:
    """Toast overlay shown when a new badge is unlocked."""
    return rx.cond(
        HabitState.new_badges.length() > 0,
        rx.box(
            rx.vstack(
                rx.text("🏅 Badge Unlocked!", font_size="14px", font_weight="700", color=TEXT_PRIMARY),
                rx.foreach(
                    HabitState.new_badges,
                    lambda b: rx.text(
                        b["icon"], " ", b["name"],
                        font_size="13px",
                        color=SUCCESS,
                        font_weight="600",
                    ),
                ),
                spacing="1",
            ),
            position="fixed",
            bottom="32px",
            right="32px",
            background=SURFACE,
            border=f"1px solid {SUCCESS}",
            border_radius="14px",
            padding="18px 24px",
            box_shadow=f"0 4px 32px {SUCCESS}44",
            z_index="1000",
        ),
        rx.fragment(),
    )
