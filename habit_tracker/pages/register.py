"""Register page."""

import reflex as rx
from habit_tracker.styles.theme import (
    BACKGROUND, TEXT_PRIMARY, TEXT_MUTED, DANGER,
    input_style, button_primary, card_style
)
from habit_tracker.state.auth_state import AuthState


def register_page() -> rx.Component:
    return rx.center(
        rx.box(
            rx.vstack(
                rx.text("⚡ HabitAI", font_size="22px", font_weight="800",
                        background="linear-gradient(90deg, #7C3AED, #FBBF24)",
                        background_clip="text", color="transparent"),
                rx.heading("Create your account", font_size="24px", font_weight="700", color=TEXT_PRIMARY),
                rx.text("Start your habit journey today", font_size="14px", color=TEXT_MUTED),

                # Error
                rx.cond(
                    AuthState.auth_error != "",
                    rx.box(
                        rx.text(AuthState.auth_error, color=DANGER, font_size="13px"),
                        background=f"{DANGER}18",
                        border=f"1px solid {DANGER}44",
                        border_radius="8px",
                        padding="10px 14px",
                        width="100%",
                    ),
                    rx.fragment(),
                ),

                # Form
                rx.vstack(
                    rx.text("Username", font_size="13px", font_weight="600", color=TEXT_MUTED),
                    rx.input(
                        placeholder="choose_username",
                        on_change=AuthState.set_form_username,
                        style=input_style,
                    ),
                    rx.text("Email", font_size="13px", font_weight="600", color=TEXT_MUTED),
                    rx.input(
                        placeholder="you@example.com",
                        type="email",
                        on_change=AuthState.set_form_email,
                        style=input_style,
                    ),
                    rx.text("Password", font_size="13px", font_weight="600", color=TEXT_MUTED),
                    rx.input(
                        placeholder="••••••••",
                        type="password",
                        on_change=AuthState.set_form_password,
                        style=input_style,
                    ),
                    spacing="2",
                    width="100%",
                ),

                rx.button("Create Account", on_click=AuthState.register,
                          style=button_primary, width="100%", font_size="15px"),
                rx.hstack(
                    rx.text("Already have an account?", font_size="13px", color=TEXT_MUTED),
                    rx.link("Sign in", href="/login", font_size="13px", color="#A855F7", font_weight="600"),
                    spacing="1",
                ),
                spacing="4",
                width="100%",
                align="stretch",
            ),
            style={**card_style, "width": "100%", "max_width": "420px"},
        ),
        min_height="100vh",
        background=BACKGROUND,
        padding="24px",
    )
