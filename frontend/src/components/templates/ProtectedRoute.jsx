import { Navigate, Outlet, useLocation } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext.jsx';
import { Spinner } from '../atoms';

export default function ProtectedRoute() {
  const { user, checking } = useAuth();
  const location = useLocation();
  if (checking) {
    return (
      <div style={{ display: 'grid', placeItems: 'center', minHeight: '100vh' }}>
        <Spinner size={32} label="Carregando" />
      </div>
    );
  }
  if (!user) return <Navigate to="/entrar" replace state={{ from: location.pathname }} />;
  return <Outlet />;
}
