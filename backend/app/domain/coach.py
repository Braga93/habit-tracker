import unicodedata
from dataclasses import dataclass, field

from app.domain.rewards import STREAK_BONUSES

WEEKDAY_NAMES = ("segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira", "sábado", "domingo")


@dataclass(frozen=True)
class HabitSnapshot:
    name: str
    icon: str
    cue: str
    routine: str
    streak: int
    rate_7: float
    scheduled_7: int
    rate_30: float
    scheduled_30: int
    scheduled_today: bool
    done_today: bool


@dataclass(frozen=True)
class CoachContext:
    username: str
    level: int
    total_xp: int
    streak: int
    habits: list[HabitSnapshot] = field(default_factory=list)
    checkins_by_weekday: dict[int, int] = field(default_factory=dict)


@dataclass(frozen=True)
class Insight:
    kind: str
    title: str
    message: str


def at_risk(context: CoachContext) -> list[HabitSnapshot]:
    return sorted(
        (h for h in context.habits if h.scheduled_7 >= 2 and h.rate_7 < 0.5),
        key=lambda h: h.rate_7,
    )


def pending_today(context: CoachContext) -> list[HabitSnapshot]:
    return [h for h in context.habits if h.scheduled_today and not h.done_today]


def next_bonus(streak: int) -> tuple[int, int] | None:
    for milestone in sorted(STREAK_BONUSES):
        if milestone > streak:
            return milestone, milestone - streak
    return None


def build_insights(context: CoachContext) -> list[Insight]:
    if not context.habits:
        return [
            Insight(
                "dica",
                "Comece pequeno",
                "Crie um hábito tão fácil que seja impossível falhar, "
                "como ler uma página ou beber um copo de água ao acordar.",
            )
        ]

    insights: list[Insight] = []

    for habit in at_risk(context)[:2]:
        insights.append(
            Insight(
                "alerta",
                f"{habit.icon} {habit.name} está em risco",
                f"Você cumpriu {round(habit.rate_7 * 100)}% dos dias agendados nesta semana. "
                f'Que tal reduzir a rotina para uma versão de 2 minutos e prender ao gatilho "{habit.cue}"?',
            )
        )

    strong = [h for h in context.habits if h.scheduled_30 >= 3 and h.rate_30 >= 0.7]
    if strong:
        best = max(strong, key=lambda h: (h.rate_30, h.streak))
        insights.append(
            Insight(
                "destaque",
                f"{best.icon} {best.name} é o seu ponto forte",
                f"{round(best.rate_30 * 100)}% de conclusão no último mês. Use-o como âncora: "
                "faça um hábito novo logo depois dele.",
            )
        )

    if context.streak >= 2:
        bonus = next_bonus(context.streak)
        extra = f" Faltam {bonus[1]} dia(s) para o bônus de {bonus[0]} dias." if bonus else ""
        insights.append(Insight("sequencia", f"{context.streak} dias seguidos", f"Sua sequência está viva.{extra}"))

    pending = pending_today(context)
    if pending:
        names = ", ".join(f"{h.icon} {h.name}" for h in pending[:3])
        insights.append(Insight("dica", "Ainda dá tempo hoje", f"Faltam {len(pending)} hábito(s) hoje: {names}."))

    total = sum(context.checkins_by_weekday.values())
    if total >= 5:
        best_day = max(context.checkins_by_weekday, key=context.checkins_by_weekday.get)
        insights.append(
            Insight(
                "destaque",
                "Seu dia mais forte",
                f"Você faz mais check-ins na {WEEKDAY_NAMES[best_day]}. "
                "Planeje os hábitos mais difíceis para esse dia.",
            )
        )

    if not insights:
        insights.append(
            Insight("dica", "Tudo em dia", "Nenhum hábito em risco. Continue registrando para eu achar padrões.")
        )
    return insights


def _normalize(text: str) -> str:
    decomposed = unicodedata.normalize("NFD", text.lower())
    return "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")


INTENTS = {
    "saudacao": ("oi", "ola", "bom dia", "boa tarde", "boa noite", "e ai"),
    "progresso": ("progresso", "como estou", "nivel", "xp", "resumo", "status", "medalha"),
    "dificuldade": ("dificil", "nao consigo", "desisti", "preguica", "falhei", "esqueci", "risco", "atrasad"),
    "motivacao": ("motiv", "desanim", "cansad", "triste", "vontade", "animo"),
    "dica": ("dica", "sugest", "ajuda", "como faco", "melhorar", "conselho", "ideia"),
}


def detect_intent(message: str) -> str:
    text = _normalize(message)
    for intent in ("dificuldade", "motivacao", "progresso", "dica", "saudacao"):
        if any(keyword in text for keyword in INTENTS[intent]):
            return intent
    return "geral"


def _summary(context: CoachContext) -> str:
    pending = pending_today(context)
    today = f"Faltam {len(pending)} hábito(s) hoje." if pending else "Hoje está tudo feito."
    return f"Você está no nível {context.level}, com {context.total_xp} XP e {context.streak} dia(s) seguidos. {today}"


def rule_based_reply(message: str, context: CoachContext) -> str:
    intent = detect_intent(message)
    risks = at_risk(context)

    if not context.habits:
        return (
            "Você ainda não tem hábitos. Comece por um bem pequeno, com um gatilho claro: "
            '"depois de escovar os dentes, vou alongar por 2 minutos".'
        )

    if intent == "saudacao":
        return f"Olá, {context.username}! {_summary(context)} Pergunte sobre o seu progresso ou peça uma dica."

    if intent == "progresso":
        bonus = next_bonus(context.streak)
        extra = f" Faltam {bonus[1]} dia(s) para o próximo bônus de sequência." if bonus else ""
        return _summary(context) + extra

    if intent == "dificuldade":
        if risks:
            habit = risks[0]
            return (
                f"Normal travar. {habit.icon} {habit.name} está com {round(habit.rate_7 * 100)}% nesta semana. "
                f'Diminua a meta: faça só a primeira parte de "{habit.routine}" logo depois de "{habit.cue}". '
                "Feito pela metade ainda conta para a sequência."
            )
        return "Quando ficar difícil, reduza o hábito até caber em 2 minutos. O importante é não quebrar a corrente."

    if intent == "motivacao":
        if context.streak:
            return f"Você já tem {context.streak} dia(s) seguidos. Não precisa ser perfeito hoje, só precisa aparecer."
        return (
            "Todo recomeço conta. Escolha o hábito mais fácil da lista e faça agora: "
            "a vitória pequena puxa as próximas."
        )

    if intent == "dica":
        insights = build_insights(context)
        return " ".join(f"{i.title}: {i.message}" for i in insights[:2])

    return (
        "Posso analisar o seu progresso, apontar hábitos em risco e sugerir ajustes. "
        'Experimente perguntar "como estou?" ou "me dá uma dica".'
    )
