import styles from './Tag.module.css';

export default function Tag({ tone = 'neutral', children }) {
  return <span className={`${styles.tag} ${styles[tone]}`}>{children}</span>;
}
