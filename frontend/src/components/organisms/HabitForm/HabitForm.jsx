import { useState } from 'react';
import { Button, Input } from '../../atoms';
import { ChoiceGroup, WeekdayPicker } from '../../molecules';
import styles from './HabitForm.module.css';

const ICONS = ['🎯', '📚', '🏃', '💧', '🧘', '🥗', '💤', '✍️', '🎸', '💻', '🧹', '🌱'];
const DIFFICULTIES = [
  { value: 'easy', label: 'Fácil · 10 XP' },
  { value: 'medium', label: 'Médio · 20 XP' },
  { value: 'hard', label: 'Difícil · 30 XP' },
];
const EMPTY = { name: '', cue: '', routine: '', reward: '', icon: '🎯', difficulty: 'medium', weekdays: [0, 1, 2, 3, 4, 5, 6] };

export default function HabitForm({ initial, onSubmit, onCancel, submitLabel = 'Criar hábito' }) {
  const [values, setValues] = useState(() => ({ ...EMPTY, ...initial }));
  const [errors, setErrors] = useState({});
  const [saving, setSaving] = useState(false);

  const set = (field) => (event) => setValues((v) => ({ ...v, [field]: event.target.value }));

  async function submit(event) {
    event.preventDefault();
    const missing = {};
    ['name', 'cue', 'routine', 'reward'].forEach((field) => {
      if (!values[field].trim()) missing[field] = 'Preencha este campo.';
    });
    setErrors(missing);
    if (Object.keys(missing).length) return;
    setSaving(true);
    try {
      await onSubmit(values);
      if (!initial) setValues(EMPTY);
    } finally {
      setSaving(false);
    }
  }

  return (
    <form className={styles.form} onSubmit={submit} noValidate>
      <ChoiceGroup
        legend="Ícone"
        compact
        value={values.icon}
        onChange={(icon) => setValues((v) => ({ ...v, icon }))}
        options={ICONS.map((icon) => ({ value: icon, label: icon, ariaLabel: `Ícone ${icon}` }))}
      />
      <Input label="Nome do hábito" placeholder="Ex.: Ler" maxLength={80} value={values.name} onChange={set('name')} error={errors.name} />
      <div className={styles.loop}>
        <Input label="Gatilho" hint="O que dispara o hábito?" placeholder="Depois do café da manhã" maxLength={200} value={values.cue} onChange={set('cue')} error={errors.cue} />
        <Input label="Rotina" hint="O que você vai fazer?" placeholder="Ler 10 páginas" maxLength={200} value={values.routine} onChange={set('routine')} error={errors.routine} />
        <Input label="Recompensa" hint="Como vai se recompensar?" placeholder="Um chá com calma" maxLength={200} value={values.reward} onChange={set('reward')} error={errors.reward} />
      </div>
      <ChoiceGroup legend="Dificuldade" value={values.difficulty} onChange={(difficulty) => setValues((v) => ({ ...v, difficulty }))} options={DIFFICULTIES} />
      <WeekdayPicker value={values.weekdays} onChange={(weekdays) => setValues((v) => ({ ...v, weekdays }))} />
      <div className={styles.actions}>
        {onCancel && (
          <Button variant="ghost" onClick={onCancel}>
            Cancelar
          </Button>
        )}
        <Button type="submit" loading={saving}>
          {submitLabel}
        </Button>
      </div>
    </form>
  );
}
