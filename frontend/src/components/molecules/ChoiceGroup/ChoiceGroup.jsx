import styles from './ChoiceGroup.module.css';

export default function ChoiceGroup({ legend, options, value, onChange, compact = false }) {
  return (
    <fieldset className={styles.fieldset}>
      <legend className={styles.legend}>{legend}</legend>
      <div className={`${styles.options} ${compact ? styles.compact : ''}`}>
        {options.map((option) => (
          <button
            key={option.value}
            type="button"
            className={styles.option}
            aria-pressed={value === option.value}
            aria-label={option.ariaLabel}
            onClick={() => onChange(option.value)}
          >
            {option.label}
          </button>
        ))}
      </div>
    </fieldset>
  );
}
