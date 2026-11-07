import { ApiError } from './errors.js';
import { readToken } from './token.js';

const BASE = `${import.meta.env.VITE_API_URL ?? ''}/api`;

function messageFrom(body, status) {
  if (typeof body?.detail === 'string') return body.detail;
  if (Array.isArray(body?.detail) && body.detail[0]?.msg) return 'Confira os campos: alguns valores não são válidos.';
  if (status >= 500) return 'O servidor teve um problema. Tente de novo em instantes.';
  return 'Não foi possível concluir a ação.';
}

async function request(path, { method = 'GET', body } = {}) {
  const headers = { Accept: 'application/json' };
  const token = readToken();
  if (token) headers.Authorization = `Bearer ${token}`;
  if (body !== undefined) headers['Content-Type'] = 'application/json';

  let response;
  try {
    response = await fetch(`${BASE}${path}`, { method, headers, body: body === undefined ? undefined : JSON.stringify(body) });
  } catch {
    throw new ApiError('Sem conexão com a API. Ela está rodando?', 0);
  }
  if (response.status === 204) return null;
  const data = await response.json().catch(() => null);
  if (!response.ok) throw new ApiError(messageFrom(data, response.status), response.status);
  return data;
}

export const remoteApi = {
  mode: 'api',
  register: (data) => request('/auth/register', { method: 'POST', body: data }),
  login: (data) => request('/auth/login', { method: 'POST', body: data }),
  me: () => request('/auth/me'),
  listHabits: () => request('/habits'),
  createHabit: (data) => request('/habits', { method: 'POST', body: data }),
  updateHabit: (id, data) => request(`/habits/${id}`, { method: 'PATCH', body: data }),
  archiveHabit: (id) => request(`/habits/${id}`, { method: 'DELETE' }),
  checkIn: (id, data = {}) => request(`/habits/${id}/checkins`, { method: 'POST', body: data }),
  undoCheckIn: (id) => request(`/habits/${id}/checkins/today`, { method: 'DELETE' }),
  progress: () => request('/progress'),
  insights: () => request('/coach/insights'),
  chat: (data) => request('/coach/chat', { method: 'POST', body: data }),
};
