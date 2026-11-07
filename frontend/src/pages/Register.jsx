import { useState } from 'react';
import { Link, Navigate, useNavigate } from 'react-router-dom';
import { isDemo } from '../api/index.js';
import { useAuth } from '../context/AuthContext.jsx';
import { Button, Input } from '../components/atoms';
import AuthLayout from '../components/templates/AuthLayout.jsx';

function validate({ username, email, password }) {
  const errors = {};
  if (!/^[a-zA-Z0-9_]{3,30}$/.test(username)) errors.username = 'De 3 a 30 caracteres: letras, números ou _.';
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) errors.email = 'Informe um e-mail válido.';
  if (password.length < 8) errors.password = 'A senha precisa de pelo menos 8 caracteres.';
  return errors;
}

export default function Register() {
  const { user, register } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ username: '', email: '', password: '' });
  const [errors, setErrors] = useState({});
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  if (user) return <Navigate to="/painel" replace />;

  if (isDemo) {
    return (
      <AuthLayout title="Criar conta" subtitle="No modo demonstração há uma conta pronta, com dados de exemplo.">
        <Button to="/entrar" block>
          Entrar como visitante
        </Button>
      </AuthLayout>
    );
  }

  const set = (field) => (event) => setForm((f) => ({ ...f, [field]: event.target.value }));

  async function submit(event) {
    event.preventDefault();
    const found = validate(form);
    setErrors(found);
    setError('');
    if (Object.keys(found).length) return;
    setLoading(true);
    try {
      await register(form);
      navigate('/habitos', { replace: true });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <AuthLayout
      title="Criar conta"
      subtitle="Leva menos de um minuto."
      footer={
        <>
          Já tem conta? <Link to="/entrar">Entrar</Link>
        </>
      }
    >
      <form onSubmit={submit} style={{ display: 'flex', flexDirection: 'column', gap: 14 }} noValidate>
        <Input label="Nome de usuário" autoComplete="username" value={form.username} onChange={set('username')} error={errors.username} />
        <Input label="E-mail" type="email" autoComplete="email" value={form.email} onChange={set('email')} error={errors.email} />
        <Input
          label="Senha"
          type="password"
          autoComplete="new-password"
          hint="Pelo menos 8 caracteres."
          value={form.password}
          onChange={set('password')}
          error={errors.password}
        />
        {error && (
          <p role="alert" style={{ color: 'var(--danger)', fontSize: '0.88rem' }}>
            {error}
          </p>
        )}
        <Button type="submit" block loading={loading}>
          Criar conta
        </Button>
      </form>
    </AuthLayout>
  );
}
