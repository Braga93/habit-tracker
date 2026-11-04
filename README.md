# Habit Tracker AI

Aplicativo web para criar hábitos e mantê-los, com XP, níveis, medalhas e um coach de inteligência artificial. Foi feito inteiramente em Python, com o framework [Reflex](https://reflex.dev/).

A ideia de cada hábito segue o ciclo **gatilho → rotina → recompensa**: você define o que dispara o hábito, o que faz e como se recompensa.

## Funcionalidades

- **Hábitos com gatilho, rotina e recompensa**, com frequência e meta de dias
- **XP e níveis:** cada check-in rende XP, e o nível sobe conforme o XP acumulado
- **Sequências (streaks)** global e por hábito, com bônus de XP em marcos
- **7 medalhas** desbloqueadas automaticamente: First Step, 3-Day Streak, 7-Day Streak, 30-Day Streak, Century Club, Level 5 e Habit Master
- **Mapa de atividade (heatmap)** com os dias em que você cumpriu seus hábitos
- **Coach de IA:** chat com respostas em tempo real, análise de padrões dos seus hábitos e previsão de risco de abandono
- **Login e cadastro**, com a senha guardada em hash (veja [Segurança](#segurança))

## Telas

| Rota | Tela |
|---|---|
| `/` | Início |
| `/login` e `/register` | Entrar e criar conta |
| `/dashboard` | Painel com XP, sequência e hábitos do dia |
| `/habits` | Gerenciar hábitos |
| `/coach` | Conversa com o coach de IA |
| `/profile` | Perfil, nível e medalhas |

## Tecnologias

- Python 3.11
- [Reflex](https://reflex.dev/) 0.7 (interface e backend, tudo em Python)
- SQLModel e SQLite
- API da OpenAI (modelo padrão `gpt-4o-mini`), ou qualquer serviço compatível, como o Ollama local
- Docker e Docker Compose

## Como rodar

### Pré-requisitos

- Python 3.11 ou superior
- Node.js 20 ou superior (o Reflex usa para montar a interface)
- Git

### Rodando localmente

```bash
git clone https://github.com/Braga93/habit-tracker.git
cd habit-tracker

python -m venv .venv
source .venv/bin/activate        # no Windows: .venv\Scripts\activate

pip install -r requirements.txt
cp .env.example .env             # no Windows: copy .env.example .env

reflex init
reflex run
```

Abra `http://localhost:3000`. O banco de dados (`habit_tracker.db`) é criado sozinho na primeira execução.

### Com Docker

```bash
cp .env.example .env
docker compose up --build
```

A interface fica em `http://localhost:3000` e o backend em `http://localhost:8000`.

### Coach de IA

Para usar o coach, coloque a sua chave no arquivo `.env`:

```text
OPENAI_API_KEY=sua_chave_aqui
```

Sem a chave, o resto do aplicativo funciona normalmente. Só o coach de IA fica indisponível.

| Variável | Descrição | Padrão |
|---|---|---|
| `OPENAI_API_KEY` | Chave da API | vazia |
| `LLM_MODEL` | Modelo usado pelo coach | `gpt-4o-mini` |
| `OPENAI_BASE_URL` | Endereço da API (troque para usar o Ollama) | `https://api.openai.com/v1` |

## Estrutura

```text
habit-tracker/
├── habit_tracker/
│   ├── habit_tracker.py     montagem do app, rotas e criação das tabelas
│   ├── pages/               as telas
│   ├── components/          barra de XP, cartão de hábito, medalhas, chat, mapa de atividade
│   ├── state/               estado das telas (login, hábitos, gamificação, IA)
│   ├── services/            regras de negócio (hábitos, XP e medalhas, coach de IA)
│   ├── models/              tabelas do banco (usuário, hábito, registro, medalha)
│   └── styles/              tema visual
├── docs/PLANO.md            plano de arquitetura do projeto (em inglês)
├── rxconfig.py              configuração do Reflex
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env.example             modelo das variáveis de ambiente
```

## Segurança

- O arquivo `.env` (com a sua chave de API) e o banco de dados local ficam fora do Git, no `.gitignore`.
- Nunca envie chaves ou o arquivo `.db` para o repositório.
- As senhas são guardadas com SHA-256 simples, sem sal. Isso serve para um projeto de estudo, mas não para produção: em um uso real, o ideal é trocar por `bcrypt` ou `argon2`.

## Autor

**Eduardo Braga**, estudante de desenvolvimento full-stack em Fortaleza, CE.
[LinkedIn](https://www.linkedin.com/in/eduardo-braga-6131b9253/) · [GitHub](https://github.com/Braga93)
