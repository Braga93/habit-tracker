import { WEEKDAY_SHORT } from '../../../utils/format.js';
import styles from './WeekdayPicker.module.css';

export default function WeekdayPicker({ value, onChange }) {
  function toggle(day) {
    const next = value.includes(day) ? value.filter((d) => d !== day) : [...value, day].sort();
    if (next.length) onChange(next);
  }
  return (
    <fieldset className={styles.fieldset}>
      <legend className={styles.legend}>Dias da semana</legend>
      <div className={styles.days}>
        {WEEKDAY_SHORT.map((label, day) => (
          <button key={label} type="button" className={styles.day} aria-pressed={value.includes(day)} onClick={() => toggle(day)}>
            {label}
          </button>
        ))}
      </div>
    </fieldset>
  );
}
