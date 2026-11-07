import { describe, expect, it } from 'vitest';
import { addDays } from './dates.js';
import { levelFromXp, levelProgress } from './levels.js';
import { ALL_WEEKDAYS, completion, completionRate, globalStreak, habitStreak } from './schedule.js';
import { newlyUnlocked } from './badges.js';
import { buildInsights, detectIntent, ruleBasedReply } from './coach.js';

const MONDAY = '2026-03-02';
const daysBack = (start, count) => new Set(Array.from({ length: count }, (_, i) => addDays(start, -i)));

describe('níveis', () => {
  it.each([
    [0, 1],
    [99, 1],
    [100, 2],
    [299, 2],
    [300, 3],
    [600, 4],
    [1000, 5],
  ])('%i XP = nível %i', (xp, level) => {
    expect(levelFromXp(xp)).toBe(level);
  });

  it('começa em 0% e reinicia a cada nível', () => {
    expect(levelProgress(0).percent).toBe(0);
    expect(levelProgress(100).percent).toBe(0);
    expect(levelProgress(200).percent).toBe(50);
  });
});

describe('sequências e conclusão', () => {
  const created = addDays(MONDAY, -30);

  it('mantém a sequência de ontem enquanto hoje está pendente', () => {
    expect(habitStreak(daysBack(addDays(MONDAY, -1), 3), ALL_WEEKDAYS, MONDAY, created)).toBe(3);
  });

  it('conta hoje quando já foi feito', () => {
    expect(habitStreak(daysBack(MONDAY, 4), ALL_WEEKDAYS, MONDAY, created)).toBe(4);
  });

  it('quebra em um dia agendado perdido', () => {
    const done = new Set([MONDAY, addDays(MONDAY, -1), addDays(MONDAY, -3)]);
    expect(habitStreak(done, ALL_WEEKDAYS, MONDAY, created)).toBe(2);
  });

  it('ignora dias não agendados', () => {
    const done = new Set([MONDAY, addDays(MONDAY, -3), addDays(MONDAY, -5)]);
    expect(habitStreak(done, [0, 2, 4], MONDAY, created)).toBe(3);
  });

  it('sequência geral', () => {
    expect(globalStreak(daysBack(MONDAY, 5), MONDAY)).toBe(5);
    expect(globalStreak(daysBack(addDays(MONDAY, -1), 2), MONDAY)).toBe(2);
    expect(globalStreak(new Set([addDays(MONDAY, -2)]), MONDAY)).toBe(0);
  });

  it('respeita a idade do hábito', () => {
    const yesterday = addDays(MONDAY, -1);
    expect(completionRate(new Set([yesterday]), ALL_WEEKDAYS, MONDAY, yesterday)).toBe(1);
    expect(completion(new Set(), ALL_WEEKDAYS, MONDAY, MONDAY).scheduled).toBe(0);
  });

  it('janela de 30 dias', () => {
    const done = daysBack(addDays(MONDAY, -1), 15);
    expect(completionRate(done, ALL_WEEKDAYS, MONDAY, addDays(MONDAY, -60))).toBe(Math.round((15 / 29) * 1000) / 1000);
  });
});

describe('medalhas', () => {
  it('primeiro hábito libera Arquiteto', () => {
    const codes = newlyUnlocked({ habitsCreated: 1, checkins: 0, streak: 0, level: 1 }, new Set()).map((b) => b.code);
    expect(codes).toEqual(['arquiteto']);
  });
});

describe('coach', () => {
  const habit = {
    name: 'Correr',
    icon: '🏃',
    cue: 'Ao acordar',
    routine: 'Correr 20 minutos',
    streak: 0,
    rate_7: 0.1,
    scheduled_7: 7,
    rate_30: 0.9,
    scheduled_30: 30,
    scheduled_today: true,
    done_today: true,
  };
  const context = { username: 'braga', level: 2, total_xp: 150, streak: 0, habits: [habit], checkins_by_weekday: {} };

  it('aponta hábito em risco', () => {
    expect(buildInsights(context)[0].kind).toBe('alerta');
  });

  it('entende intenções', () => {
    expect(detectIntent('Oi!')).toBe('saudacao');
    expect(detectIntent('Como estou indo?')).toBe('progresso');
    expect(detectIntent('Não consigo manter')).toBe('dificuldade');
  });

  it('responde com os dados do usuário', () => {
    expect(ruleBasedReply('não consigo', context)).toContain('Ao acordar');
  });
});
