import { Link } from 'react-router-dom';
import Spinner from '../Spinner/Spinner.jsx';
import styles from './Button.module.css';

export default function Button({ variant = 'primary', size = 'md', to, loading = false, block = false, className = '', children, ...props }) {
  const classes = [styles.button, styles[variant], styles[size], block && styles.block, className].filter(Boolean).join(' ');
  if (to) {
    return (
      <Link to={to} className={classes} {...props}>
        {children}
      </Link>
    );
  }
  return (
    <button type="button" className={classes} disabled={loading || props.disabled} aria-busy={loading || undefined} {...props}>
      {loading && <Spinner size={16} />}
      {children}
    </button>
  );
}
