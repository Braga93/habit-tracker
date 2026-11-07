import styles from './Toaster.module.css';

export default function Toaster({ toasts, onDismiss }) {
  return (
    <div className={styles.region} role="status" aria-live="polite">
      {toasts.map((toast) => (
        <div key={toast.id} className={`${styles.toast} ${styles[toast.tone] ?? ''}`}>
          <div>
            <p className={styles.title}>{toast.title}</p>
            {toast.message && <p className={styles.message}>{toast.message}</p>}
          </div>
          <button type="button" className={styles.close} onClick={() => onDismiss(toast.id)} aria-label="Fechar aviso">
            ×
          </button>
        </div>
      ))}
    </div>
  );
}
