import { createContext, useCallback, useContext, useMemo, useRef, useState } from 'react';
import Toaster from '../components/organisms/Toaster/Toaster.jsx';

const ToastContext = createContext(null);

export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([]);
  const counter = useRef(0);

  const dismiss = useCallback((id) => setToasts((list) => list.filter((t) => t.id !== id)), []);

  const notify = useCallback(
    (toast) => {
      counter.current += 1;
      const id = counter.current;
      setToasts((list) => [...list.slice(-3), { tone: 'info', ...toast, id }]);
      setTimeout(() => dismiss(id), toast.duration ?? 4200);
    },
    [dismiss],
  );

  const value = useMemo(() => ({ notify }), [notify]);
  return (
    <ToastContext.Provider value={value}>
      {children}
      <Toaster toasts={toasts} onDismiss={dismiss} />
    </ToastContext.Provider>
  );
}

export function useToast() {
  const context = useContext(ToastContext);
  if (!context) throw new Error('useToast precisa estar dentro de <ToastProvider>');
  return context;
}
