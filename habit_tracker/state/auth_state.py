"""
Auth State — registration, login, session management.
"""

import hashlib
import reflex as rx
from sqlmodel import select

from habit_tracker.models.user import User
from habit_tracker.services.gamification_service import GamificationService


def _hash_password(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()


class AuthState(rx.State):
    """Manages authentication and the active user session."""

    user_id: int = 0
    username: str = ""
    email: str = ""
    is_authenticated: bool = False
    auth_error: str = ""

    # Form fields
    form_username: str = ""
    form_email: str = ""
    form_password: str = ""

    def set_form_username(self, val: str):
        self.form_username = val

    def set_form_email(self, val: str):
        self.form_email = val

    def set_form_password(self, val: str):
        self.form_password = val

    def register(self):
        if not self.form_username or not self.form_email or not self.form_password:
            self.auth_error = "All fields are required."
            return

        with rx.session() as session:
            existing = session.exec(
                select(User).where(User.username == self.form_username)
            ).first()
            if existing:
                self.auth_error = "Username already taken."
                return

            existing_email = session.exec(
                select(User).where(User.email == self.form_email)
            ).first()
            if existing_email:
                self.auth_error = "An account with this email already exists."
                return

            user = User(
                username=self.form_username,
                email=self.form_email,
                hashed_password=_hash_password(self.form_password),
            )
            session.add(user)
            session.commit()
            session.refresh(user)

            # Seed badges on first user creation
            GamificationService.seed_badges(session)

            self.user_id = user.id
            self.username = user.username
            self.email = user.email
            self.is_authenticated = True
            self.auth_error = ""
        return rx.redirect("/dashboard")

    def login(self):
        if not self.form_username or not self.form_password:
            self.auth_error = "Username and password required."
            return

        with rx.session() as session:
            user = session.exec(
                select(User).where(User.username == self.form_username)
            ).first()
            if not user or user.hashed_password != _hash_password(self.form_password):
                self.auth_error = "Invalid credentials."
                return

            self.user_id = user.id
            self.username = user.username
            self.email = user.email
            self.is_authenticated = True
            self.auth_error = ""
        return rx.redirect("/dashboard")

    def logout(self):
        self.user_id = 0
        self.username = ""
        self.email = ""
        self.is_authenticated = False
        return rx.redirect("/")
