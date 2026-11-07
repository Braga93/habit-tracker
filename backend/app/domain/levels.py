from dataclasses import dataclass


def xp_for_level(level: int) -> int:
    return 50 * level * (level - 1)


def level_from_xp(total_xp: int) -> int:
    level = 1
    while total_xp >= xp_for_level(level + 1):
        level += 1
    return level


@dataclass(frozen=True)
class LevelProgress:
    level: int
    total_xp: int
    level_floor: int
    next_level_at: int

    @property
    def current(self) -> int:
        return self.total_xp - self.level_floor

    @property
    def needed(self) -> int:
        return self.next_level_at - self.level_floor

    @property
    def percent(self) -> float:
        return round(self.current / self.needed * 100, 1)


def level_progress(total_xp: int) -> LevelProgress:
    total_xp = max(0, total_xp)
    level = level_from_xp(total_xp)
    return LevelProgress(
        level=level,
        total_xp=total_xp,
        level_floor=xp_for_level(level),
        next_level_at=xp_for_level(level + 1),
    )
