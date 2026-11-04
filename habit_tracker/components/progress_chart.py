"""Progress heatmap chart component (12-week calendar heatmap)."""

import reflex as rx
from datetime import date, timedelta
from habit_tracker.styles.theme import SURFACE, BORDER, TEXT_MUTED, ACCENT
from habit_tracker.state.habit_state import HabitState


def _day_cell(day_offset: int) -> rx.Component:
    """Renders a single day cell in the heatmap grid."""
    d = (date.today() - timedelta(days=83 - day_offset)).isoformat()
    count = HabitState.heatmap[d]

    color = rx.cond(
        count == 0, "#1E1E3A",
        rx.cond(
            count == 1, "#4C1D95",
            rx.cond(
                count <= 3, "#7C3AED",
                "#A855F7",
            ),
        ),
    )

    return rx.box(
        width="14px",
        height="14px",
        background=color,
        border_radius="3px",
        title=count.to_string() + f" completions on {d}",
        cursor="default",
    )


def heatmap_chart() -> rx.Component:
    """
    84-day (12-week) contribution-style heatmap.
    Rows = days of week (Mon-Sun), columns = weeks.
    """
    weeks = []
    for week in range(12):
        cols = []
        for day in range(7):
            offset = week * 7 + day
            cols.append(_day_cell(offset))
        weeks.append(rx.vstack(*cols, spacing="1"))

    return rx.box(
        rx.text("Activity Heatmap", font_size="15px", font_weight="700", color="white", margin_bottom="12px"),
        rx.hstack(*weeks, spacing="1"),
        rx.hstack(
            rx.text("12 weeks ago", font_size="10px", color=TEXT_MUTED),
            rx.spacer(),
            rx.text("Today", font_size="10px", color=TEXT_MUTED),
            width="100%",
            margin_top="6px",
        ),
        padding="20px",
        background=SURFACE,
        border=f"1px solid {BORDER}",
        border_radius="16px",
        overflow_x="auto",
    )
