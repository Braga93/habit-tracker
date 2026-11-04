"""Habits management page — add, view, and delete habits."""

import reflex as rx
from habit_tracker.styles.theme import (
    BACKGROUND, SURFACE, BORDER, TEXT_PRIMARY, TEXT_MUTED, DANGER,
    input_style, button_primary, card_style
)
from habit_tracker.components.navbar import navbar
from habit_tracker.components.habit_card import habit_card
from habit_tracker.components.badge_panel import badge_toast
from habit_tracker.state.habit_state import HabitState

ICON_OPTIONS = ["🎯", "💪", "📚", "🧘", "🏃", "💧", "🥗", "💤", "✍️", "🎵", "🌿", "🧠"]


def _icon_picker() -> rx.Component:
    return rx.hstack(
        *[
            rx.button(
                icon,
                on_click=HabitState.set_new_icon(icon),
                background=rx.cond(
                    HabitState.new_icon == icon, "#7C3AED33", "transparent"
                ),
                border=rx.cond(
                    HabitState.new_icon == icon, "2px solid #7C3AED", f"1px solid {BORDER}"
                ),
                border_radius="8px",
                font_size="18px",
                padding="6px 10px",
                cursor="pointer",
            )
            for icon in ICON_OPTIONS
        ],
        wrap="wrap",
        spacing="1",
    )


def add_habit_form() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text("Add New Habit", font_size="18px", font_weight="700", color=TEXT_PRIMARY),
            rx.text("Define your habit using the Cue → Routine → Reward loop",
                    font_size="13px", color=TEXT_MUTED),

            # Error
            rx.cond(
                HabitState.habit_error != "",
                rx.box(
                    rx.text(HabitState.habit_error, color=DANGER, font_size="13px"),
                    background=f"{DANGER}18",
                    border=f"1px solid {DANGER}44",
                    border_radius="8px",
                    padding="10px 14px",
                    width="100%",
                ),
                rx.fragment(),
            ),

            rx.grid(
                rx.vstack(
                    rx.text("Habit Name *", font_size="13px", font_weight="600", color=TEXT_MUTED),
                    rx.input(placeholder="e.g. Morning Exercise", on_change=HabitState.set_new_name,
                             value=HabitState.new_name, style=input_style),
                    spacing="1",
                ),
                rx.vstack(
                    rx.text("🔔 Cue (Trigger) *", font_size="13px", font_weight="600", color=TEXT_MUTED),
                    rx.input(placeholder="e.g. Wake up at 7am", on_change=HabitState.set_new_cue,
                             value=HabitState.new_cue, style=input_style),
                    spacing="1",
                ),
                rx.vstack(
                    rx.text("⚙️ Routine (Action) *", font_size="13px", font_weight="600", color=TEXT_MUTED),
                    rx.input(placeholder="e.g. 20-minute jog", on_change=HabitState.set_new_routine,
                             value=HabitState.new_routine, style=input_style),
                    spacing="1",
                ),
                rx.vstack(
                    rx.text("🎁 Reward *", font_size="13px", font_weight="600", color=TEXT_MUTED),
                    rx.input(placeholder="e.g. Smoothie + good mood", on_change=HabitState.set_new_reward,
                             value=HabitState.new_reward, style=input_style),
                    spacing="1",
                ),
                columns="2",
                spacing="4",
                width="100%",
            ),

            rx.hstack(
                rx.vstack(
                    rx.text("Icon", font_size="13px", font_weight="600", color=TEXT_MUTED),
                    _icon_picker(),
                    spacing="1",
                    flex="1",
                ),
                rx.vstack(
                    rx.text("XP Reward", font_size="13px", font_weight="600", color=TEXT_MUTED),
                    rx.select(
                        ["10", "20", "30", "50", "75", "100"],
                        default_value="20",
                        on_change=HabitState.set_new_xp,
                        style=input_style,
                        width="120px",
                    ),
                    spacing="1",
                ),
                spacing="6",
                width="100%",
                align="end",
            ),

            rx.button(
                "＋ Add Habit",
                on_click=HabitState.add_habit,
                style=button_primary,
                font_size="15px",
                padding="12px 28px",
            ),
            spacing="4",
            width="100%",
            align="stretch",
        ),
        style=card_style,
        width="100%",
    )


def habits_page() -> rx.Component:
    return rx.box(
        navbar(),
        rx.box(
            rx.heading("My Habits", font_size="28px", font_weight="800", color=TEXT_PRIMARY, margin_bottom="4px"),
            rx.text("Manage your habit loop definitions", font_size="14px", color=TEXT_MUTED, margin_bottom="24px"),
            add_habit_form(),
            rx.box(height="8px"),
            rx.text(
                HabitState.habits.length().to_string() + " active habits",
                font_size="13px", color=TEXT_MUTED, margin_bottom="12px",
            ),
            rx.vstack(
                rx.foreach(HabitState.habits, habit_card),
                spacing="3",
                width="100%",
            ),
            padding="32px",
            max_width="900px",
            margin="0 auto",
        ),
        badge_toast(),
        background=BACKGROUND,
        min_height="100vh",
        on_mount=HabitState.load_habits,
    )
