"""
Gamification Service
Handles XP, leveling, streak bonuses, and badge unlocking.
"""

from datetime import date, timedelta
from typing import List, Optional, Tuple
from sqlmodel import Session, select

from habit_tracker.models.user import User, level_from_xp, xp_progress_pct
from habit_tracker.models.gamification import Badge, UserBadge, XPEvent, SEED_BADGES
from habit_tracker.models.log import HabitLog


class GamificationService:
    """Award XP, manage levels, evaluate and unlock badges."""

    # ── XP ────────────────────────────────────────────────────────────────────

    @staticmethod
    def award_xp(session: Session, user_id: int, amount: int, reason: str) -> User:
        user = session.get(User, user_id)
        if not user:
            raise ValueError(f"User {user_id} not found")

        user.total_xp += amount
        user.level = level_from_xp(user.total_xp)

        event = XPEvent(user_id=user_id, amount=amount, reason=reason)
        session.add(event)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    @staticmethod
    def get_xp_progress(user: User) -> Tuple[int, float]:
        """Returns (level, progress_pct 0-100)."""
        return user.level, xp_progress_pct(user.total_xp)

    # ── STREAKS ───────────────────────────────────────────────────────────────

    @staticmethod
    def update_global_streak(session: Session, user_id: int) -> int:
        """
        Recalculate the user's global streak (days where at least one habit was completed)
        and save it to the User record.
        """
        user = session.get(User, user_id)
        if not user:
            return 0

        logs = session.exec(
            select(HabitLog)
            .where(HabitLog.user_id == user_id, HabitLog.completed == True)
            .order_by(HabitLog.log_date.desc())
        ).all()

        active_dates = {log.log_date for log in logs}
        streak = 0
        check = date.today()
        while check.isoformat() in active_dates:
            streak += 1
            check -= timedelta(days=1)

        user.streak_days = streak
        user.last_active_date = date.today().isoformat()
        session.add(user)
        session.commit()
        return streak

    # ── STREAK BONUS XP ───────────────────────────────────────────────────────

    STREAK_BONUSES = {7: 50, 14: 75, 30: 150, 60: 300, 100: 500}

    @classmethod
    def streak_bonus(cls, streak: int) -> int:
        """Return any bonus XP for hitting a streak milestone."""
        bonus = 0
        for milestone, xp in cls.STREAK_BONUSES.items():
            if streak == milestone:
                bonus += xp
        return bonus

    # ── BADGES ────────────────────────────────────────────────────────────────

    @staticmethod
    def seed_badges(session: Session) -> None:
        """Insert default badges if they don't exist yet."""
        for badge in SEED_BADGES:
            existing = session.exec(select(Badge).where(Badge.name == badge.name)).first()
            if not existing:
                session.add(badge)
        session.commit()

    @staticmethod
    def get_all_badges(session: Session) -> List[Badge]:
        return session.exec(select(Badge)).all()

    @staticmethod
    def get_earned_badge_ids(session: Session, user_id: int) -> List[int]:
        rows = session.exec(select(UserBadge).where(UserBadge.user_id == user_id)).all()
        return [r.badge_id for r in rows]

    @classmethod
    def evaluate_badges(
        cls, session: Session, user_id: int
    ) -> List[Badge]:
        """
        Check all badge conditions for a user and unlock any new ones.
        Returns list of newly unlocked badges.
        """
        user = session.get(User, user_id)
        if not user:
            return []

        earned_ids = cls.get_earned_badge_ids(session, user_id)
        all_badges = cls.get_all_badges(session)
        newly_earned: List[Badge] = []

        total_completions = session.exec(
            select(HabitLog).where(HabitLog.user_id == user_id, HabitLog.completed == True)
        ).all()
        total_count = len(total_completions)

        for badge in all_badges:
            if badge.id in earned_ids:
                continue

            unlocked = False
            if badge.condition_type == "streak" and user.streak_days >= badge.condition_value:
                unlocked = True
            elif badge.condition_type == "total_completions" and total_count >= badge.condition_value:
                unlocked = True
            elif badge.condition_type == "level" and user.level >= badge.condition_value:
                unlocked = True

            if unlocked:
                user_badge = UserBadge(user_id=user_id, badge_id=badge.id)
                session.add(user_badge)
                # Award bonus XP for the badge
                cls.award_xp(session, user_id, badge.xp_bonus, f"Badge unlocked: {badge.name}")
                newly_earned.append(badge)

        session.commit()
        return newly_earned
