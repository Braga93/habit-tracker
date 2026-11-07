DIFFICULTY_XP = {"easy": 10, "medium": 20, "hard": 30}

STREAK_BONUSES = {7: 50, 14: 75, 30: 150, 60: 300, 100: 500}


def xp_for_difficulty(difficulty: str) -> int:
    return DIFFICULTY_XP.get(difficulty, DIFFICULTY_XP["medium"])


def streak_bonus(streak: int) -> int:
    return STREAK_BONUSES.get(streak, 0)
