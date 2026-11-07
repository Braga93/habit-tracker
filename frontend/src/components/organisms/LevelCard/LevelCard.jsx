import { Card, ProgressBar } from '../../atoms';
import styles from './LevelCard.module.css';

export default function LevelCard({ level }) {
  return (
    <Card className={styles.card} aria-label="Nível e experiência">
      <div className={styles.top}>
        <div className={styles.badge}>
          <span className={styles.number}>{level.level}</span>
          <span className={styles.caption}>nível</span>
        </div>
        <div className={styles.text}>
          <p className={styles.xp}>{level.total_xp} XP no total</p>
          <p className={styles.next}>
            {level.needed - level.current} XP para o nível {level.level + 1}
          </p>
        </div>
      </div>
      <ProgressBar value={level.percent} tone="xp" label={`Progresso para o nível ${level.level + 1}`} />
      <p className={styles.range}>
        {level.current} / {level.needed} XP
      </p>
    </Card>
  );
}
