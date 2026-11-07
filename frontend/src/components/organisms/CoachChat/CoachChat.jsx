import { useEffect, useRef, useState } from 'react';
import { api } from '../../../api/index.js';
import { Button } from '../../atoms';
import { ChatBubble } from '../../molecules';
import styles from './CoachChat.module.css';

const SUGGESTIONS = ['Como estou?', 'Me dá uma dica', 'Não consigo manter um hábito', 'Estou desanimado'];

export default function CoachChat({ username }) {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: `Oi, ${username}! Sou o seu coach. Pergunte sobre o seu progresso ou peça uma dica.` },
  ]);
  const [text, setText] = useState('');
  const [sending, setSending] = useState(false);
  const listRef = useRef(null);

  useEffect(() => {
    const list = listRef.current;
    if (list) list.scrollTop = list.scrollHeight;
  }, [messages, sending]);

  async function send(message) {
    const content = message.trim();
    if (!content || sending) return;
    const history = messages.slice(1).map(({ role, content: c }) => ({ role, content: c }));
    setMessages((list) => [...list, { role: 'user', content }]);
    setText('');
    setSending(true);
    try {
      const answer = await api.chat({ message: content, history });
      setMessages((list) => [
        ...list,
        { role: 'assistant', content: answer.reply, meta: answer.notice ?? (answer.source === 'ia' ? 'Resposta da IA' : 'Análise por regras') },
      ]);
    } catch (err) {
      setMessages((list) => [...list, { role: 'assistant', content: err.message, meta: 'Erro' }]);
    } finally {
      setSending(false);
    }
  }

  return (
    <div className={styles.chat}>
      <ul ref={listRef} className={styles.messages} aria-live="polite" aria-label="Conversa com o coach">
        {messages.map((message, index) => (
          <ChatBubble key={index} role={message.role} meta={message.meta}>
            {message.content}
          </ChatBubble>
        ))}
        {sending && (
          <ChatBubble role="assistant">
            <span className={styles.typing}>pensando</span>
          </ChatBubble>
        )}
      </ul>
      <div className={styles.suggestions}>
        {SUGGESTIONS.map((suggestion) => (
          <button key={suggestion} type="button" className={styles.suggestion} onClick={() => send(suggestion)} disabled={sending}>
            {suggestion}
          </button>
        ))}
      </div>
      <form
        className={styles.form}
        onSubmit={(event) => {
          event.preventDefault();
          send(text);
        }}
      >
        <label htmlFor="mensagem-coach" className="visually-hidden">
          Mensagem para o coach
        </label>
        <input
          id="mensagem-coach"
          className={styles.input}
          value={text}
          onChange={(event) => setText(event.target.value)}
          placeholder="Escreva para o coach..."
          maxLength={500}
          autoComplete="off"
        />
        <Button type="submit" disabled={!text.trim()} loading={sending}>
          Enviar
        </Button>
      </form>
    </div>
  );
}
