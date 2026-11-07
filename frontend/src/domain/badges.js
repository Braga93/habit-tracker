export const BADGES = [
  { code: 'arquiteto', name: 'Arquiteto', description: 'Crie o seu primeiro hábito', icon: '🧱', kind: 'habits', threshold: 1, xp_bonus: 25 },
  { code: 'primeiro_passo', name: 'Primeiro Passo', description: 'Faça o seu primeiro check-in', icon: '👣', kind: 'checkins', threshold: 1, xp_bonus: 25 },
  { code: 'aquecendo', name: 'Aquecendo', description: 'Mantenha 3 dias seguidos', icon: '🔥', kind: 'streak', threshold: 3, xp_bonus: 50 },
  { code: 'semana_de_ferro', name: 'Semana de Ferro', description: 'Mantenha 7 dias seguidos', icon: '⚡', kind: 'streak', threshold: 7, xp_bonus: 100 },
  { code: 'inabalavel', name: 'Inabalável', description: 'Mantenha 30 dias seguidos', icon: '🌟', kind: 'streak', threshold: 30, xp_bonus: 300 },
  { code: 'centenario', name: 'Centenário', description: 'Complete 100 check-ins', icon: '💯', kind: 'checkins', threshold: 100, xp_bonus: 200 },
  { code: 'veterano', name: 'Veterano', description: 'Alcance o nível 5', icon: '🎖️', kind: 'level', threshold: 5, xp_bonus: 150 },
  { code: 'mestre', name: 'Mestre dos Hábitos', description: 'Complete 500 check-ins', icon: '🏆', kind: 'checkins', threshold: 500, xp_bonus: 500 },
];

export function isUnlocked(badge, stats) {
  const value = {
    habits: stats.habitsCreated,
    checkins: stats.checkins,
    streak: stats.streak,
    level: stats.level,
  }[badge.kind];
  return value >= badge.threshold;
}

export function newlyUnlocked(stats, earned) {
  return BADGES.filter((badge) => !earned.has(badge.code) && isUnlocked(badge, stats));
}
