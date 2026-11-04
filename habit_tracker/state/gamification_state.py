"""
Gamification State — XP bar, level, badges panel.
"""

from typing import List, Dict, Any
import reflex as rx
from sqlmodel import select

from habit_tracker.models.user import User, xp_progress_pct, level_from_xp, xp_for_level
from habit_tracker.models.gamification import Badge, UserBadge
from habit_tracker.services.gamification_service import GamificationService
from habit_tracker.state.auth_state import AuthState


class GamificationState(AuthState):
    """Owns XP, level, progress, and badge display data."""

    total_xp: int = 0
    level: int = 1
    xp_progress_pct: float = 0.0
    xp_for_next_level: int = 100
    streak_days: int = 0

    earned_badges: List[Dict[str, Any]] = []
    all_badges: List[Dict[str, Any]] = []

    def load_gamification(self):
        if not self.is_authenticated:
            return
        with rx.session() as session:
            user = session.get(User, self.user_id)
            if not user:
                return
            self.total_xp = user.total_xp
            self.level = user.level
            self.xp_progress_pct = xp_progress_pct(user.total_xp)
            self.xp_for_next_level = xp_for_level(user.level + 1)
            self.streak_days = user.streak_days

            earned_ids = GamificationService.get_earned_badge_ids(session, self.user_id)
            all_badges = GamificationService.get_all_badges(session)

            self.all_badges = [
                {
                    "id": b.id,
                    "name": b.name,
                    "description": b.description,
                    "icon": b.icon,
                    "earned": b.id in earned_ids,
                }
                for b in all_badges
            ]
            self.earned_badges = [b for b in self.all_badges if b["earned"]]
