from app.domain.badges import BadgeStats, newly_unlocked


def codes(stats: BadgeStats, earned: set[str] | None = None) -> set[str]:
    return {badge.code for badge in newly_unlocked(stats, earned or set())}


def test_first_habit_unlocks_architect() -> None:
    assert codes(BadgeStats(habits_created=1, checkins=0, streak=0, level=1)) == {"arquiteto"}


def test_already_earned_is_not_repeated() -> None:
    stats = BadgeStats(habits_created=1, checkins=1, streak=1, level=1)
    assert codes(stats, {"arquiteto"}) == {"primeiro_passo"}


def test_streak_and_level_badges() -> None:
    stats = BadgeStats(habits_created=3, checkins=40, streak=7, level=5)
    assert {"aquecendo", "semana_de_ferro", "veterano"} <= codes(stats)
    assert "inabalavel" not in codes(stats)
