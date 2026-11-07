import { useState } from 'react';
import { api } from '../api/index.js';
import { useToast } from '../context/ToastContext.jsx';
import useResource from '../hooks/useResource.js';
import { Button, Card, Spinner } from '../components/atoms';
import HabitForm from '../components/organisms/HabitForm/HabitForm.jsx';
import HabitPanel from '../components/organisms/HabitPanel/HabitPanel.jsx';
import PageHeader from '../components/templates/PageHeader.jsx';
import ErrorState from './ErrorState.jsx';
import styles from './Habits.module.css';

export default function Habits() {
  const { notify } = useToast();
  const { data: habits, setData, error, loading, reload } = useResource(api.listHabits);
  const [creating, setCreating] = useState(false);

  if (loading) return <Spinner size={32} label="Carregando hábitos" />;
  if (error) return <ErrorState error={error} onRetry={reload} />;

  const showForm = creating || habits.length === 0;

  async function create(values) {
    try {
      const result = await api.createHabit(values);
      setData((list) => [...list, result.habit]);
      setCreating(false);
      notify({ tone: 'info', title: 'Hábito criado', message: `${result.habit.icon} ${result.habit.name}` });
      result.new_badges.forEach((badge) =>
        notify({ tone: 'badge', title: `${badge.icon} Medalha: ${badge.name}`, message: `${badge.description} · +${badge.xp_bonus} XP`, duration: 6000 }),
      );
    } catch (err) {
      notify({ tone: 'error', title: 'Não foi possível criar', message: err.message });
      throw err;
    }
  }

  async function save(id, values) {
    try {
      const updated = await api.updateHabit(id, values);
      setData((list) => list.map((h) => (h.id === id ? updated : h)));
      notify({ tone: 'info', title: 'Alterações salvas', message: `${updated.icon} ${updated.name}` });
    } catch (err) {
      notify({ tone: 'error', title: 'Não foi possível salvar', message: err.message });
      throw err;
    }
  }

  async function archive(habit) {
    try {
      await api.archiveHabit(habit.id);
      setData((list) => list.filter((h) => h.id !== habit.id));
      notify({ tone: 'info', title: 'Hábito arquivado', message: 'O histórico continua guardado.' });
    } catch (err) {
      notify({ tone: 'error', title: 'Não foi possível arquivar', message: err.message });
    }
  }

  return (
    <>
      <PageHeader
        title="Hábitos"
        subtitle="Cada hábito tem um gatilho, uma rotina e uma recompensa."
        action={
          habits.length > 0 && !creating ? (
            <Button onClick={() => setCreating(true)}>+ Novo hábito</Button>
          ) : null
        }
      />

      {showForm && (
        <Card title={habits.length ? 'Novo hábito' : 'Crie o seu primeiro hábito'} className={styles.form}>
          <HabitForm onSubmit={create} onCancel={habits.length ? () => setCreating(false) : undefined} />
        </Card>
      )}

      {habits.length > 0 && (
        <ul className={styles.list}>
          {habits.map((habit) => (
            <HabitPanel key={habit.id} habit={habit} onSave={save} onArchive={archive} />
          ))}
        </ul>
      )}
    </>
  );
}
