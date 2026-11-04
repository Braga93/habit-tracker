"""AI Coach page — chat interface + pattern analysis panel."""

import reflex as rx
from habit_tracker.styles.theme import (
    BACKGROUND, SURFACE, BORDER, TEXT_PRIMARY, TEXT_MUTED,
    DANGER, SUCCESS, ACCENT, card_style
)
from habit_tracker.components.navbar import navbar
from habit_tracker.components.chat import chat_interface
from habit_tracker.state.ai_state import AIState
from habit_tracker.state.gamification_state import GamificationState


def _insights_panel() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text("📊 Pattern Analysis", font_size="16px", font_weight="700", color=TEXT_PRIMARY),
                rx.spacer(),
                rx.button(
                    rx.cond(AIState.insights_loading, "Analyzing...", "Refresh"),
                    on_click=AIState.load_insights,
                    is_loading=AIState.insights_loading,
                    background="transparent",
                    color=ACCENT,
                    border=f"1px solid {ACCENT}",
                    border_radius="8px",
                    padding="4px 14px",
                    font_size="12px",
                    cursor="pointer",
                ),
                width="100%",
                align="center",
            ),
            # Dropout risk alert
            rx.cond(
                AIState.dropout_risks.length() > 0,
                rx.box(
                    rx.hstack(
                        rx.text("⚠️", font_size="16px"),
                        rx.vstack(
                            rx.text("At-Risk Habits", font_size="13px", font_weight="700", color=DANGER),
                            rx.foreach(
                                AIState.dropout_risks,
                                lambda name: rx.text("• ", name, font_size="12px", color=TEXT_MUTED),
                            ),
                            spacing="0",
                            align_items="start",
                        ),
                        spacing="2",
                        align="start",
                    ),
                    background=f"{DANGER}12",
                    border=f"1px solid {DANGER}44",
                    border_radius="10px",
                    padding="12px",
                    width="100%",
                ),
                rx.fragment(),
            ),
            # Insights text
            rx.cond(
                AIState.coach_insights != "",
                rx.box(
                    rx.text(AIState.coach_insights, font_size="13px", color=TEXT_MUTED,
                            white_space="pre-wrap", line_height="1.6"),
                    background=f"{ACCENT}0C",
                    border=f"1px solid {ACCENT}33",
                    border_radius="10px",
                    padding="14px",
                    width="100%",
                ),
                rx.box(
                    rx.text("Click Refresh to analyze your habit patterns with AI.",
                            font_size="13px", color=TEXT_MUTED, text_align="center"),
                    padding="20px",
                    width="100%",
                ),
            ),
            spacing="3",
            width="100%",
        ),
        style=card_style,
        width="100%",
    )


def coach_page() -> rx.Component:
    return rx.box(
        navbar(),
        rx.box(
            rx.heading("AI Behavioral Coach", font_size="28px", font_weight="800", color=TEXT_PRIMARY,
                       margin_bottom="4px"),
            rx.text(
                "Chat with your personal AI coach powered by LLM pattern analysis",
                font_size="14px", color=TEXT_MUTED, margin_bottom="24px",
            ),
            rx.grid(
                chat_interface(),
                rx.vstack(
                    _insights_panel(),
                    spacing="4",
                    width="100%",
                ),
                columns="2",
                spacing="4",
                width="100%",
                template_columns=["1fr", "1fr 380px"],
            ),
            padding="32px",
            max_width="1200px",
            margin="0 auto",
        ),
        background=BACKGROUND,
        min_height="100vh",
        on_mount=[AIState.load_habits, GamificationState.load_gamification],
    )
