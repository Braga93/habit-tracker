import { ApiError } from './errors.js';
import { readToken } from './token.js';
import { addDays, todayISO, weekday } from '../domain/dates.js';
import { levelFromXp, levelProgress } from '../domain/levels.js';
import { streakBonus, xpForDifficulty } from '../domain/rewards.js';
import { ALL_WEEKDAYS, completion, completionRate, globalStreak, habitStreak, isScheduled } from '../domain/schedule.js';
import { BADGES, newlyUnlocked } from '../domain/badges.js';
import { buildInsights, ruleBasedReply } from '../domain/coach.js';

const STORAGE_KEY = 'habit-tracker-demo-v1';
export const DEMO_USERNAME = 'visitante';
export const DEMO_PASSWORD = 'demonstracao';

let memory = null;

function emptyState() {
  return { seq: 1, users: [], habits: [], checkins: [], badges: [], xpEvents: [] };
}

function load() {
  if (memory) return memory;
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    memory = raw ? JSON.parse(raw) : null;
  } catch {
    memory = null;
  }
  if (!memory) {
    memory = emptyState();
    seed(memory);
    persist();
  }
  return memory;
}

function persist() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(memory));
  } catch {
    return;
  }
}

export function resetDemo() {
  memory = emptyState();
  seed(memory);
  persist();
}

const nextId = (state) => state.seq++;
const nowISO = () => new Date().toISOString();
const delay = (ms = 150) => new Promise((resolve) => setTimeout(resolve, ms));

function publicUser(user) {
  return { id: user.id, username: user.username, email: user.email, created_at: user.created_at };
}

function currentUser(state) {
  const token = readToken();
  const id = token?.startsWith('demo-') ? Number(token.slice(5)) : null;
  const user = state.users.find((u) => u.id === id);
  if (!user) throw new ApiError('Sessão inválida ou expirada. Entre novamente.', 401);
  return user;
}

function award(state, user, amount, reason, at = nowISO()) {
  if (amount <= 0) return;
  user.total_xp += amount;
  state.xpEvents.push({ id: nextId(state), user_id: user.id, amount, reason, created_at: at });
}

function revoke(state, user, amount, reason) {
  const removed = Math.min(amount, user.total_xp);
  if (removed <= 0) return;
  user.total_xp -= removed;
  state.xpEvents.push({ id: nextId(state), user_id: user.id, amount: -removed, reason, created_at: nowISO() });
}

const userCheckins = (state, user) => state.checkins.filter((c) => c.user_id === user.id);
const activeDays = (state, user) => new Set(userCheckins(state, user).map((c) => c.day));
const habitDays = (state, habit) => new Set(state.checkins.filter((c) => c.habit_id === habit.id).map((c) => c.day));
const activeHabits = (state, user) => state.habits.filter((h) => h.user_id === user.id && !h.archived);

function evaluateBadges(state, user, today, at) {
  const earned = new Set(state.badges.filter((b) => b.user_id === user.id).map((b) => b.code));
  const unlocked = [];
  for (;;) {
    const stats = {
      habitsCreated: state.habits.filter((h) => h.user_id === user.id).length,
      checkins: userCheckins(state, user).length,
      streak: globalStreak(activeDays(state, user), today),
      level: levelFromXp(user.total_xp),
    };
    const fresh = newlyUnlocked(stats, earned);
    if (!fresh.length) return unlocked;
    fresh.forEach((badge) => {
      state.badges.push({ user_id: user.id, code: badge.code, earned_at: at ?? nowISO() });
      award(state, user, badge.xp_bonus, `Medalha: ${badge.name}`, at);
      earned.add(badge.code);
      unlocked.push(badge);
    });
  }
}

const badgeOut = (badge, earned) => ({
  code: badge.code,
  name: badge.name,
  description: badge.description,
  icon: badge.icon,
  xp_bonus: badge.xp_bonus,
  earned: Boolean(earned),
  earned_at: earned?.earned_at ?? null,
});

