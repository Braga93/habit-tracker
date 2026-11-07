import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react';
import { api, readToken, saveToken } from '../api/index.js';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [checking, setChecking] = useState(() => Boolean(readToken()));

  useEffect(() => {
    if (!readToken()) return;
    let active = true;
    api
      .me()
      .then((me) => active && setUser(me))
      .catch(() => {
        saveToken(null);
        if (active) setUser(null);
      })
      .finally(() => active && setChecking(false));
    return () => {
      active = false;
    };
  }, []);

  const startSession = useCallback((session) => {
    saveToken(session.access_token);
    setUser(session.user);
    return session.user;
  }, []);

  const login = useCallback((credentials) => api.login(credentials).then(startSession), [startSession]);
  const register = useCallback((data) => api.register(data).then(startSession), [startSession]);

  const logout = useCallback(() => {
    saveToken(null);
    setUser(null);
  }, []);

  const value = useMemo(() => ({ user, checking, login, register, logout }), [user, checking, login, register, logout]);
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth precisa estar dentro de <AuthProvider>');
  return context;
}
