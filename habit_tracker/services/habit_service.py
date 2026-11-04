"""
Habit Loop Engine Service
Implements Cue → Routine → Reward cycle logic.
"""

from datetime import date, datetime, timedelta
from typing import List, Optional, Dict
import json
import reflex as rx
from sqlmodel import Session, select

from habit_tracker.models.habit import Habit
from habit_tracker.models.log import HabitLog
from habit_tracker.models.user import User


class HabitService:
    """Core habit loop engine: creation, logging, streak calculation."""

    # ── CRUD ──────────────────────────────────────────────────────────────────

    @staticmethod
    def create_habit(
        session: Session,
        user_id: int,
        name: str,
        cue: str,
        routine: str,
        reward: str,
        description: str = "",
        frequency: str = "daily",
        target_days: Optional[List[int]] = None,
        xp_reward: int = 20,
        icon: str = "🎯",
        color: str = "#7C3AED",
    ) -> Habit:
        habit = Habit(
            user_id=user_id,
            name=name,
            cue=cue,
            routine=routine,
            reward=reward,
            description=description,
            frequency=frequency,
            target_days=json.dumps(target_days) if target_days else None,
            xp_reward=xp_reward,
            icon=icon,
            color=color,
        )
        session.add(habit)
        session.commit()
        session.refresh(habit)
        return habit

    @staticmethod
    def get_user_habits(session: Session, user_id: int) -> List[Habit]:
        statement = select(Habit).where(Habit.user_id == user_id, Habit.is_active == True)
        return session.exec(statement).all()

    @staticmethod
    def delete_habit(session: Session, habit_id: int, user_id: int) -> bool:
        habit = session.get(Habit, habit_id)
        if habit and habit.user_id == user_id:
            habit.is_active = False
            session.add(habit)
            session.commit()
            return True
        return False

    # ── LOGGING ───────────────────────────────────────────────────────────────

    @staticmethod
    def log_completion(
        session: Session,
        user_id: int,
        habit_id: int,
        log_date: Optional[str] = None,
        notes: str = "",
        mood: int = 3,
    ) -> Optional[HabitLog]:
        """Record a habit completion; returns None if already logged today."""
        if log_date is None:
            log_date = date.today().isoformat()

        # Prevent duplicate logs for the same day
        existing = session.exec(
            select(HabitLog).where(
                HabitLog.user_id == user_id,
                HabitLog.habit_id == habit_id,
                HabitLog.log_date == log_date,
            )
        ).first()
        if existing:
            return None

        habit = session.get(Habit, habit_id)
        if not habit or habit.user_id != user_id:
            return None

        log = HabitLog(
            user_id=user_id,
            habit_id=habit_id,
            log_date=log_date,
            completed=True,
            notes=notes,
            mood=mood,
            xp_earned=habit.xp_reward,
        )
        session.add(log)
        session.commit()
        session.refresh(log)
        return log

    # ── ANALYTICS ─────────────────────────────────────────────────────────────

    @staticmethod
    def get_streak(session: Session, user_id: int, habit_id: int) -> int:
        """Calculate current streak (consecutive completed days) for a habit."""
        logs = session.exec(
            select(HabitLog)
            .where(HabitLog.user_id == user_id, HabitLog.habit_id == habit_id, HabitLog.completed == True)
            .order_by(HabitLog.log_date.desc())
        ).all()

        if not logs:
            return 0

        streak = 0
        check_date = date.today()
        log_dates = {log.log_date for log in logs}

        while check_date.isoformat() in log_dates:
            streak += 1
            check_date -= timedelta(days=1)

        return streak

    @staticmethod
    def get_completion_rate(
        session: Session, user_id: int, habit_id: int, days: int = 30
    ) -> float:
        """Completion rate over the last N days (0.0–1.0)."""
        start_date = (date.today() - timedelta(days=days)).isoformat()
        logs = session.exec(
            select(HabitLog).where(
                HabitLog.user_id == user_id,
                HabitLog.habit_id == habit_id,
                HabitLog.log_date >= start_date,
                HabitLog.completed == True,
            )
        ).all()
        return len(logs) / days

    @staticmethod
    def get_weekly_heatmap(session: Session, user_id: int) -> Dict[str, int]:
        """Returns a dict of {iso_date: completion_count} for the last 84 days."""
        start_date = (date.today() - timedelta(days=84)).isoformat()
        logs = session.exec(
            select(HabitLog).where(
                HabitLog.user_id == user_id,
                HabitLog.log_date >= start_date,
                HabitLog.completed == True,
            )
        ).all()
        heatmap: Dict[str, int] = {}
        for log in logs:
            heatmap[log.log_date] = heatmap.get(log.log_date, 0) + 1
        return heatmap

    @staticmethod
    def habits_completed_today(session: Session, user_id: int) -> List[int]:
        """Returns list of habit_ids completed today."""
        today = date.today().isoformat()
        logs = session.exec(
            select(HabitLog).where(
                HabitLog.user_id == user_id,
                HabitLog.log_date == today,
                HabitLog.completed == True,
            )
        ).all()
        return [log.habit_id for log in logs]
