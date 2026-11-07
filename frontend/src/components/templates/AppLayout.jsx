import { Outlet } from 'react-router-dom';
import { isDemo } from '../../api/index.js';
import NavBar from '../organisms/NavBar/NavBar.jsx';
import DemoBanner from '../organisms/DemoBanner/DemoBanner.jsx';
import styles from './AppLayout.module.css';

export default function AppLayout() {
  return (
    <>
      {isDemo && <DemoBanner />}
      <NavBar />
      <main className={styles.main}>
        <Outlet />
      </main>
    </>
  );
}
