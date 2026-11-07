const KEY = 'habit-tracker-token';

export function readToken() {
  try {
    return localStorage.getItem(KEY);
  } catch {
    return null;
  }
}

export function saveToken(token) {
  try {
    if (token) localStorage.setItem(KEY, token);
    else localStorage.removeItem(KEY);
  } catch {
    return;
  }
}
