import { BadgeItem } from '../../molecules';
import styles from './BadgeGrid.module.css';

export default function BadgeGrid({ badges }) {
  return (
    <ul className={styles.grid}>
      {badges.map((badge) => (
        <BadgeItem key={badge.code} badge={badge} />
      ))}
    </ul>
  );
}
