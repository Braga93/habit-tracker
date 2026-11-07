import { useCallback, useState } from 'react';
import { api } from '../api/index.js';
import { useToast } from '../context/ToastContext.jsx';

export default function useCheckIn(onChange) {
  const { notify } = useToast();
  const [busyId, setBusyId] = useState(null);

  const toggle = useCallback(
    async (habit) => {
      setBusyId(habit.id);
      try {
        if (habit.done_today) {
          const updated = await api.undoCheckIn(habit.id);
          notify({ tone: 'info', title: 'Check-in desfeito', message: `${habit.icon} ${habit.name}` });
          await onChange?.(updated);
          return;
        }
        const result = await api.checkIn(habit.id);
        notify({ tone: 'xp', title: `+${result.xp_gained} XP`, message: `${habit.icon} ${habit.name} concluído` });
        if (result.streak_bonus) {
          notify({ tone: 'xp', title: `Bônus de ${result.streak} dias!`, message: `+${result.streak_bonus} XP pela sequência` });
        }
        result.new_badges.forEach((badge) =>
          notify({ tone: 'badge', title: `${badge.icon} Medalha: ${badge.name}`, message: `${badge.description} · +${badge.xp_bonus} XP`, duration: 6000 }),
        );
        if (result.leveled_up) {
          notify({ tone: 'level', title: `Nível ${result.level.level}!`, message: 'Você subiu de nível. Continue assim.', duration: 6000 });
        }
        await onChange?.(result.habit);
      } catch (err) {
        notify({ tone: 'error', title: 'Não deu certo', message: err.message });
      } finally {
        setBusyId(null);
      }
    },
    [notify, onChange],
  );

  return { toggle, busyId };
}
