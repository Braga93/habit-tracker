import styles from './ProgressBar.module.css';

export default function ProgressBar({ value, label, tone = 'accent', size = 'md' }) {
  const clamped = Math.max(0, Math.min(100, value));
  return (
    <div className={`${styles.track} ${styles[size]}`} role="progressbar" aria-valuemin={0} aria-valuemax={100} aria-valuenow={Math.round(clamped)} aria-label={label}>
      <div className={`${styles.fill} ${styles[tone]}`} style={{ width: `${clamped}%` }} />
    </div>
  );
}
