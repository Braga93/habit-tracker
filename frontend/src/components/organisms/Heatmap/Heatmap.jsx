import { shortDate } from '../../../utils/format.js';
import styles from './Heatmap.module.css';

function intensity(count, max) {
  if (!count) return 0;
  return Math.min(4, Math.ceil((count / Math.max(max, 1)) * 4));
}

export default function Heatmap({ days }) {
  const max = Math.max(...days.map((d) => d.count), 1);
  const active = days.filter((d) => d.count > 0).length;
  const firstWeekday = (new Date(`${days[0].day}T12:00:00`).getDay() + 6) % 7;
  const cells = [...Array(firstWeekday).fill(null), ...days];

  return (
    <figure className={styles.figure}>
      <div className={styles.grid} role="img" aria-label={`${active} dias com check-in nas últimas 12 semanas`}>
        {cells.map((cell, index) =>
          cell ? (
            <span
              key={cell.day}
              className={styles.cell}
              data-level={intensity(cell.count, max)}
              title={`${shortDate(cell.day)}: ${cell.count} check-in(s)`}
            />
          ) : (
            <span key={`vazio-${index}`} className={styles.empty} />
          ),
        )}
      </div>
      <figcaption className={styles.caption}>
        <span>{active} dias ativos em 12 semanas</span>
        <span className={styles.legend} aria-hidden="true">
          menos
          {[0, 1, 2, 3, 4].map((level) => (
            <span key={level} className={styles.cell} data-level={level} />
          ))}
          mais
        </span>
      </figcaption>
    </figure>
  );
}
