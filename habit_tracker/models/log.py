from datetime import datetime, date
from typing import Optional
import sqlmodel
from sqlmodel import Field, Relationship


class HabitLog(sqlmodel.SQLModel, table=True):
    """Records each time a user completes (or skips) a habit."""

    __tablename__ = "habit_logs"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    habit_id: int = Field(foreign_key="habits.id", index=True)

    log_date: str = Field(index=True)          # ISO date: YYYY-MM-DD
    completed: bool = Field(default=True)
    notes: Optional[str] = None
    mood: Optional[int] = None                  # 1–5 emoji rating
    xp_earned: int = Field(default=0)
    logged_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: Optional["User"] = Relationship(back_populates="logs")
    habit: Optional["Habit"] = Relationship(back_populates="logs")
