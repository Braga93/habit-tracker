import { useCallback } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../api/index.js';
import { useAuth } from '../context/AuthContext.jsx';
import useResource from '../hooks/useResource.js';
import useCheckIn from '../hooks/useCheckIn.js';
import { Card, Spinner } from '../components/atoms';
import { InsightCard, StatCard } from '../components/molecules';
import LevelCard from '../components/organisms/LevelCard/LevelCard.jsx';
import TodayList from '../components/organisms/TodayList/TodayList.jsx';
import Heatmap from '../components/organisms/Heatmap/Heatmap.jsx';
import PageHeader from '../components/templates/PageHeader.jsx';
import ErrorState from './ErrorState.jsx';
import { greeting } from '../utils/format.js';
import styles from './Dashboard.module.css';

async function loadDashboard() {
  const [habits, progress, coach] = await Promise.all([api.listHabits(), api.progress(), api.insights()]);
  return { habits, progress, insights: coach.insights };
}

export default function Dashboard() {
  const { user } = useAuth();
  const { data, error, loading, reload } = useResource(loadDashboard);
  const refresh = useCallback(() => reload(), [reload]);
  const { toggle, busyId } = useCheckIn(refresh);

  if (loading) return <Spinner size={32} label="Carregando o painel" />;
  if (error) return <ErrorState error={error} onRetry={reload} />;

  const { habits, progress, insights } = data;
  const earned = progress.badges.filter((b) => b.earned).length;

  return (
    <>
      <PageHeader title={`${greeting()}, ${user.username}!`} subtitle="Estes são os seus hábitos de hoje." />

      <div className={styles.stats}>
        <StatCard icon="🔥" label="dias seguidos" value={progress.streak} tone="xp" />
        <StatCard icon="✅" label="feitos hoje" value={`${progress.today.done}/${progress.today.scheduled}`} tone="success" />
        <StatCard icon="📈" label="check-ins no total" value={progress.total_checkins} />
        <StatCard icon="🏅" label="medalhas" value={`${earned}/${progress.badges.length}`} tone="xp" />
      </div>

      <div className={styles.grid}>
        <Card title="Hoje" className={styles.today}>
          <TodayList habits={habits} busyId={busyId} onToggle={toggle} />
        </Card>

        <div className={styles.side}>
          <LevelCard level={progress.level} />
          <Card title="Coach" action={<Link className={styles.more} to="/coach">Ver tudo</Link>}>
            <ul className={styles.insights}>
              {insights.slice(0, 2).map((insight) => (
                <InsightCard key={insight.title} insight={insight} />
              ))}
            </ul>
          </Card>
        </div>

        <Card title="Últimas 12 semanas" className={styles.heatmap}>
          <Heatmap days={progress.heatmap} />
        </Card>
      </div>
    </>
  );
}
