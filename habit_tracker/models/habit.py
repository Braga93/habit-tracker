from datetime import datetime
from typing import Optional, List
import sqlmodel
from sqlmodel import Field, Relationship


class Habit(sqlmodel.SQLModel, table=True):
    """A habit defined using the Cue → Routine → Reward loop."""

    __tablename__ = "habits"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)

    # Habit-loop fields
    name: str = Field(max_length=120)
    cue: str = Field(max_length=255)          # Trigger / context
    routine: str = Field(max_length=255)      # The action to perform
    reward: str = Field(max_length=255)       # The reinforcement
    description: Optional[str] = None

    # Scheduling
    frequency: str = Field(default="daily")   # daily | weekly | custom
    target_days: Optional[str] = None         # JSON list of weekday ints for weekly/custom

    # Gamification
    xp_reward: int = Field(default=20)        # XP per completion
    icon: str = Field(default="🎯")
    color: str = Field(default="#7C3AED")

    # Status
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: Optional["User"] = Relationship(back_populates="habits")
    logs: List["HabitLog"] = Relationship(back_populates="habit")
