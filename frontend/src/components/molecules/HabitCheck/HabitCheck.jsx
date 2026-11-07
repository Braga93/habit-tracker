import { Spinner, Tag } from '../../atoms';
import styles from './HabitCheck.module.css';

export default function HabitCheck({ habit, busy, onToggle }) {
  const done = habit.done_today;
  return (
    <li className={`${styles.item} ${done ? styles.done : ''}`}>
      <button
        type="button"
        className={styles.check}
        onClick={() => onToggle(habit)}
        disabled={busy}
        aria-pressed={done}
        aria-label={done ? `Desfazer check-in de ${habit.name}` : `Marcar ${habit.name} como feito hoje`}
      >
        {busy ? <Spinner size={18} /> : <span aria-hidden="true">{done ? '✓' : ''}</span>}
      </button>
      <span className={styles.icon} aria-hidden="true">
        {habit.icon}
      </span>
      <div className={styles.body}>
        <p className={styles.name}>{habit.name}</p>
        <p className={styles.loop}>
          {habit.cue} → {habit.routine}
        </p>
      </div>
      <div className={styles.meta}>
        {habit.streak > 0 && <Tag tone="xp">🔥 {habit.streak}</Tag>}
        <Tag tone={done ? 'success' : 'accent'}>+{habit.xp} XP</Tag>
      </div>
    </li>
  );
}
