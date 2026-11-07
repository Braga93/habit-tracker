import { api } from '../api/index.js';
import useResource from '../hooks/useResource.js';
import { Card, Spinner } from '../components/atoms';
import LevelCard from '../components/organisms/LevelCard/LevelCard.jsx';
import BadgeGrid from '../components/organisms/BadgeGrid/BadgeGrid.jsx';
import PageHeader from '../components/templates/PageHeader.jsx';
import ErrorState from './ErrorState.jsx';
import { shortDate } from '../utils/format.js';
import styles from './Profile.module.css';

export default function Profile() {
  const { data, error, loading, reload } = useResource(api.progress);

  if (loading) return <Spinner size={32} label="Carregando o perfil" />;
  if (error) return <ErrorState error={error} onRetry={reload} />;

  const earned = data.badges.filter((b) => b.earned).length;

  return (
    <>
      <PageHeader title={`@${data.user.username}`} subtitle={`Membro desde ${shortDate(data.user.created_at)} · ${data.user.email}`} />
      <div className={styles.grid}>
        <div className={styles.side}>
          <LevelCard level={data.level} />
          <Card title="Últimos ganhos de XP">
            {data.recent_xp.length ? (
              <ul className={styles.history}>
                {data.recent_xp.map((event, index) => (
                  <li key={index} className={styles.event}>
                    <span>{event.reason}</span>
                    <strong className={event.amount < 0 ? styles.negative : styles.positive}>
                      {event.amount > 0 ? '+' : ''}
                      {event.amount} XP
                    </strong>
                  </li>
                ))}
              </ul>
            ) : (
              <p className={styles.empty}>Nada por aqui ainda.</p>
            )}
          </Card>
        </div>
        <Card title={`Medalhas · ${earned} de ${data.badges.length}`}>
          <BadgeGrid badges={data.badges} />
        </Card>
      </div>
    </>
  );
}
