"""AI Coach chat interface component."""

import reflex as rx
from habit_tracker.styles.theme import (
    SURFACE, SURFACE2, BORDER, TEXT_PRIMARY, TEXT_MUTED, ACCENT, ACCENT_GLOW,
    input_style, button_primary,
)
from habit_tracker.state.ai_state import AIState


def _message_bubble(msg: dict) -> rx.Component:
    is_user = msg["role"] == "user"
    return rx.box(
        rx.text(msg["content"], font_size="14px", color=TEXT_PRIMARY, white_space="pre-wrap"),
        background=rx.cond(is_user, f"{ACCENT}33", SURFACE2),
        border=rx.cond(is_user, f"1px solid {ACCENT}55", f"1px solid {BORDER}"),
        border_radius=rx.cond(is_user, "18px 18px 4px 18px", "18px 18px 18px 4px"),
        padding="12px 16px",
        max_width="75%",
        align_self=rx.cond(is_user, "flex-end", "flex-start"),
    )


def chat_interface() -> rx.Component:
    """Full AI coach chat panel with message history, input, and typing indicator."""
    return rx.box(
        # Chat header
        rx.hstack(
            rx.text("🤖", font_size="20px"),
            rx.vstack(
                rx.text("Behavioral Coach", font_size="15px", font_weight="700", color=TEXT_PRIMARY),
                rx.text("AI-powered habit advisor", font_size="12px", color=TEXT_MUTED),
                spacing="0",
                align_items="start",
            ),
            rx.spacer(),
            rx.button(
                "Clear",
                on_click=AIState.clear_chat,
                background="transparent",
                color=TEXT_MUTED,
                border=f"1px solid {BORDER}",
                border_radius="8px",
                padding="4px 12px",
                font_size="12px",
                cursor="pointer",
                _hover={"color": TEXT_PRIMARY},
            ),
            width="100%",
            align="center",
            padding_bottom="12px",
            border_bottom=f"1px solid {BORDER}",
        ),
        # Message list
        rx.box(
            rx.cond(
                AIState.chat_history.length() == 0,
                rx.vstack(
                    rx.text("👋", font_size="32px"),
                    rx.text(
                        "Hi! I'm your Behavioral Coach. Ask me anything about building better habits, "
                        "overcoming obstacles, or understanding your progress.",
                        font_size="14px",
                        color=TEXT_MUTED,
                        text_align="center",
                        max_width="300px",
                    ),
                    align="center",
                    justify="center",
                    height="100%",
                ),
                rx.vstack(
                    rx.foreach(AIState.chat_history, _message_bubble),
                    # Typing indicator
                    rx.cond(
                        AIState.ai_is_typing,
                        rx.box(
                            rx.text("● ● ●", color=ACCENT, font_size="18px", letter_spacing="4px"),
                            align_self="flex-start",
                            padding="8px 14px",
                        ),
                        rx.fragment(),
                    ),
                    spacing="2",
                    width="100%",
                    align_items="stretch",
                ),
            ),
            flex="1",
            overflow_y="auto",
            padding="12px 0",
            min_height="320px",
            max_height="480px",
        ),
        # Input row
        rx.hstack(
            rx.input(
                placeholder="Ask your coach...",
                value=AIState.current_input,
                on_change=AIState.set_current_input,
                on_key_down=lambda e: rx.cond(
                    e == "Enter",
                    AIState.send_message(),
                    rx.noop(),
                ),
                style=input_style,
                flex="1",
            ),
            rx.button(
                "Send →",
                on_click=AIState.send_message,
                is_loading=AIState.ai_is_typing,
                style=button_primary,
                min_width="80px",
            ),
            width="100%",
            spacing="2",
            padding_top="12px",
            border_top=f"1px solid {BORDER}",
        ),
        display="flex",
        flex_direction="column",
        gap="0",
        padding="20px",
        background=SURFACE,
        border=f"1px solid {BORDER}",
        border_radius="16px",
        height="100%",
        min_height="500px",
    )