function habitOut(state, habit, today) {
  const done = habitDays(state, habit);
  return {
    id: habit.id,
    name: habit.name,
    cue: habit.cue,
    routine: habit.routine,
    reward: habit.reward,
    icon: habit.icon,
    difficulty: habit.difficulty,
    xp: xpForDifficulty(habit.difficulty),
    weekdays: habit.weekdays,
    created_on: habit.created_on,
    streak: habitStreak(done, habit.weekdays, today, habit.created_on),
    completion_rate: completionRate(done, habit.weekdays, today, habit.created_on),
    total_checkins: done.size,
    scheduled_today: isScheduled(habit.weekdays, today),
    done_today: done.has(today),
  };
}

function ownedHabit(state, user, id) {
  const habit = state.habits.find((h) => h.id === Number(id) && h.user_id === user.id && !h.archived);
  if (!habit) throw new ApiError('Hábito não encontrado.', 404);
  return habit;
}

function validateHabit(data) {
  for (const field of ['name', 'cue', 'routine', 'reward']) {
    if (data[field] !== undefined && !String(data[field]).trim()) {
      throw new ApiError('Confira os campos: alguns valores não são válidos.', 422);
    }
  }
}

function createHabitFor(state, user, data, today, at) {
  validateHabit(data);
  const habit = {
    id: nextId(state),
    user_id: user.id,
    name: data.name.trim(),
    cue: data.cue.trim(),
    routine: data.routine.trim(),
    reward: data.reward.trim(),
    icon: data.icon || '🎯',
    difficulty: data.difficulty || 'medium',
    weekdays: [...new Set(data.weekdays?.length ? data.weekdays : ALL_WEEKDAYS)].sort(),
    archived: false,
    created_on: today,
  };
  state.habits.push(habit);
  const unlocked = evaluateBadges(state, user, today, at);
  return { habit, unlocked };
}

function checkInFor(state, user, habit, data, today, at) {
  if (habitDays(state, habit).has(today)) throw new ApiError('Este hábito já foi registrado hoje.', 409);
  const levelBefore = levelFromXp(user.total_xp);
  const firstOfDay = !activeDays(state, user).has(today);
  const gained = xpForDifficulty(habit.difficulty);
  const checkin = {
    id: nextId(state),
    user_id: user.id,
    habit_id: habit.id,
    day: today,
    mood: data?.mood ?? null,
    note: data?.note?.trim() || null,
    xp_earned: gained,
  };
  state.checkins.push(checkin);
  award(state, user, gained, `Check-in: ${habit.name}`, at);
  const streak = globalStreak(activeDays(state, user), today);
  const bonus = firstOfDay ? streakBonus(streak) : 0;
  if (bonus) {
    award(state, user, bonus, `Bônus de ${streak} dias seguidos`, at);
    checkin.xp_earned += bonus;
  }
  const unlocked = evaluateBadges(state, user, today, at);
  return {
    habit: habitOut(state, habit, today),
    xp_gained: gained,
    streak_bonus: bonus,
    streak,
    new_badges: unlocked.map((b) => badgeOut(b)),
    level: levelProgress(user.total_xp),
    leveled_up: levelFromXp(user.total_xp) > levelBefore,
  };
}

