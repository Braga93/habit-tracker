import styles from './StatCard.module.css';

export default function StatCard({ icon, label, value, hint, tone = 'accent' }) {
  return (
    <div className={`${styles.card} ${styles[tone]}`}>
      <span className={styles.icon} aria-hidden="true">
        {icon}
      </span>
      <div>
        <p className={styles.value}>{value}</p>
        <p className={styles.label}>{label}</p>
        {hint && <p className={styles.hint}>{hint}</p>}
      </div>
    </div>
  );
}
