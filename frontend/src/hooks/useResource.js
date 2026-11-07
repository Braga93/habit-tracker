import { useCallback, useEffect, useRef, useState } from 'react';
import { useAuth } from '../context/AuthContext.jsx';

export default function useResource(loader) {
  const { logout } = useAuth();
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const loaderRef = useRef(loader);
  loaderRef.current = loader;

  const reload = useCallback(async () => {
    try {
      const result = await loaderRef.current();
      setData(result);
      setError(null);
      return result;
    } catch (err) {
      if (err.status === 401) logout();
      setError(err);
      return null;
    } finally {
      setLoading(false);
    }
  }, [logout]);

  useEffect(() => {
    reload();
  }, [reload]);

  return { data, setData, error, loading, reload };
}
