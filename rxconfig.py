import reflex as rx

config = rx.Config(
    app_name="habit_tracker",
    db_url="sqlite:///habit_tracker.db",
    env=rx.Env.DEV,
)
