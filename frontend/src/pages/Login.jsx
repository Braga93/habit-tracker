import { useState } from 'react';
import { Link, Navigate, useLocation, useNavigate } from 'react-router-dom';
import { isDemo } from '../api/index.js';
import { DEMO_PASSWORD, DEMO_USERNAME } from '../api/demo.js';
import { useAuth } from '../context/AuthContext.jsx';
import { Button, Input } from '../components/atoms';
import AuthLayout from '../components/templates/AuthLayout.jsx';

export default function Login() {
  const { user, login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [form, setForm] = useState(isDemo ? { username: DEMO_USERNAME, password: DEMO_PASSWORD } : { username: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  if (user) return <Navigate to="/painel" replace />;

  async function submit(event) {
    event.preventDefault();
    setError('');
    setLoading(true);
    try {
      await login(form);
      navigate(location.state?.from ?? '/painel', { replace: true });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <AuthLayout
      title="Entrar"
      subtitle="Bom te ver de novo."
      footer={
        isDemo ? null : (
          <>
            Ainda não tem conta? <Link to="/criar-conta">Criar conta</Link>
          </>
        )
      }
    >
      <form onSubmit={submit} style={{ display: 'flex', flexDirection: 'column', gap: 14 }} noValidate>
        <Input
          label="Usuário ou e-mail"
          autoComplete="username"
          value={form.username}
          onChange={(e) => setForm((f) => ({ ...f, username: e.target.value }))}
          required
        />
        <Input
          label="Senha"
          type="password"
          autoComplete="current-password"
          value={form.password}
          onChange={(e) => setForm((f) => ({ ...f, password: e.target.value }))}
          required
          error={error}
        />
        <Button type="submit" block loading={loading} disabled={!form.username || !form.password}>
          {isDemo ? 'Entrar como visitante' : 'Entrar'}
        </Button>
      </form>
    </AuthLayout>
  );
}
