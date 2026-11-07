import styles from './Card.module.css';

export default function Card({ as: Tag = 'section', title, action, className = '', children, ...props }) {
  return (
    <Tag className={`${styles.card} ${className}`} {...props}>
      {(title || action) && (
        <header className={styles.header}>
          {title && <h2 className={styles.title}>{title}</h2>}
          {action}
        </header>
      )}
      {children}
    </Tag>
  );
}
