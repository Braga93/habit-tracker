"""
AI Coach State — manages chat history, streaming, and pattern-analysis panel.
"""

from typing import List, Dict, Any
import reflex as rx

from habit_tracker.services import ai_service
from habit_tracker.services.habit_service import HabitService
from habit_tracker.state.habit_state import HabitState


class AIState(HabitState):
    """Owns the AI chat thread and coach-insight panel."""

    chat_history: List[Dict[str, str]] = []  # {"role": "user"|"assistant", "content": ...}
    current_input: str = ""
    ai_is_typing: bool = False
    coach_insights: str = ""
    dropout_risks: List[str] = []
    insights_loading: bool = False

    def set_current_input(self, val: str):
        self.current_input = val

    async def send_message(self):
        if not self.current_input.strip() or not self.is_authenticated:
            return

        user_msg = self.current_input.strip()
        self.current_input = ""
        self.chat_history = [*self.chat_history, {"role": "user", "content": user_msg}]
        self.ai_is_typing = True
        yield  # flush UI

        # Build habit context for the LLM
        with rx.session() as session:
            habits_raw = HabitService.get_user_habits(session, self.user_id)
            context = ai_service.build_habit_context(
                habits=habits_raw,
                streaks={
                    h.name: HabitService.get_streak(session, self.user_id, h.id)
                    for h in habits_raw
                },
                completion_rates={
                    h.name: HabitService.get_completion_rate(session, self.user_id, h.id)
                    for h in habits_raw
                },
                total_xp=self.total_xp,
                level=self.level,
                streak_days=self.streak_days,
            )

        # Strip any trailing partial assistant message before streaming
        history_for_llm = [m for m in self.chat_history if not (m["role"] == "assistant")]

        assistant_reply = ""
        async for token in ai_service.stream_coach_response(
            history=history_for_llm,
            user_message=user_msg,
            habit_context=context,
        ):
            assistant_reply += token
            # Replace or append streaming assistant placeholder
            if self.chat_history and self.chat_history[-1]["role"] == "assistant":
                self.chat_history = [
                    *self.chat_history[:-1],
                    {"role": "assistant", "content": assistant_reply},
                ]
            else:
                self.chat_history = [
                    *self.chat_history,
                    {"role": "assistant", "content": assistant_reply},
                ]
            yield

        self.ai_is_typing = False

    async def load_insights(self):
        if not self.is_authenticated:
            return
        self.insights_loading = True
        yield

        with rx.session() as session:
            habits_raw = HabitService.get_user_habits(session, self.user_id)
            rates_7d = {
                h.name: HabitService.get_completion_rate(session, self.user_id, h.id, days=7)
                for h in habits_raw
            }
            stats = {
                "habits": [h.name for h in habits_raw],
                "7d_completion_rates": rates_7d,
                "global_streak": self.streak_days,
                "level": self.level,
            }

        self.coach_insights = await ai_service.analyze_patterns(stats)
        self.dropout_risks = await ai_service.predict_dropout_risk(rates_7d)
        self.insights_loading = False

    def clear_chat(self):
        self.chat_history = []
