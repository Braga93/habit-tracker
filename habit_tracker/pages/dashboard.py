"""Dashboard page — overview of stats, XP, heatmap, and today's habits."""

import reflex as rx
from habit_tracker.styles.theme import (
    BACKGROUND, SURFACE, BORDER, TEXT_PRIMARY, TEXT_MUTED,
    SUCCESS, XP_COLOR, ACCENT, card_style
)
from habit_tracker.components.navbar import navbar
from habit_tracker.components.xp_bar import xp_bar
from habit_tracker.components.badge_panel import badge_panel, badge_toast
from habit_tracker.components.habit_card import habit_card
from habit_tracker.components.progress_chart import heatmap_chart
from habit_tracker.state.habit_state import HabitState
from habit_tracker.state.gamification_state import GamificationState


def _stat_card(icon: str, label: str, value: rx.Component) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text(icon, font_size="24px"),
            value,
            rx.text(label, font_size="12px", color=TEXT_MUTED, font_weight="500"),
            spacing="1",
            align="center",
        ),
        style=card_style,
        text_align="center",
        flex="1",
        min_width="120px",
    )


def dashboard_page() -> rx.Component:
    return rx.box(
        navbar(),
        rx.box(
            # Stats row
            rx.hstack(
                _stat_card(
                    "🔥",
                    "Day Streak",
                    rx.text(GamificationState.streak_days.to_string(),
                            font_size="28px", font_weight="800", color=XP_COLOR),
                ),
                _stat_card(
                    "✅",
                    "Done Today",
                    rx.text(
                        HabitState.completed_today.length().to_string()
                        + " / "
                        + HabitState.habits.length().to_string(),
                        font_size="28px", font_weight="800", color=SUCCESS,
                    ),
                ),
                _stat_card(
                    "🎮",
                    "Level",
                    rx.text(GamificationState.level.to_string(),
                            font_size="28px", font_weight="800", color=ACCENT),
                ),
                _stat_card(
                    "💯",
                    "Total XP",
                    rx.text(GamificationState.total_xp.to_string(),
                            font_size="28px", font_weight="800", color=XP_COLOR),
                ),
                spacing="4",
                wrap="wrap",
                width="100%",
            ),

            # XP Bar + Heatmap row
            rx.grid(
                rx.vstack(xp_bar(), badge_panel(), spacing="4"),
                heatmap_chart(),
                columns="2",
                spacing="4",
                width="100%",
                template_columns=["1fr", "1fr 1fr"],
            ),

            # Today's habits
            rx.box(
                rx.hstack(
                    rx.text("Today's Habits", font_size="18px", font_weight="700", color=TEXT_PRIMARY),
                    rx.link("Manage Habits →", href="/habits", font_size="13px", color=ACCENT),
                    justify="between",
                    width="100%",
                ),
                rx.cond(
                    HabitState.habits.length() == 0,
                    rx.center(
                        rx.vstack(
                            rx.text("🌱", font_size="40px"),
                            rx.text("No habits yet. Add your first habit!", color=TEXT_MUTED, font_size="14px"),
                            rx.link(
                                rx.button("Add Habit", background=f"linear-gradient(135deg, #7C3AED, #A855F7)",
                                          color="white", border_radius="10px", padding="10px 24px",
                                          font_weight="600", cursor="pointer", border="none"),
                                href="/habits",
                            ),
                            align="center",
                            spacing="3",
                        ),
                        padding="40px",
                    ),
                    rx.vstack(
                        rx.foreach(HabitState.habits, habit_card),
                        spacing="3",
                        width="100%",
                    ),
                ),
                style=card_style,
                width="100%",
            ),
            spacing="5",
            padding="32px",
            max_width="1200px",
            margin="0 auto",
            display="flex",
            flex_direction="column",
        ),
        badge_toast(),
        background=BACKGROUND,
        min_height="100vh",
        on_mount=[HabitState.load_habits, GamificationState.load_gamification],
    )
