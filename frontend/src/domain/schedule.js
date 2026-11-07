import { addDays, weekday } from './dates.js';

export const ALL_WEEKDAYS = [0, 1, 2, 3, 4, 5, 6];
const MAX_LOOKBACK_DAYS = 3660;

export function isScheduled(weekdays, iso) {
  return weekdays.includes(weekday(iso));
}

export function habitStreak(done, weekdays, today, createdOn) {
  let cursor = today;
  if (isScheduled(weekdays, cursor) && !done.has(cursor)) cursor = addDays(cursor, -1);
  let streak = 0;
  for (let i = 0; i < MAX_LOOKBACK_DAYS; i += 1) {
    if (cursor < createdOn) break;
    if (isScheduled(weekdays, cursor)) {
      if (!done.has(cursor)) break;
      streak += 1;
    }
    cursor = addDays(cursor, -1);
  }
  return streak;
}

export function globalStreak(activeDays, today) {
  let cursor = activeDays.has(today) ? today : addDays(today, -1);
  let streak = 0;
  while (activeDays.has(cursor)) {
    streak += 1;
    cursor = addDays(cursor, -1);
  }
  return streak;
}

export function completion(done, weekdays, today, createdOn, windowDays = 30) {
  const windowStart = addDays(today, -(windowDays - 1));
  let cursor = createdOn > windowStart ? createdOn : windowStart;
  let scheduled = 0;
  let completed = 0;
  while (cursor <= today) {
    const counts = isScheduled(weekdays, cursor) && (cursor !== today || done.has(cursor));
    if (counts) {
      scheduled += 1;
      if (done.has(cursor)) completed += 1;
    }
    cursor = addDays(cursor, 1);
  }
  const rate = scheduled ? Math.round((completed / scheduled) * 1000) / 1000 : 0;
  return { completed, scheduled, rate };
}

export function completionRate(done, weekdays, today, createdOn, windowDays = 30) {
  return completion(done, weekdays, today, createdOn, windowDays).rate;
}
