import { useState } from 'react';
import { resetDemo } from '../../../api/demo.js';
import styles from './DemoBanner.module.css';

export default function DemoBanner() {
  const [resetting, setResetting] = useState(false);
  return (
    <div className={styles.banner} role="note">
      <span>
        <strong>Modo demonstração.</strong> Os dados ficam só neste navegador. O projeto completo tem API em FastAPI.
      </span>
      <button
        type="button"
        className={styles.reset}
        disabled={resetting}
        onClick={() => {
          setResetting(true);
          resetDemo();
          window.location.reload();
        }}
      >
        Recomeçar demo
      </button>
    </div>
  );
}
