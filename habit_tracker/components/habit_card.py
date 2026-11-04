"""Habit card component rendering cue/routine/reward + complete button."""

import reflex as rx
from typing import Dict, Any
from habit_tracker.styles.theme import (
    SURFACE, BORDER, TEXT_PRIMARY, TEXT_MUTED, SUCCESS, DANGER, XP_COLOR
)
from habit_tracker.state.habit_state import HabitState


def habit_card(habit: Dict[str, Any]) -> rx.Component:
    """A single habit card with loop details and daily check-in button."""
    is_done = HabitState.completed_today.contains(habit["id"])
    streak = HabitState.streaks[habit["id"].to_string()]

    return rx.box(
        rx.hstack(
            # Left: icon + name
            rx.vstack(
                rx.hstack(
                    rx.text(habit["icon"], font_size="22px"),
                    rx.text(habit["name"], font_size="16px", font_weight="700", color=TEXT_PRIMARY),
                    align="center",
                    spacing="2",
                ),
                # Habit loop pills
                rx.hstack(
                    rx.box(
                        rx.text("🔔 ", habit["cue"], font_size="11px", color=TEXT_MUTED),
                        padding="3px 8px",
                        background="#1E1E3A",
                        border_radius="6px",
                    ),
                    rx.text("→", color=TEXT_MUTED, font_size="12px"),
                    rx.box(
                        rx.text("⚙️ ", habit["routine"], font_size="11px", color=TEXT_MUTED),
                        padding="3px 8px",
                        background="#1E1E3A",
                        border_radius="6px",
                    ),
                    rx.text("→", color=TEXT_MUTED, font_size="12px"),
                    rx.box(
                        rx.text("🎁 ", habit["reward"], font_size="11px", color=TEXT_MUTED),
                        padding="3px 8px",
                        background="#1E1E3A",
                        border_radius="6px",
                    ),
                    wrap="wrap",
                    spacing="1",
                ),
                # Streak indicator
                rx.hstack(
                    rx.text("🔥", font_size="13px"),
                    rx.text(streak.to_string() + " day streak", font_size="12px", color=XP_COLOR),
                    rx.text(
                        "+", habit["xp_reward"].to_string(), " XP",
                        font_size="12px",
                        color=XP_COLOR,
                        font_weight="600",
                        margin_left="8px",
                    ),
                    spacing="1",
                    align="center",
                ),
                spacing="2",
                align_items="start",
            ),
            rx.spacer(),
            # Right: complete / done + delete
            rx.vstack(
                rx.cond(
                    is_done,
                    rx.button(
                        "✅ Done",
                        is_disabled=True,
                        background=f"{SUCCESS}22",
                        color=SUCCESS,
                        border=f"1px solid {SUCCESS}",
                        border_radius="10px",
                        padding="8px 18px",
                        font_weight="600",
                        cursor="not-allowed",
                    ),
                    rx.button(
                        "Mark Complete",
                        on_click=HabitState.complete_habit(habit["id"]),
                        background=f"linear-gradient(135deg, #7C3AED, #A855F7)",
                        color="white",
                        border_radius="10px",
                        padding="8px 18px",
                        font_weight="600",
                        cursor="pointer",
                        border="none",
                        _hover={"opacity": "0.85"},
                    ),
                ),
                rx.button(
                    "🗑",
                    on_click=HabitState.delete_habit(habit["id"]),
                    background="transparent",
                    color=DANGER,
                    border="none",
                    cursor="pointer",
                    font_size="16px",
                    _hover={"opacity": "0.7"},
                ),
                align="end",
                spacing="2",
            ),
            width="100%",
            align="start",
            spacing="4",
        ),
        padding="18px 20px",
        background=SURFACE,
        border=f"2px solid {habit['color']}44",
        border_radius="14px",
        width="100%",
        border_left=f"4px solid {habit['color']}",
        _hover={"box_shadow": f"0 2px 16px {habit['color']}22"},
        transition="box-shadow 0.2s ease",
    )
