import { shortDate } from '../../../utils/format.js';
import styles from './BadgeItem.module.css';

export default function BadgeItem({ badge }) {
  return (
    <li className={`${styles.badge} ${badge.earned ? styles.earned : styles.locked}`}>
      <span className={styles.icon} aria-hidden="true">
        {badge.earned ? badge.icon : '🔒'}
      </span>
      <p className={styles.name}>{badge.name}</p>
      <p className={styles.description}>{badge.description}</p>
      <p className={styles.footer}>{badge.earned ? `Conquistada em ${shortDate(badge.earned_at)}` : `+${badge.xp_bonus} XP`}</p>
      <span className="visually-hidden">{badge.earned ? 'Conquistada' : 'Bloqueada'}</span>
    </li>
  );
}
