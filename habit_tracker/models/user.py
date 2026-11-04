from datetime import datetime
from typing import Optional, List
import sqlmodel
from sqlmodel import Field, Relationship


class User(sqlmodel.SQLModel, table=True):
    """Represents an application user."""

    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, max_length=50)
    email: str = Field(unique=True, max_length=255)
    hashed_password: str
    avatar_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Gamification
    total_xp: int = Field(default=0)
    level: int = Field(default=1)
    streak_days: int = Field(default=0)
    last_active_date: Optional[str] = None  # ISO date string

    # Relationships
    habits: List["Habit"] = Relationship(back_populates="user")
    logs: List["HabitLog"] = Relationship(back_populates="user")
    user_badges: List["UserBadge"] = Relationship(back_populates="user")
    xp_events: List["XPEvent"] = Relationship(back_populates="user")


def xp_for_level(level: int) -> int:
    """XP required to reach a given level (quadratic scaling)."""
    return 100 * (level ** 2)


def level_from_xp(total_xp: int) -> int:
    level = 1
    while xp_for_level(level + 1) <= total_xp:
        level += 1
    return level


def xp_progress_pct(total_xp: int) -> float:
    """0-100 progress percentage toward the next level."""
    current_level = level_from_xp(total_xp)
    xp_current_floor = xp_for_level(current_level)
    xp_next = xp_for_level(current_level + 1)
    return min(100.0, (total_xp - xp_current_floor) / (xp_next - xp_current_floor) * 100)
