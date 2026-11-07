import { useId } from 'react';
import styles from './Input.module.css';

export default function Input({ label, hint, error, as = 'input', className = '', ...props }) {
  const id = useId();
  const Field = as;
  const describedBy = [hint && `${id}-hint`, error && `${id}-error`].filter(Boolean).join(' ') || undefined;
  return (
    <div className={`${styles.field} ${className}`}>
      <label htmlFor={id} className={styles.label}>
        {label}
      </label>
      <Field id={id} className={`${styles.input} ${error ? styles.invalid : ''}`} aria-invalid={Boolean(error)} aria-describedby={describedBy} {...props} />
      {hint && !error && (
        <p id={`${id}-hint`} className={styles.hint}>
          {hint}
        </p>
      )}
      {error && (
        <p id={`${id}-error`} className={styles.error} role="alert">
          {error}
        </p>
      )}
    </div>
  );
}
