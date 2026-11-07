import { api } from '../api/index.js';
import { isDemo } from '../api/index.js';
import { useAuth } from '../context/AuthContext.jsx';
import useResource from '../hooks/useResource.js';
import { Card, Spinner, Tag } from '../components/atoms';
import { InsightCard } from '../components/molecules';
import CoachChat from '../components/organisms/CoachChat/CoachChat.jsx';
import PageHeader from '../components/templates/PageHeader.jsx';
import ErrorState from './ErrorState.jsx';
import styles from './Coach.module.css';

export default function Coach() {
  const { user } = useAuth();
  const { data, error, loading, reload } = useResource(api.insights);

  if (loading) return <Spinner size={32} label="Analisando os seus hábitos" />;
  if (error) return <ErrorState error={error} onRetry={reload} />;

  const mode = data.ai_enabled ? 'IA ativada' : 'Análise por regras';

  return (
    <>
      <PageHeader title="Coach" subtitle="Uma leitura dos seus dados, com sugestões práticas." action={<Tag tone={data.ai_enabled ? 'success' : 'accent'}>{mode}</Tag>} />
      <div className={styles.grid}>
        <Card title="Análise">
          <ul className={styles.insights}>
            {data.insights.map((insight) => (
              <InsightCard key={insight.title} insight={insight} />
            ))}
          </ul>
          {!data.ai_enabled && (
            <p className={styles.note}>
              {isDemo
                ? 'Na demonstração o coach usa só as regras. Rodando o projeto com uma chave da OpenAI (ou o Ollama), a conversa passa a usar IA.'
                : 'Para conversar com IA, defina OPENAI_API_KEY no .env da API. Sem chave, o coach responde pelas regras.'}
            </p>
          )}
        </Card>
        <Card title="Conversa">
          <CoachChat username={user.username} />
        </Card>
      </div>
    </>
  );
}
