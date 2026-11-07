import { Link } from 'react-router-dom';
import { isDemo } from '../../api/index.js';
import styles from './AuthLayout.module.css';

export default function AuthLayout({ title, subtitle, children, footer }) {
  return (
    <main className={styles.page}>
      <div className={styles.box}>
        <Link to="/" className={styles.brand}>
          <span aria-hidden="true">🎯</span> Habit Tracker
        </Link>
        <h1 className={styles.title}>{title}</h1>
        {subtitle && <p className={styles.subtitle}>{subtitle}</p>}
        {isDemo && <p className={styles.demo}>Modo demonstração: tudo roda no seu navegador.</p>}
        {children}
        {footer && <p className={styles.footer}>{footer}</p>}
      </div>
    </main>
  );
}
