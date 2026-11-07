import styles from './ChatBubble.module.css';

export default function ChatBubble({ role, children, meta }) {
  return (
    <li className={`${styles.row} ${role === 'user' ? styles.user : styles.coach}`}>
      <div className={styles.bubble}>
        <span className="visually-hidden">{role === 'user' ? 'Você disse:' : 'Coach disse:'}</span>
        {children}
      </div>
      {meta && <p className={styles.meta}>{meta}</p>}
    </li>
  );
}
