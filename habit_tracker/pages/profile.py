"""User profile page — account info, stats, and all badges."""

import reflex as rx
from habit_tracker.styles.theme import (
    BACKGROUND, SURFACE, BORDER, TEXT_PRIMARY, TEXT_MUTED,
    ACCENT, XP_COLOR, SUCCESS, card_style
)
from habit_tracker.components.navbar import navbar
from habit_tracker.components.xp_bar import xp_bar
from habit_tracker.components.badge_panel import badge_panel
from habit_tracker.state.auth_state import AuthState
from habit_tracker.state.gamification_state import GamificationState
from habit_tracker.state.habit_state import HabitState


def profile_page() -> rx.Component:
    return rx.box(
        navbar(),
        rx.box(
            # Profile header
            rx.box(
                rx.hstack(
                    rx.box(
                        rx.text(
                            AuthState.username[:1].upper(),
                            font_size="32px",
                            font_weight="800",
                            color="white",
                        ),
                        width="72px",
                        height="72px",
                        background=f"linear-gradient(135deg, {ACCENT}, {XP_COLOR})",
                        border_radius="50%",
                        display="flex",
                        align_items="center",
                        justify_content="center",
                        flex_shrink="0",
                    ),
                    rx.vstack(
                        rx.text(AuthState.username, font_size="22px", font_weight="700", color=TEXT_PRIMARY),
                        rx.text(AuthState.email, font_size="13px", color=TEXT_MUTED),
                        rx.hstack(
                            rx.badge(
                                "Level ", GamificationState.level.to_string(),
                                color_scheme="purple",
                                font_size="12px",
                            ),
                            rx.badge(
                                "🔥 ", GamificationState.streak_days.to_string(), " day streak",
                                color_scheme="orange",
                                font_size="12px",
                            ),
                            spacing="2",
                        ),
                        spacing="1",
                        align_items="start",
                    ),
                    spacing="4",
                    align="center",
                ),
                style=card_style,
                width="100%",
                margin_bottom="0",
            ),

            # XP bar
            xp_bar(),

            # Stat cards row
            rx.hstack(
                rx.box(
                    rx.vstack(
                        rx.text("💯", font_size="24px"),
                        rx.text(GamificationState.total_xp.to_string(), font_size="24px", font_weight="800", color=XP_COLOR),
                        rx.text("Total XP", font_size="12px", color=TEXT_MUTED),
                        align="center", spacing="1",
                    ),
                    style=card_style, flex="1", text_align="center",
                ),
                rx.box(
                    rx.vstack(
                        rx.text("🏅", font_size="24px"),
                        rx.text(GamificationState.earned_badges.length().to_string(), font_size="24px", font_weight="800", color=SUCCESS),
                        rx.text("Badges Earned", font_size="12px", color=TEXT_MUTED),
                        align="center", spacing="1",
                    ),
                    style=card_style, flex="1", text_align="center",
                ),
                rx.box(
                    rx.vstack(
                        rx.text("📋", font_size="24px"),
                        rx.text(HabitState.habits.length().to_string(), font_size="24px", font_weight="800", color=ACCENT),
                        rx.text("Active Habits", font_size="12px", color=TEXT_MUTED),
                        align="center", spacing="1",
                    ),
                    style=card_style, flex="1", text_align="center",
                ),
                spacing="4",
                wrap="wrap",
                width="100%",
            ),

            # All badges
            badge_panel(),

            spacing="4",
            padding="32px",
            max_width="900px",
            margin="0 auto",
            display="flex",
            flex_direction="column",
        ),
        background=BACKGROUND,
        min_height="100vh",
        on_mount=[GamificationState.load_gamification, HabitState.load_habits],
    )
