export function xpForLevel(level) {
  return 50 * level * (level - 1);
}

export function levelFromXp(totalXp) {
  let level = 1;
  while (totalXp >= xpForLevel(level + 1)) level += 1;
  return level;
}

export function levelProgress(totalXp) {
  const xp = Math.max(0, totalXp);
  const level = levelFromXp(xp);
  const floor = xpForLevel(level);
  const next = xpForLevel(level + 1);
  return {
    level,
    total_xp: xp,
    current: xp - floor,
    needed: next - floor,
    percent: Math.round(((xp - floor) / (next - floor)) * 1000) / 10,
  };
}
