from datetime import datetime
from typing import Optional, List
import sqlmodel
from sqlmodel import Field, Relationship


class Badge(sqlmodel.SQLModel, table=True):
    """A badge definition that can be unlocked by users."""

    __tablename__ = "badges"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=80, unique=True)
    description: str = Field(max_length=255)
    icon: str = Field(default="🏅")
    condition_type: str  # streak | total_completions | level | first_habit
    condition_value: int = Field(default=1)
    xp_bonus: int = Field(default=50)

    user_badges: List["UserBadge"] = Relationship(back_populates="badge")


class UserBadge(sqlmodel.SQLModel, table=True):
    """Junction: which badges a user has earned."""

    __tablename__ = "user_badges"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    badge_id: int = Field(foreign_key="badges.id", index=True)
    earned_at: datetime = Field(default_factory=datetime.utcnow)

    user: Optional["User"] = Relationship(back_populates="user_badges")
    badge: Optional["Badge"] = Relationship(back_populates="user_badges")


class XPEvent(sqlmodel.SQLModel, table=True):
    """Audit log for every XP gain event."""

    __tablename__ = "xp_events"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    amount: int
    reason: str = Field(max_length=120)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    user: Optional["User"] = Relationship(back_populates="xp_events")


# ── Seed badges ──────────────────────────────────────────────────────────────
SEED_BADGES = [
    Badge(name="First Step",       description="Complete your first habit",       icon="👣", condition_type="total_completions", condition_value=1,   xp_bonus=25),
    Badge(name="3-Day Streak",     description="Maintain a 3-day streak",         icon="🔥", condition_type="streak",            condition_value=3,   xp_bonus=50),
    Badge(name="7-Day Streak",     description="Maintain a 7-day streak",         icon="⚡", condition_type="streak",            condition_value=7,   xp_bonus=100),
    Badge(name="30-Day Streak",    description="Maintain a 30-day streak",        icon="🌟", condition_type="streak",            condition_value=30,  xp_bonus=300),
    Badge(name="Century Club",     description="Complete 100 habit check-ins",    icon="💯", condition_type="total_completions", condition_value=100, xp_bonus=200),
    Badge(name="Level 5",          description="Reach level 5",                   icon="🎮", condition_type="level",             condition_value=5,   xp_bonus=150),
    Badge(name="Habit Master",     description="Complete 500 habit check-ins",    icon="🏆", condition_type="total_completions", condition_value=500, xp_bonus=500),
]
