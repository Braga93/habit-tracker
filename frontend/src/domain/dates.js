export function toISODate(date) {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, '0');
  const d = String(date.getDate()).padStart(2, '0');
  return `${y}-${m}-${d}`;
}

export function fromISODate(iso) {
  const [y, m, d] = iso.split('-').map(Number);
  return new Date(y, m - 1, d);
}

export function addDays(iso, amount) {
  const date = fromISODate(iso);
  date.setDate(date.getDate() + amount);
  return toISODate(date);
}

export function weekday(iso) {
  return (fromISODate(iso).getDay() + 6) % 7;
}

export function todayISO() {
  return toISODate(new Date());
}

export function daysBetween(fromIso, toIso) {
  return Math.round((fromISODate(toIso) - fromISODate(fromIso)) / 86400000);
}
