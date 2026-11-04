"""Top navigation bar component."""

import reflex as rx
from habit_tracker.styles.theme import (
    SURFACE, BORDER, TEXT_PRIMARY, TEXT_MUTED, ACCENT, XP_COLOR
)
from habit_tracker.state.auth_state import AuthState
from habit_tracker.state.gamification_state import GamificationState


def navbar() -> rx.Component:
    return rx.box(
        rx.hstack(
            # Logo
            rx.hstack(
                rx.text("⚡", font_size="22px"),
                rx.text(
                    "HabitAI",
                    font_size="18px",
                    font_weight="800",
                    background=f"linear-gradient(90deg, {ACCENT}, {XP_COLOR})",
                    background_clip="text",
                    color="transparent",
                ),
                spacing="1",
                align="center",
            ),
            rx.spacer(),
            # Nav links
            rx.cond(
                AuthState.is_authenticated,
                rx.hstack(
                    rx.link("Dashboard", href="/dashboard", color=TEXT_MUTED, _hover={"color": TEXT_PRIMARY}, font_size="14px"),
                    rx.link("Habits", href="/habits", color=TEXT_MUTED, _hover={"color": TEXT_PRIMARY}, font_size="14px"),
                    rx.link("Coach", href="/coach", color=TEXT_MUTED, _hover={"color": TEXT_PRIMARY}, font_size="14px"),
                    rx.link("Profile", href="/profile", color=TEXT_MUTED, _hover={"color": TEXT_PRIMARY}, font_size="14px"),
                    rx.divider(orientation="vertical", height="20px", color=BORDER),
                    rx.button(
                        "Logout",
                        on_click=AuthState.logout,
                        background="transparent",
                        color=TEXT_MUTED,
                        border=f"1px solid {BORDER}",
                        border_radius="8px",
                        padding="6px 14px",
                        font_size="13px",
                        cursor="pointer",
                        _hover={"color": TEXT_PRIMARY},
                    ),
                    spacing="4",
                    align="center",
                ),
                rx.hstack(
                    rx.link("Login", href="/login", color=TEXT_MUTED, _hover={"color": TEXT_PRIMARY}, font_size="14px"),
                    rx.link("Register", href="/register", color=TEXT_MUTED, _hover={"color": TEXT_PRIMARY}, font_size="14px"),
                    spacing="4",
                ),
            ),
            width="100%",
            align="center",
        ),
        padding="0 32px",
        height="60px",
        background=SURFACE,
        border_bottom=f"1px solid {BORDER}",
        position="sticky",
        top="0",
        z_index="100",
        display="flex",
        align_items="center",
    )
