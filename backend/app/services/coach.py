import json
from collections import Counter
from datetime import date, timedelta

import httpx
from sqlmodel import Session, select

from app.config import Settings
from app.domain.coach import CoachContext, HabitSnapshot, build_insights, rule_based_reply
from app.domain.levels import level_from_xp
from app.domain.schedule import completion, global_streak, habit_streak, is_scheduled, parse_weekdays
from app.models import CheckIn, User
from app.schemas import ChatIn, ChatOut, InsightOut, InsightsOut
from app.services.habits import active_habits, checkin_days_by_habit

SYSTEM_PROMPT = (
    "Você é um coach de hábitos que fala português do Brasil. Use o ciclo gatilho, rotina e recompensa "
    "e princípios de psicologia positiva. Responda de forma curta (até 120 palavras), prática e encorajadora, "
    "sempre baseada nos dados do usuário. Nunca invente dados que não estão no contexto."
)


def build_context(session: Session, user: User, today: date) -> CoachContext:
    days_by_habit = checkin_days_by_habit(session, user)
    snapshots = []
    for habit in active_habits(session, user):
        done = days_by_habit.get(habit.id, set())
        weekdays = parse_weekdays(habit.weekdays)
        week = completion(done, weekdays, today, habit.created_on, window_days=7)
        month = completion(done, weekdays, today, habit.created_on, window_days=30)
        snapshots.append(
            HabitSnapshot(
                name=habit.name,
                icon=habit.icon,
                cue=habit.cue,
                routine=habit.routine,
                streak=habit_streak(done, weekdays, today, habit.created_on),
                rate_7=week.rate,
                scheduled_7=week.scheduled,
                rate_30=month.rate,
                scheduled_30=month.scheduled,
                scheduled_today=is_scheduled(weekdays, today),
                done_today=today in done,
            )
        )

    since = today - timedelta(days=55)
    recent = session.exec(select(CheckIn.day).where(CheckIn.user_id == user.id, CheckIn.day >= since)).all()
    all_days = set(session.exec(select(CheckIn.day).where(CheckIn.user_id == user.id)).all())

    return CoachContext(
        username=user.username,
        level=level_from_xp(user.total_xp),
        total_xp=user.total_xp,
        streak=global_streak(all_days, today),
        habits=snapshots,
        checkins_by_weekday=dict(Counter(day.weekday() for day in recent)),
    )


def insights(session: Session, user: User, today: date, settings: Settings) -> InsightsOut:
    context = build_context(session, user, today)
    return InsightsOut(
        insights=[InsightOut(kind=i.kind, title=i.title, message=i.message) for i in build_insights(context)],
        ai_enabled=settings.ai_enabled,
    )


def _context_for_ai(context: CoachContext) -> str:
    data = {
        "usuario": context.username,
        "nivel": context.level,
        "xp_total": context.total_xp,
        "dias_seguidos": context.streak,
        "habitos": [
            {
                "nome": h.name,
                "gatilho": h.cue,
                "rotina": h.routine,
                "sequencia": h.streak,
                "conclusao_7_dias": h.rate_7,
                "conclusao_30_dias": h.rate_30,
                "feito_hoje": h.done_today,
                "agendado_hoje": h.scheduled_today,
            }
            for h in context.habits
        ],
    }
    return json.dumps(data, ensure_ascii=False)


async def ask_ai(context: CoachContext, data: ChatIn, settings: Settings) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "system", "content": f"Dados do usuário: {_context_for_ai(context)}"},
        *[{"role": m.role, "content": m.content} for m in data.history[-10:]],
        {"role": "user", "content": data.message},
    ]
    async with httpx.AsyncClient(timeout=settings.llm_timeout_seconds) as client:
        response = await client.post(
            f"{settings.openai_base_url.rstrip('/')}/chat/completions",
            headers={"Authorization": f"Bearer {settings.openai_api_key}"},
            json={"model": settings.llm_model, "messages": messages, "max_tokens": 300, "temperature": 0.7},
        )
        response.raise_for_status()
        reply = response.json()["choices"][0]["message"]["content"]
    if not reply or not reply.strip():
        raise ValueError("Resposta vazia da IA")
    return reply.strip()


async def chat(session: Session, user: User, data: ChatIn, today: date, settings: Settings) -> ChatOut:
    context = build_context(session, user, today)
    if settings.ai_enabled:
        try:
            return ChatOut(reply=await ask_ai(context, data, settings), source="ia")
        except (httpx.HTTPError, KeyError, IndexError, ValueError):
            return ChatOut(
                reply=rule_based_reply(data.message, context),
                source="regras",
                notice="A IA não respondeu agora. Esta resposta veio da análise por regras.",
            )
    return ChatOut(reply=rule_based_reply(data.message, context), source="regras")
