from datetime import UTC, date, datetime

from sqlmodel import Field, SQLModel, UniqueConstraint


def utcnow() -> datetime:
    return datetime.now(UTC)


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, max_length=30)
    email: str = Field(index=True, unique=True, max_length=255)
    password_hash: str
    total_xp: int = Field(default=0)
    created_at: datetime = Field(default_factory=utcnow)


class Habit(SQLModel, table=True):
    __tablename__ = "habits"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    name: str = Field(max_length=80)
    cue: str = Field(max_length=200)
    routine: str = Field(max_length=200)
    reward: str = Field(max_length=200)
    icon: str = Field(default="🎯", max_length=8)
    difficulty: str = Field(default="medium", max_length=10)
    weekdays: str = Field(default="0,1,2,3,4,5,6", max_length=20)
    archived: bool = Field(default=False)
    created_on: date = Field(default_factory=date.today)


class CheckIn(SQLModel, table=True):
    __tablename__ = "checkins"
    __table_args__ = (UniqueConstraint("habit_id", "day"),)

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    habit_id: int = Field(foreign_key="habits.id", index=True)
    day: date = Field(index=True)
    mood: int | None = Field(default=None, ge=1, le=5)
    note: str | None = Field(default=None, max_length=280)
    xp_earned: int = Field(default=0)
    created_at: datetime = Field(default_factory=utcnow)


class UserBadge(SQLModel, table=True):
    __tablename__ = "user_badges"
    __table_args__ = (UniqueConstraint("user_id", "code"),)

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    code: str = Field(max_length=40)
    earned_at: datetime = Field(default_factory=utcnow)


class XPEvent(SQLModel, table=True):
    __tablename__ = "xp_events"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    amount: int
    reason: str = Field(max_length=120)
    created_at: datetime = Field(default_factory=utcnow)