function coachContext(state, user, today) {
  const habits = activeHabits(state, user).map((habit) => {
    const done = habitDays(state, habit);
    const week = completion(done, habit.weekdays, today, habit.created_on, 7);
    const month = completion(done, habit.weekdays, today, habit.created_on, 30);
    return {
      name: habit.name,
      icon: habit.icon,
      cue: habit.cue,
      routine: habit.routine,
      streak: habitStreak(done, habit.weekdays, today, habit.created_on),
      rate_7: week.rate,
      scheduled_7: week.scheduled,
      rate_30: month.rate,
      scheduled_30: month.scheduled,
      scheduled_today: isScheduled(habit.weekdays, today),
      done_today: done.has(today),
    };
  });
  const since = addDays(today, -55);
  const counts = {};
  userCheckins(state, user)
    .filter((c) => c.day >= since)
    .forEach((c) => {
      const day = weekday(c.day);
      counts[day] = (counts[day] ?? 0) + 1;
    });
  return {
    username: user.username,
    level: levelFromXp(user.total_xp),
    total_xp: user.total_xp,
    streak: globalStreak(activeDays(state, user), today),
    habits,
    checkins_by_weekday: counts,
  };
}

function random(seedValue) {
  let value = seedValue;
  return () => {
    value = (value * 1664525 + 1013904223) % 4294967296;
    return value / 4294967296;
  };
}

const SAMPLE_HABITS = [
  { name: 'Ler', icon: '📚', cue: 'Depois do café da manhã', routine: 'Ler 10 páginas de um livro', reward: 'Tomar um chá com calma', difficulty: 'medium', weekdays: ALL_WEEKDAYS, age: 45, chance: 0.85 },
  { name: 'Correr', icon: '🏃', cue: 'Ao acordar, calçar o tênis', routine: 'Correr 20 minutos', reward: 'Banho quente', difficulty: 'hard', weekdays: [0, 2, 4], age: 40, chance: 0.75 },
  { name: 'Beber água', icon: '💧', cue: 'Ao sentar na mesa de trabalho', routine: 'Beber um copo de água', reward: 'Riscar no quadro', difficulty: 'easy', weekdays: ALL_WEEKDAYS, age: 30, chance: 0.92, doneToday: true },
  { name: 'Meditar', icon: '🧘', cue: 'Antes de dormir', routine: 'Meditar 5 minutos', reward: 'Ouvir uma música', difficulty: 'medium', weekdays: ALL_WEEKDAYS, age: 21, chance: 0.6, fading: true },
];

function seed(state) {
  const today = todayISO();
  const rng = random(20261107);
  const user = {
    id: nextId(state),
    username: DEMO_USERNAME,
    email: 'visitante@demo.local',
    password: DEMO_PASSWORD,
    total_xp: 0,
    created_at: `${addDays(today, -46)}T12:00:00.000Z`,
  };
  state.users.push(user);

  const created = SAMPLE_HABITS.map((sample) => ({ sample, start: addDays(today, -sample.age), habit: null }));
  for (let offset = 46; offset >= 0; offset -= 1) {
    const day = addDays(today, -offset);
    const at = `${day}T20:00:00.000Z`;
    created
      .filter((entry) => entry.start === day)
      .forEach((entry) => {
        entry.habit = createHabitFor(state, user, entry.sample, day, at).habit;
      });
    created
      .filter((entry) => entry.habit && isScheduled(entry.habit.weekdays, day))
      .forEach(({ sample, habit }) => {
        let chance = sample.chance;
        if (sample.fading && offset < 8) chance = 0.25;
        if (offset < 6) chance = Math.max(chance, sample.fading ? 0.25 : 0.95);
        const doIt = offset === 0 ? Boolean(sample.doneToday) : rng() < chance;
        if (doIt) checkInFor(state, user, habit, { mood: 3 + Math.floor(rng() * 3) }, day, at);
      });
  }
}

