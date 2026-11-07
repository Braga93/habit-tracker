from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date, timedelta

ALL_WEEKDAYS = (0, 1, 2, 3, 4, 5, 6)
MAX_LOOKBACK_DAYS = 3660


def parse_weekdays(raw: str) -> tuple[int, ...]:
    days = sorted({int(part) for part in raw.split(",") if part.strip() != ""})
    return tuple(day for day in days if 0 <= day <= 6) or ALL_WEEKDAYS


def format_weekdays(days: Iterable[int]) -> str:
    unique = sorted({day for day in days if 0 <= day <= 6})
    return ",".join(str(day) for day in (unique or ALL_WEEKDAYS))


def is_scheduled(weekdays: Iterable[int], day: date) -> bool:
    return day.weekday() in set(weekdays)


def habit_streak(done: set[date], weekdays: Iterable[int], today: date, created_on: date) -> int:
    weekdays = set(weekdays)
    cursor = today
    if is_scheduled(weekdays, cursor) and cursor not in done:
        cursor -= timedelta(days=1)
    streak = 0
    for _ in range(MAX_LOOKBACK_DAYS):
        if cursor < created_on:
            break
        if is_scheduled(weekdays, cursor):
            if cursor not in done:
                break
            streak += 1
        cursor -= timedelta(days=1)
    return streak


def global_streak(active_days: set[date], today: date) -> int:
    cursor = today if today in active_days else today - timedelta(days=1)
    streak = 0
    while cursor in active_days:
        streak += 1
        cursor -= timedelta(days=1)
    return streak


@dataclass(frozen=True)
class Completion:
    completed: int
    scheduled: int

    @property
    def rate(self) -> float:
        return round(self.completed / self.scheduled, 3) if self.scheduled else 0.0


def completion(
    done: set[date], weekdays: Iterable[int], today: date, created_on: date, window_days: int = 30
) -> Completion:
    weekdays = set(weekdays)
    start = max(created_on, today - timedelta(days=window_days - 1))
    scheduled = 0
    completed = 0
    cursor = start
    while cursor <= today:
        counts = is_scheduled(weekdays, cursor) and (cursor != today or cursor in done)
        if counts:
            scheduled += 1
            completed += cursor in done
        cursor += timedelta(days=1)
    return Completion(completed=completed, scheduled=scheduled)


def completion_rate(
    done: set[date], weekdays: Iterable[int], today: date, created_on: date, window_days: int = 30
) -> float:
    return completion(done, weekdays, today, created_on, window_days).rate
