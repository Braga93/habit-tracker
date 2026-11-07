from datetime import date, timedelta

from app.domain.schedule import (
    ALL_WEEKDAYS,
    completion,
    completion_rate,
    format_weekdays,
    global_streak,
    habit_streak,
    parse_weekdays,
)

MONDAY = date(2026, 3, 2)


def days_back(start: date, count: int) -> set[date]:
    return {start - timedelta(days=offset) for offset in range(count)}


def test_weekdays_round_trip() -> None:
    assert parse_weekdays(format_weekdays([4, 0, 0, 2])) == (0, 2, 4)
    assert parse_weekdays("") == ALL_WEEKDAYS


def test_streak_keeps_yesterday_when_today_is_pending() -> None:
    done = days_back(MONDAY - timedelta(days=1), 3)
    assert habit_streak(done, ALL_WEEKDAYS, MONDAY, MONDAY - timedelta(days=30)) == 3


def test_streak_counts_today_when_done() -> None:
    done = days_back(MONDAY, 4)
    assert habit_streak(done, ALL_WEEKDAYS, MONDAY, MONDAY - timedelta(days=30)) == 4


def test_streak_breaks_on_missed_scheduled_day() -> None:
    done = {MONDAY, MONDAY - timedelta(days=1), MONDAY - timedelta(days=3)}
    assert habit_streak(done, ALL_WEEKDAYS, MONDAY, MONDAY - timedelta(days=30)) == 2


def test_streak_skips_unscheduled_days() -> None:
    weekdays = (0, 2, 4)
    done = {MONDAY, MONDAY - timedelta(days=3), MONDAY - timedelta(days=5)}
    assert habit_streak(done, weekdays, MONDAY, MONDAY - timedelta(days=30)) == 3


def test_global_streak() -> None:
    assert global_streak(days_back(MONDAY, 5), MONDAY) == 5
    assert global_streak(days_back(MONDAY - timedelta(days=1), 2), MONDAY) == 2
    assert global_streak({MONDAY - timedelta(days=2)}, MONDAY) == 0


def test_rate_respects_habit_age() -> None:
    created = MONDAY - timedelta(days=1)
    assert completion_rate({created}, ALL_WEEKDAYS, MONDAY, created) == 1.0


def test_today_only_counts_after_check_in() -> None:
    assert completion(set(), ALL_WEEKDAYS, MONDAY, MONDAY).scheduled == 0
    assert completion({MONDAY}, ALL_WEEKDAYS, MONDAY, MONDAY).rate == 1.0


def test_rate_over_window() -> None:
    created = MONDAY - timedelta(days=60)
    done = days_back(MONDAY - timedelta(days=1), 15)
    assert completion_rate(done, ALL_WEEKDAYS, MONDAY, created) == round(15 / 29, 3)
