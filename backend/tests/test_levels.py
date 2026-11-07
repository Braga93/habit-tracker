import pytest

from app.domain.levels import level_from_xp, level_progress, xp_for_level


@pytest.mark.parametrize(
    ("xp", "level"),
    [(0, 1), (99, 1), (100, 2), (299, 2), (300, 3), (600, 4), (1000, 5)],
)
def test_level_from_xp(xp: int, level: int) -> None:
    assert level_from_xp(xp) == level


def test_new_user_starts_at_zero_percent() -> None:
    progress = level_progress(0)
    assert progress.level == 1
    assert progress.percent == 0
    assert progress.needed == xp_for_level(2)


def test_progress_resets_at_each_level() -> None:
    assert level_progress(100).percent == 0
    assert level_progress(200).percent == 50
