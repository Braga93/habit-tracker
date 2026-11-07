import { Button } from '../components/atoms';
import AuthLayout from '../components/templates/AuthLayout.jsx';

export default function NotFound() {
  return (
    <AuthLayout title="Página não encontrada" subtitle="Esse endereço não existe.">
      <Button to="/" block>
        Voltar ao início
      </Button>
    </AuthLayout>
  );
}
