import { beforeEach, describe, expect, it, vi } from 'vitest';

function memoryStorage() {
  const data = new Map();
  return {
    getItem: (key) => (data.has(key) ? data.get(key) : null),
    setItem: (key, value) => data.set(key, String(value)),
    removeItem: (key) => data.delete(key),
  };
}

describe('API de demonstração', () => {
  let demo;
  let token;

  beforeEach(async () => {
    vi.resetModules();
    vi.stubGlobal('localStorage', memoryStorage());
    demo = await import('./demo.js');
    token = await import('./token.js');
  });

  it('exige login', async () => {
    await expect(demo.demoApi.listHabits()).rejects.toMatchObject({ status: 401 });
  });

  it('entra como visitante e traz dados de exemplo coerentes', async () => {
    const session = await demo.demoApi.login({ username: demo.DEMO_USERNAME, password: demo.DEMO_PASSWORD });
    token.saveToken(session.access_token);

    const habits = await demo.demoApi.listHabits();
    expect(habits).toHaveLength(4);

    const progress = await demo.demoApi.progress();
    expect(progress.streak).toBeGreaterThanOrEqual(5);
    expect(progress.level.level).toBeGreaterThan(1);
    expect(progress.badges.filter((b) => b.earned).length).toBeGreaterThanOrEqual(3);
    expect(progress.heatmap).toHaveLength(84);

    const insights = await demo.demoApi.insights();
    expect(insights.insights.some((i) => i.kind === 'alerta')).toBe(true);
  });

  it('faz e desfaz check-in devolvendo o XP', async () => {
    const session = await demo.demoApi.login({ username: 'visitante', password: 'demonstracao' });
    token.saveToken(session.access_token);
    const pending = (await demo.demoApi.listHabits()).find((h) => h.scheduled_today && !h.done_today);
    const before = (await demo.demoApi.progress()).level.total_xp;

    const result = await demo.demoApi.checkIn(pending.id);
    expect(result.habit.done_today).toBe(true);
    await expect(demo.demoApi.checkIn(pending.id)).rejects.toMatchObject({ status: 409 });

    await demo.demoApi.undoCheckIn(pending.id);
    expect((await demo.demoApi.progress()).level.total_xp).toBe(before);
  });
});
