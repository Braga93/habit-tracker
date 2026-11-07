import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { isDemo } from '../api/index.js';
import { DEMO_PASSWORD, DEMO_USERNAME } from '../api/demo.js';
import { useAuth } from '../context/AuthContext.jsx';
import { Button } from '../components/atoms';
import styles from './Landing.module.css';

const STEPS = [
  { icon: '⚡', title: 'Gatilho', text: 'O que dispara o hábito: "depois do café".' },
  { icon: '🔁', title: 'Rotina', text: 'A ação em si: "ler 10 páginas".' },
  { icon: '🎁', title: 'Recompensa', text: 'O que fecha o ciclo: "um chá com calma".' },
];

const FEATURES = [
  { icon: '✨', title: 'XP e níveis', text: 'Cada check-in rende XP pela dificuldade do hábito, com bônus em 7, 14, 30, 60 e 100 dias seguidos.' },
  { icon: '🏅', title: 'Medalhas', text: 'Oito conquistas, de criar o primeiro hábito a completar 500 check-ins.' },
  { icon: '🔥', title: 'Sequências justas', text: 'Contam só os dias agendados e não zeram enquanto o dia de hoje ainda está em aberto.' },
  { icon: '🧠', title: 'Coach', text: 'Aponta hábitos em risco e seu dia mais forte. Com uma chave de IA, também conversa.' },
];

export default function Landing() {
  const { user, login } = useAuth();
  const navigate = useNavigate();
  const [entering, setEntering] = useState(false);

  async function enterDemo() {
    setEntering(true);
    try {
      await login({ username: DEMO_USERNAME, password: DEMO_PASSWORD });
      navigate('/painel');
    } finally {
      setEntering(false);
    }
  }

  return (
    <div className={styles.page}>
      <header className={styles.top}>
        <span className={styles.brand}>
          <span aria-hidden="true">🎯</span> Habit Tracker
        </span>
        {user ? (
          <Button to="/painel" size="sm" variant="secondary">
            Ir para o painel
          </Button>
        ) : (
          <Button to="/entrar" size="sm" variant="secondary">
            Entrar
          </Button>
        )}
      </header>

      <main>
        <section className={styles.hero} aria-labelledby="titulo">
          <p className={styles.eyebrow}>Gatilho → Rotina → Recompensa</p>
          <h1 id="titulo" className={styles.title}>
            Hábitos que viram <span>rotina</span>.
          </h1>
          <p className={styles.lead}>
            Monte cada hábito no ciclo que a ciência usa para explicar como eles se formam, ganhe XP a cada check-in e receba
            dicas de um coach que lê os seus dados.
          </p>
          <div className={styles.actions}>
            {user ? (
              <Button to="/painel" size="lg">
                Continuar
              </Button>
            ) : isDemo ? (
              <Button size="lg" onClick={enterDemo} loading={entering}>
                Ver demonstração
              </Button>
            ) : (
              <Button to="/criar-conta" size="lg">
                Criar conta grátis
              </Button>
            )}
            <a className={styles.code} href="https://github.com/Braga93/habit-tracker" target="_blank" rel="noreferrer">
              Ver o código no GitHub
            </a>
          </div>
        </section>

        <section className={styles.loop} aria-label="O ciclo do hábito">
          {STEPS.map((step, index) => (
            <div key={step.title} className={styles.step}>
              <span className={styles.stepIcon} aria-hidden="true">
                {step.icon}
              </span>
              <h2 className={styles.stepTitle}>
                {index + 1}. {step.title}
              </h2>
              <p>{step.text}</p>
            </div>
          ))}
        </section>

        <section className={styles.features} aria-labelledby="recursos">
          <h2 id="recursos" className={styles.sectionTitle}>
            O que tem dentro
          </h2>
          <ul className={styles.grid}>
            {FEATURES.map((feature) => (
              <li key={feature.title} className={styles.feature}>
                <span aria-hidden="true">{feature.icon}</span>
                <h3>{feature.title}</h3>
                <p>{feature.text}</p>
              </li>
            ))}
          </ul>
        </section>
      </main>

      <footer className={styles.footer}>
        Feito por <Link to="/">Eduardo Braga</Link> · React, FastAPI e SQLite
      </footer>
    </div>
  );
}
