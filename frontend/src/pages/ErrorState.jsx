import { Button, Card } from '../components/atoms';

export default function ErrorState({ error, onRetry }) {
  return (
    <Card role="alert" style={{ textAlign: 'center' }}>
      <p style={{ fontSize: '2rem' }} aria-hidden="true">
        ⚠️
      </p>
      <p style={{ fontWeight: 700, margin: '8px 0 4px' }}>Não foi possível carregar</p>
      <p style={{ color: 'var(--text-soft)', marginBottom: 16 }}>{error.message}</p>
      <Button variant="secondary" onClick={onRetry}>
        Tentar de novo
      </Button>
    </Card>
  );
}
