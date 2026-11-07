export const DIFFICULTY_XP = { easy: 10, medium: 20, hard: 30 };

export const STREAK_BONUSES = { 7: 50, 14: 75, 30: 150, 60: 300, 100: 500 };

export function xpForDifficulty(difficulty) {
  return DIFFICULTY_XP[difficulty] ?? DIFFICULTY_XP.medium;
}

export function streakBonus(streak) {
  return STREAK_BONUSES[streak] ?? 0;
}
