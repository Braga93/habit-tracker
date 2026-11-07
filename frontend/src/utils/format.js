export const WEEKDAY_SHORT = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom'];

export const DIFFICULTY_LABEL = { easy: 'Fácil', medium: 'Médio', hard: 'Difícil' };

export function percent(rate) {
  return `${Math.round(rate * 100)}%`;
}

export function scheduleLabel(weekdays) {
  if (weekdays.length === 7) return 'Todos os dias';
  if (weekdays.join() === '0,1,2,3,4') return 'Dias úteis';
  if (weekdays.join() === '5,6') return 'Fins de semana';
  return weekdays.map((d) => WEEKDAY_SHORT[d]).join(', ');
}

export function shortDate(iso) {
  const [y, m, d] = iso.slice(0, 10).split('-').map(Number);
  return new Date(y, m - 1, d).toLocaleDateString('pt-BR', { day: '2-digit', month: 'short' });
}

export function greeting(date = new Date()) {
  const hour = date.getHours();
  if (hour < 12) return 'Bom dia';
  if (hour < 18) return 'Boa tarde';
  return 'Boa noite';
}
