from app.domain.coach import CoachContext, HabitSnapshot, build_insights, detect_intent, rule_based_reply


def snapshot(**overrides) -> HabitSnapshot:
    data = {
        "name": "Correr",
        "icon": "🏃",
        "cue": "Ao acordar",
        "routine": "Correr 20 minutos",
        "streak": 0,
        "rate_7": 0.9,
        "scheduled_7": 7,
        "rate_30": 0.9,
        "scheduled_30": 30,
        "scheduled_today": True,
        "done_today": True,
    }
    data.update(overrides)
    return HabitSnapshot(**data)


def context(*habits: HabitSnapshot, streak: int = 0) -> CoachContext:
    return CoachContext(username="braga", level=2, total_xp=150, streak=streak, habits=list(habits))


def test_empty_context_suggests_starting_small() -> None:
    insights = build_insights(context())
    assert insights[0].title == "Comece pequeno"


def test_detects_habit_at_risk() -> None:
    insights = build_insights(context(snapshot(rate_7=0.2)))
    assert insights[0].kind == "alerta"
    assert "Correr" in insights[0].title


def test_highlights_strong_habit_and_streak() -> None:
    kinds = {i.kind for i in build_insights(context(snapshot(), streak=5))}
    assert {"destaque", "sequencia"} <= kinds


def test_intents() -> None:
    assert detect_intent("Oi!") == "saudacao"
    assert detect_intent("Como estou indo?") == "progresso"
    assert detect_intent("Não consigo manter a corrida") == "dificuldade"
    assert detect_intent("Estou desanimado") == "motivacao"
    assert detect_intent("Me dá uma dica") == "dica"


def test_reply_uses_user_data() -> None:
    reply = rule_based_reply("não consigo", context(snapshot(rate_7=0.1)))
    assert "Correr" in reply and "Ao acordar" in reply
