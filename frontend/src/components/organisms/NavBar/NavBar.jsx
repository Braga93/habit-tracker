import { NavLink } from 'react-router-dom';
import { useAuth } from '../../../context/AuthContext.jsx';
import styles from './NavBar.module.css';

const LINKS = [
  { to: '/painel', label: 'Hoje', icon: '📅' },
  { to: '/habitos', label: 'Hábitos', icon: '🎯' },
  { to: '/coach', label: 'Coach', icon: '🧠' },
  { to: '/perfil', label: 'Perfil', icon: '🏅' },
];

export default function NavBar() {
  const { user, logout } = useAuth();
  return (
    <header className={styles.header}>
      <div className={styles.inner}>
        <NavLink to="/painel" className={styles.brand}>
          <span aria-hidden="true">🎯</span> Habit Tracker
        </NavLink>
        <nav aria-label="Navegação principal" className={styles.nav}>
          <ul className={styles.links}>
            {LINKS.map((link) => (
              <li key={link.to}>
                <NavLink to={link.to} className={({ isActive }) => `${styles.link} ${isActive ? styles.active : ''}`}>
                  <span aria-hidden="true">{link.icon}</span>
                  <span className={styles.label}>{link.label}</span>
                </NavLink>
              </li>
            ))}
          </ul>
        </nav>
        <div className={styles.user}>
          <span className={styles.username}>@{user?.username}</span>
          <button type="button" className={styles.logout} onClick={logout}>
            Sair
          </button>
        </div>
      </div>
    </header>
  );
}
