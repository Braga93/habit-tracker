import { useState } from 'react';
import { Button, ProgressBar, Tag } from '../../atoms';
import HabitForm from '../HabitForm/HabitForm.jsx';
import { DIFFICULTY_LABEL, percent, scheduleLabel } from '../../../utils/format.js';
import styles from './HabitPanel.module.css';

export default function HabitPanel({ habit, onSave, onArchive }) {
  const [editing, setEditing] = useState(false);
  const [confirming, setConfirming] = useState(false);

  if (editing) {
    return (
      <li className={styles.panel}>
        <HabitForm
          initial={habit}
          submitLabel="Salvar alterações"
          onCancel={() => setEditing(false)}
          onSubmit={async (values) => {
            await onSave(habit.id, values);
            setEditing(false);
          }}
        />
      </li>
    );
  }

  return (
    <li className={styles.panel}>
      <div className={styles.head}>
        <span className={styles.icon} aria-hidden="true">
          {habit.icon}
        </span>
        <div className={styles.title}>
          <h3 className={styles.name}>{habit.name}</h3>
          <div className={styles.tags}>
            <Tag tone="accent">{DIFFICULTY_LABEL[habit.difficulty]} · {habit.xp} XP</Tag>
            <Tag>{scheduleLabel(habit.weekdays)}</Tag>
            {habit.streak > 0 && <Tag tone="xp">🔥 {habit.streak} seguidos</Tag>}
          </div>
        </div>
      </div>

      <dl className={styles.loop}>
        <div>
          <dt>Gatilho</dt>
          <dd>{habit.cue}</dd>
        </div>
        <div>
          <dt>Rotina</dt>
          <dd>{habit.routine}</dd>
        </div>
        <div>
          <dt>Recompensa</dt>
          <dd>{habit.reward}</dd>
        </div>
      </dl>

      <div className={styles.stats}>
        <span>Conclusão (30 dias)</span>
        <strong>{percent(habit.completion_rate)}</strong>
      </div>
      <ProgressBar value={habit.completion_rate * 100} size="sm" label={`Conclusão de ${habit.name}`} />
      <p className={styles.total}>{habit.total_checkins} check-in(s) no total</p>

      <div className={styles.actions}>
        {confirming ? (
          <>
            <span className={styles.confirm}>Arquivar este hábito?</span>
            <Button size="sm" variant="ghost" onClick={() => setConfirming(false)}>
              Não
            </Button>
            <Button size="sm" variant="danger" onClick={() => onArchive(habit)}>
              Sim, arquivar
            </Button>
          </>
        ) : (
          <>
            <Button size="sm" variant="ghost" onClick={() => setConfirming(true)}>
              Arquivar
            </Button>
            <Button size="sm" variant="secondary" onClick={() => setEditing(true)}>
              Editar
            </Button>
          </>
        )}
      </div>
    </li>
  );
}
