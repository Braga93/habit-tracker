import { Button, ProgressBar } from '../../atoms';
import { HabitCheck } from '../../molecules';
import styles from './TodayList.module.css';

export default function TodayList({ habits, busyId, onToggle }) {
  const today = habits.filter((h) => h.scheduled_today);
  const others = habits.filter((h) => !h.scheduled_today);
  const done = today.filter((h) => h.done_today).length;

  if (!habits.length) {
    return (
      <div className={styles.empty}>
        <p className={styles.emptyIcon} aria-hidden="true">
          🌱
        </p>
        <p className={styles.emptyTitle}>Nenhum hábito ainda</p>
        <p className={styles.emptyText}>Crie o primeiro e ganhe a medalha Arquiteto.</p>
        <Button to="/habitos">Criar hábito</Button>
      </div>
    );
  }

  return (
    <div className={styles.wrapper}>
      <div className={styles.progress}>
        <ProgressBar value={today.length ? (done / today.length) * 100 : 0} tone="success" size="sm" label="Hábitos de hoje concluídos" />
        <span className={styles.count}>
          {done}/{today.length}
        </span>
      </div>
      {today.length ? (
        <ul className={styles.list}>
          {today.map((habit) => (
            <HabitCheck key={habit.id} habit={habit} busy={busyId === habit.id} onToggle={onToggle} />
          ))}
        </ul>
      ) : (
        <p className={styles.free}>Nenhum hábito agendado para hoje. Dia livre!</p>
      )}
      {others.length > 0 && (
        <details className={styles.others}>
          <summary>Fora da agenda de hoje ({others.length})</summary>
          <ul className={styles.list}>
            {others.map((habit) => (
              <HabitCheck key={habit.id} habit={habit} busy={busyId === habit.id} onToggle={onToggle} />
            ))}
          </ul>
        </details>
      )}
    </div>
  );
}
