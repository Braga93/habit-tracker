from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

Difficulty = Literal["easy", "medium", "hard"]


class RegisterIn(BaseModel):
    username: str = Field(min_length=3, max_length=30, pattern=r"^[a-zA-Z0-9_]+$")
    email: str = Field(max_length=255, pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    password: str = Field(min_length=8, max_length=128)

    @field_validator("email")
    @classmethod
    def lower_email(cls, value: str) -> str:
        return value.strip().lower()


class LoginIn(BaseModel):
    username: str = Field(min_length=1, max_length=255)
    password: str = Field(min_length=1, max_length=128)


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    created_at: datetime


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class HabitIn(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    cue: str = Field(min_length=1, max_length=200)
    routine: str = Field(min_length=1, max_length=200)
    reward: str = Field(min_length=1, max_length=200)
    icon: str = Field(default="🎯", min_length=1, max_length=8)
    difficulty: Difficulty = "medium"
    weekdays: list[int] = Field(default_factory=lambda: [0, 1, 2, 3, 4, 5, 6], min_length=1, max_length=7)

    @field_validator("weekdays")
    @classmethod
    def valid_weekdays(cls, value: list[int]) -> list[int]:
        if any(day < 0 or day > 6 for day in value):
            raise ValueError("Os dias da semana vão de 0 (segunda) a 6 (domingo).")
        return sorted(set(value))


class HabitUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=80)
    cue: str | None = Field(default=None, min_length=1, max_length=200)
    routine: str | None = Field(default=None, min_length=1, max_length=200)
    reward: str | None = Field(default=None, min_length=1, max_length=200)
    icon: str | None = Field(default=None, min_length=1, max_length=8)
    difficulty: Difficulty | None = None
    weekdays: list[int] | None = Field(default=None, min_length=1, max_length=7)

    @field_validator("weekdays")
    @classmethod
    def valid_weekdays(cls, value: list[int] | None) -> list[int] | None:
        if value is None:
            return value
        if any(day < 0 or day > 6 for day in value):
            raise ValueError("Os dias da semana vão de 0 (segunda) a 6 (domingo).")
        return sorted(set(value))


class HabitOut(BaseModel):
    id: int
    name: str
    cue: str
    routine: str
    reward: str
    icon: str
    difficulty: Difficulty
    xp: int
    weekdays: list[int]
    created_on: date
    streak: int
    completion_rate: float
    total_checkins: int
    scheduled_today: bool
    done_today: bool


class LevelOut(BaseModel):
    level: int
    total_xp: int
    current: int
    needed: int
    percent: float


class BadgeOut(BaseModel):
    code: str
    name: str
    description: str
    icon: str
    xp_bonus: int
    earned: bool = False
    earned_at: datetime | None = None


class HabitCreated(BaseModel):
    habit: HabitOut
    new_badges: list[BadgeOut]


class CheckInIn(BaseModel):
    mood: int | None = Field(default=None, ge=1, le=5)
    note: str | None = Field(default=None, max_length=280)


class CheckInResult(BaseModel):
    habit: HabitOut
    xp_gained: int
    streak_bonus: int
    streak: int
    new_badges: list[BadgeOut]
    level: LevelOut
    leveled_up: bool


class HeatmapDay(BaseModel):
    day: date
    count: int


class XPEventOut(BaseModel):
    amount: int
    reason: str
    created_at: datetime


class TodayOut(BaseModel):
    done: int
    scheduled: int


class ProgressOut(BaseModel):
    user: UserOut
    level: LevelOut
    streak: int
    total_checkins: int
    today: TodayOut
    heatmap: list[HeatmapDay]
    badges: list[BadgeOut]
    recent_xp: list[XPEventOut]


class InsightOut(BaseModel):
    kind: str
    title: str
    message: str


class InsightsOut(BaseModel):
    insights: list[InsightOut]
    ai_enabled: bool


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=2000)


class ChatIn(BaseModel):
    message: str = Field(min_length=1, max_length=500)
    history: list[ChatMessage] = Field(default_factory=list, max_length=20)


class ChatOut(BaseModel):
    reply: str
    source: Literal["ia", "regras"]
    notice: str | None = None
