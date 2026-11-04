"""
Habit State — reactive state for habits + logging + analytics.
"""

from datetime import date
from typing import List, Dict, Any
import reflex as rx
from sqlmodel import select

from habit_tracker.models.habit import Habit
from habit_tracker.models.log import HabitLog
from habit_tracker.services.habit_service import HabitService
from habit_tracker.services.gamification_service import GamificationService
from habit_tracker.state.gamification_state import GamificationState


class HabitState(GamificationState):
    """Owns all habit data visible in the UI."""

    habits: List[Dict[str, Any]] = []
    completed_today: List[int] = []
    heatmap: Dict[str, int] = {}
    streaks: Dict[str, int] = {}          # habit_id(str) → streak int
    completion_rates: Dict[str, float] = {}  # habit_id(str) → rate float

    # New habit form
    new_name: str = ""
    new_cue: str = ""
    new_routine: str = ""
    new_reward: str = ""
    new_icon: str = "🎯"
    new_color: str = "#7C3AED"
    new_xp: int = 20
    habit_error: str = ""

    # Newly earned badges (used to trigger toast)
    new_badges: List[Dict[str, Any]] = []

    def set_new_name(self, v: str): self.new_name = v
    def set_new_cue(self, v: str): self.new_cue = v
    def set_new_routine(self, v: str): self.new_routine = v
    def set_new_reward(self, v: str): self.new_reward = v
    def set_new_icon(self, v: str): self.new_icon = v
    def set_new_color(self, v: str): self.new_color = v
    def set_new_xp(self, v: str): self.new_xp = int(v)

    def load_habits(self):
        if not self.is_authenticated:
            return
        with rx.session() as session:
            habits = HabitService.get_user_habits(session, self.user_id)
            self.habits = [
                {
                    "id": h.id,
                    "name": h.name,
                    "cue": h.cue,
                    "routine": h.routine,
                    "reward": h.reward,
                    "icon": h.icon,
                    "color": h.color,
                    "xp_reward": h.xp_reward,
                    "frequency": h.frequency,
                }
                for h in habits
            ]
            self.completed_today = HabitService.habits_completed_today(session, self.user_id)
            self.heatmap = HabitService.get_weekly_heatmap(session, self.user_id)

            self.streaks = {}
            self.completion_rates = {}
            for h in habits:
                self.streaks[str(h.id)] = HabitService.get_streak(session, self.user_id, h.id)
                self.completion_rates[str(h.id)] = HabitService.get_completion_rate(
                    session, self.user_id, h.id
                )

    def add_habit(self):
        if not self.new_name or not self.new_cue or not self.new_routine or not self.new_reward:
            self.habit_error = "All habit loop fields are required."
            return
        with rx.session() as session:
            HabitService.create_habit(
                session,
                user_id=self.user_id,
                name=self.new_name,
                cue=self.new_cue,
                routine=self.new_routine,
                reward=self.new_reward,
                xp_reward=self.new_xp,
                icon=self.new_icon,
                color=self.new_color,
            )
        self.new_name = ""
        self.new_cue = ""
        self.new_routine = ""
        self.new_reward = ""
        self.habit_error = ""

        # Evaluate first-habit badge
        with rx.session() as session:
            earned = GamificationService.evaluate_badges(session, self.user_id)
            self.new_badges = [{"name": b.name, "icon": b.icon} for b in earned]
        self.load_habits()

    def complete_habit(self, habit_id: int):
        with rx.session() as session:
            log = HabitService.log_completion(
                session, user_id=self.user_id, habit_id=habit_id
            )
            if log:
                # Award XP
                habit = session.get(Habit, habit_id)
                GamificationService.award_xp(
                    session, self.user_id, habit.xp_reward, f"Completed: {habit.name}"
                )
                # Update streak + check streak bonus
                streak = GamificationService.update_global_streak(session, self.user_id)
                bonus = GamificationService.streak_bonus(streak)
                if bonus:
                    GamificationService.award_xp(session, self.user_id, bonus, f"Streak milestone: {streak} days")
                # Evaluate badges
                earned = GamificationService.evaluate_badges(session, self.user_id)
                self.new_badges = [{"name": b.name, "icon": b.icon} for b in earned]
        self.load_habits()

    def delete_habit(self, habit_id: int):
        with rx.session() as session:
            HabitService.delete_habit(session, habit_id, self.user_id)
        self.load_habits()