export const demoApi = {
  mode: 'demo',
  async register() {
    await delay();
    throw new ApiError('No modo demonstração, use a conta de visitante.', 400);
  },
  async login({ username, password }) {
    await delay();
    const state = load();
    const user = state.users.find((u) => u.username === username.trim() || u.email === username.trim().toLowerCase());
    if (!user || user.password !== password) throw new ApiError('Usuário ou senha incorretos.', 401);
    return { access_token: `demo-${user.id}`, token_type: 'bearer', user: publicUser(user) };
  },
  async me() {
    await delay(50);
    return publicUser(currentUser(load()));
  },
  async listHabits() {
    await delay();
    const state = load();
    const user = currentUser(state);
    const today = todayISO();
    return activeHabits(state, user).map((h) => habitOut(state, h, today));
  },
  async createHabit(data) {
    await delay();
    const state = load();
    const user = currentUser(state);
    const today = todayISO();
    const { habit, unlocked } = createHabitFor(state, user, data, today);
    persist();
    return { habit: habitOut(state, habit, today), new_badges: unlocked.map((b) => badgeOut(b)) };
  },
  async updateHabit(id, data) {
    await delay();
    const state = load();
    const user = currentUser(state);
    const habit = ownedHabit(state, user, id);
    validateHabit(data);
    ['name', 'cue', 'routine', 'reward'].forEach((field) => {
      if (data[field] !== undefined) habit[field] = data[field].trim();
    });
    if (data.icon) habit.icon = data.icon;
    if (data.difficulty) habit.difficulty = data.difficulty;
    if (data.weekdays?.length) habit.weekdays = [...new Set(data.weekdays)].sort();
    persist();
    return habitOut(state, habit, todayISO());
  },
  async archiveHabit(id) {
    await delay();
    const state = load();
    ownedHabit(state, currentUser(state), id).archived = true;
    persist();
    return null;
  },
  async checkIn(id, data = {}) {
    await delay();
    const state = load();
    const user = currentUser(state);
    const result = checkInFor(state, user, ownedHabit(state, user, id), data, todayISO());
    persist();
    return result;
  },
  async undoCheckIn(id) {
    await delay();
    const state = load();
    const user = currentUser(state);
    const habit = ownedHabit(state, user, id);
    const today = todayISO();
    const index = state.checkins.findIndex((c) => c.habit_id === habit.id && c.day === today);
    if (index === -1) throw new ApiError('Não há registro de hoje para desfazer.', 404);
    revoke(state, user, state.checkins[index].xp_earned, `Check-in desfeito: ${habit.name}`);
    state.checkins.splice(index, 1);
    persist();
    return habitOut(state, habit, today);
  },
  async progress() {
    await delay();
    const state = load();
    const user = currentUser(state);
    const today = todayISO();
    const perDay = {};
    userCheckins(state, user).forEach((c) => {
      perDay[c.day] = (perDay[c.day] ?? 0) + 1;
    });
    const heatmap = Array.from({ length: 84 }, (_, i) => {
      const day = addDays(today, i - 83);
      return { day, count: perDay[day] ?? 0 };
    });
    const habits = activeHabits(state, user);
    const scheduled = habits.filter((h) => isScheduled(h.weekdays, today));
    const doneToday = new Set(userCheckins(state, user).filter((c) => c.day === today).map((c) => c.habit_id));
    const earned = Object.fromEntries(state.badges.filter((b) => b.user_id === user.id).map((b) => [b.code, b]));
    return {
      user: publicUser(user),
      level: levelProgress(user.total_xp),
      streak: globalStreak(activeDays(state, user), today),
      total_checkins: userCheckins(state, user).length,
      today: { done: scheduled.filter((h) => doneToday.has(h.id)).length, scheduled: scheduled.length },
      heatmap,
      badges: BADGES.map((b) => badgeOut(b, earned[b.code])),
      recent_xp: state.xpEvents
        .filter((e) => e.user_id === user.id)
        .slice(-8)
        .reverse()
        .map(({ amount, reason, created_at }) => ({ amount, reason, created_at })),
    };
  },
  async insights() {
    await delay();
    const state = load();
    return { insights: buildInsights(coachContext(state, currentUser(state), todayISO())), ai_enabled: false };
  },
  async chat({ message }) {
    await delay(450);
    const state = load();
    return { reply: ruleBasedReply(message, coachContext(state, currentUser(state), todayISO())), source: 'regras', notice: null };
  },
};
