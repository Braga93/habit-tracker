import { STREAK_BONUSES } from './rewards.js';

const WEEKDAY_NAMES = ['segunda-feira', 'terça-feira', 'quarta-feira', 'quinta-feira', 'sexta-feira', 'sábado', 'domingo'];

const pct = (value) => Math.round(value * 100);

export function atRisk(context) {
  return context.habits.filter((h) => h.scheduled_7 >= 2 && h.rate_7 < 0.5).sort((a, b) => a.rate_7 - b.rate_7);
}

export function pendingToday(context) {
  return context.habits.filter((h) => h.scheduled_today && !h.done_today);
}

export function nextBonus(streak) {
  const milestone = Object.keys(STREAK_BONUSES)
    .map(Number)
    .sort((a, b) => a - b)
    .find((m) => m > streak);
  return milestone ? { milestone, remaining: milestone - streak } : null;
}

export function buildInsights(context) {
  if (!context.habits.length) {
    return [
      {
        kind: 'dica',
        title: 'Comece pequeno',
        message: 'Crie um hábito tão fácil que seja impossível falhar, como ler uma página ou beber um copo de água ao acordar.',
      },
    ];
  }

  const insights = [];

  atRisk(context)
    .slice(0, 2)
    .forEach((habit) => {
      insights.push({
        kind: 'alerta',
        title: `${habit.icon} ${habit.name} está em risco`,
        message:
          `Você cumpriu ${pct(habit.rate_7)}% dos dias agendados nesta semana. ` +
          `Que tal reduzir a rotina para uma versão de 2 minutos e prender ao gatilho "${habit.cue}"?`,
      });
    });

  const strong = context.habits.filter((h) => h.scheduled_30 >= 3 && h.rate_30 >= 0.7);
  if (strong.length) {
    const best = strong.reduce((a, b) => (b.rate_30 > a.rate_30 || (b.rate_30 === a.rate_30 && b.streak > a.streak) ? b : a));
    insights.push({
      kind: 'destaque',
      title: `${best.icon} ${best.name} é o seu ponto forte`,
      message: `${pct(best.rate_30)}% de conclusão no último mês. Use-o como âncora: faça um hábito novo logo depois dele.`,
    });
  }

  if (context.streak >= 2) {
    const bonus = nextBonus(context.streak);
    const extra = bonus ? ` Faltam ${bonus.remaining} dia(s) para o bônus de ${bonus.milestone} dias.` : '';
    insights.push({ kind: 'sequencia', title: `${context.streak} dias seguidos`, message: `Sua sequência está viva.${extra}` });
  }

  const pending = pendingToday(context);
  if (pending.length) {
    const names = pending
      .slice(0, 3)
      .map((h) => `${h.icon} ${h.name}`)
      .join(', ');
    insights.push({ kind: 'dica', title: 'Ainda dá tempo hoje', message: `Faltam ${pending.length} hábito(s) hoje: ${names}.` });
  }

  const counts = context.checkins_by_weekday;
  const total = Object.values(counts).reduce((s, n) => s + n, 0);
  if (total >= 5) {
    const bestDay = Object.keys(counts).reduce((a, b) => (counts[b] > counts[a] ? b : a));
    insights.push({
      kind: 'destaque',
      title: 'Seu dia mais forte',
      message: `Você faz mais check-ins na ${WEEKDAY_NAMES[bestDay]}. Planeje os hábitos mais difíceis para esse dia.`,
    });
  }

  if (!insights.length) {
    insights.push({ kind: 'dica', title: 'Tudo em dia', message: 'Nenhum hábito em risco. Continue registrando para eu achar padrões.' });
  }
  return insights;
}

function normalize(text) {
  return text
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '');
}

const INTENTS = {
  saudacao: ['oi', 'ola', 'bom dia', 'boa tarde', 'boa noite', 'e ai'],
  progresso: ['progresso', 'como estou', 'nivel', 'xp', 'resumo', 'status', 'medalha'],
  dificuldade: ['dificil', 'nao consigo', 'desisti', 'preguica', 'falhei', 'esqueci', 'risco', 'atrasad'],
  motivacao: ['motiv', 'desanim', 'cansad', 'triste', 'vontade', 'animo'],
  dica: ['dica', 'sugest', 'ajuda', 'como faco', 'melhorar', 'conselho', 'ideia'],
};

export function detectIntent(message) {
  const text = normalize(message);
  for (const intent of ['dificuldade', 'motivacao', 'progresso', 'dica', 'saudacao']) {
    if (INTENTS[intent].some((keyword) => text.includes(keyword))) return intent;
  }
  return 'geral';
}

function summary(context) {
  const pending = pendingToday(context);
  const today = pending.length ? `Faltam ${pending.length} hábito(s) hoje.` : 'Hoje está tudo feito.';
  return `Você está no nível ${context.level}, com ${context.total_xp} XP e ${context.streak} dia(s) seguidos. ${today}`;
}

export function ruleBasedReply(message, context) {
  const intent = detectIntent(message);
  const risks = atRisk(context);

  if (!context.habits.length) {
    return 'Você ainda não tem hábitos. Comece por um bem pequeno, com um gatilho claro: "depois de escovar os dentes, vou alongar por 2 minutos".';
  }
  if (intent === 'saudacao') {
    return `Olá, ${context.username}! ${summary(context)} Pergunte sobre o seu progresso ou peça uma dica.`;
  }
  if (intent === 'progresso') {
    const bonus = nextBonus(context.streak);
    return summary(context) + (bonus ? ` Faltam ${bonus.remaining} dia(s) para o próximo bônus de sequência.` : '');
  }
  if (intent === 'dificuldade') {
    if (risks.length) {
      const habit = risks[0];
      return (
        `Normal travar. ${habit.icon} ${habit.name} está com ${pct(habit.rate_7)}% nesta semana. ` +
        `Diminua a meta: faça só a primeira parte de "${habit.routine}" logo depois de "${habit.cue}". ` +
        'Feito pela metade ainda conta para a sequência.'
      );
    }
    return 'Quando ficar difícil, reduza o hábito até caber em 2 minutos. O importante é não quebrar a corrente.';
  }
  if (intent === 'motivacao') {
    if (context.streak) {
      return `Você já tem ${context.streak} dia(s) seguidos. Não precisa ser perfeito hoje, só precisa aparecer.`;
    }
    return 'Todo recomeço conta. Escolha o hábito mais fácil da lista e faça agora: a vitória pequena puxa as próximas.';
  }
  if (intent === 'dica') {
    return buildInsights(context)
      .slice(0, 2)
      .map((i) => `${i.title}: ${i.message}`)
      .join(' ');
  }
  return 'Posso analisar o seu progresso, apontar hábitos em risco e sugerir ajustes. Experimente perguntar "como estou?" ou "me dá uma dica".';
}
