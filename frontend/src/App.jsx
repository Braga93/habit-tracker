import { HashRouter, Navigate, Route, Routes } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext.jsx';
import { ToastProvider } from './context/ToastContext.jsx';
import ProtectedRoute from './components/templates/ProtectedRoute.jsx';
import AppLayout from './components/templates/AppLayout.jsx';
import Landing from './pages/Landing.jsx';
import Login from './pages/Login.jsx';
import Register from './pages/Register.jsx';
import Dashboard from './pages/Dashboard.jsx';
import Habits from './pages/Habits.jsx';
import Coach from './pages/Coach.jsx';
import Profile from './pages/Profile.jsx';
import NotFound from './pages/NotFound.jsx';

export default function App() {
  return (
    <HashRouter>
      <ToastProvider>
        <AuthProvider>
          <Routes>
            <Route path="/" element={<Landing />} />
            <Route path="/entrar" element={<Login />} />
            <Route path="/criar-conta" element={<Register />} />
            <Route element={<ProtectedRoute />}>
              <Route element={<AppLayout />}>
                <Route path="/painel" element={<Dashboard />} />
                <Route path="/habitos" element={<Habits />} />
                <Route path="/coach" element={<Coach />} />
                <Route path="/perfil" element={<Profile />} />
              </Route>
            </Route>
            <Route path="/inicio" element={<Navigate to="/" replace />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </AuthProvider>
      </ToastProvider>
    </HashRouter>
  );
}
