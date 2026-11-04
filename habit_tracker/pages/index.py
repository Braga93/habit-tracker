"""Landing / home page."""

import reflex as rx
from habit_tracker.styles.theme import (
    BACKGROUND, TEXT_PRIMARY, TEXT_MUTED, ACCENT, XP_COLOR, button_primary
)
from habit_tracker.components.navbar import navbar


def index_page() -> rx.Component:
    return rx.box(
        navbar(),
        # Hero section
        rx.center(
            rx.vstack(
                rx.badge("✨ AI-Powered", color_scheme="purple", font_size="13px", padding="6px 14px"),
                rx.heading(
                    "Build Habits That Stick",
                    font_size=["32px", "48px", "60px"],
                    font_weight="800",
                    text_align="center",
                    background=f"linear-gradient(135deg, {TEXT_PRIMARY} 0%, {ACCENT} 100%)",
                    background_clip="text",
                    color="transparent",
                    line_height="1.1",
                ),
                rx.text(
                    "Gamified habit tracking with AI behavioral coaching. "
                    "Earn XP, unlock badges, and let your personal AI coach "
                    "guide you through the Cue → Routine → Reward cycle.",
                    font_size="18px",
                    color=TEXT_MUTED,
                    text_align="center",
                    max_width="560px",
                ),
                rx.hstack(
                    rx.link(
                        rx.button("Get Started Free →", style=button_primary, font_size="16px", padding="14px 32px"),
                        href="/register",
                    ),
                    rx.link(
                        rx.button("Sign In", background="transparent", color=TEXT_MUTED,
                                  border=f"1px solid #2D2D44", border_radius="10px",
                                  padding="14px 28px", cursor="pointer", font_size="16px",
                                  _hover={"color": TEXT_PRIMARY}),
                        href="/login",
                    ),
                    spacing="4",
                ),
                # Feature pills
                rx.hstack(
                    *[
                        rx.box(
                            rx.text(label, font_size="13px", color=TEXT_MUTED),
                            background="#1A1A2E",
                            border=f"1px solid #2D2D44",
                            border_radius="99px",
                            padding="8px 16px",
                        )
                        for label in ["⚡ XP & Levels", "🏅 Achievement Badges",
                                      "🔥 Streaks", "🤖 AI Coach", "📈 Progress Charts"]
                    ],
                    wrap="wrap",
                    justify="center",
                    spacing="2",
                ),
                spacing="6",
                align="center",
                max_width="700px",
                padding="80px 24px",
            ),
        ),
        min_height="100vh",
        background=BACKGROUND,
    )
