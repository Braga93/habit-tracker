import styles from './InsightCard.module.css';

const ICONS = { alerta: '⚠️', destaque: '⭐', sequencia: '🔥', dica: '💡' };

export default function InsightCard({ insight }) {
  return (
    <li className={`${styles.card} ${styles[insight.kind] ?? ''}`}>
      <span className={styles.icon} aria-hidden="true">
        {ICONS[insight.kind] ?? '💡'}
      </span>
      <div>
        <p className={styles.title}>{insight.title}</p>
        <p className={styles.message}>{insight.message}</p>
      </div>
    </li>
  );
}
