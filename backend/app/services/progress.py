from collections import Counter
from datetime import date, timedelta

from sqlmodel import Session, func, select

from app.domain.schedule import global_streak, is_scheduled, parse_weekdays
from app.models import CheckIn, User, XPEvent
from app.schemas import HeatmapDay, ProgressOut, TodayOut, UserOut, XPEventOut
from app.services import badges
from app.services.habits import active_habits, level_out

HEATMAP_DAYS = 84


def summary(session: Session, user: User, today: date) -> ProgressOut:
    days = session.exec(select(CheckIn.day).where(CheckIn.user_id == user.id)).all()
    per_day = Counter(days)
    start = today - timedelta(days=HEATMAP_DAYS - 1)
    heatmap = [
        HeatmapDay(day=start + timedelta(days=offset), count=per_day.get(start + timedelta(days=offset), 0))
        for offset in range(HEATMAP_DAYS)
    ]

    habits = active_habits(session, user)
    done_today = {
        habit_id
        for habit_id in session.exec(
            select(CheckIn.habit_id).where(CheckIn.user_id == user.id, CheckIn.day == today)
        ).all()
    }
    scheduled = [h for h in habits if is_scheduled(parse_weekdays(h.weekdays), today)]

    events = session.exec(select(XPEvent).where(XPEvent.user_id == user.id).order_by(XPEvent.id.desc()).limit(8)).all()
    total = session.exec(select(func.count()).select_from(CheckIn).where(CheckIn.user_id == user.id)).one()

    return ProgressOut(
        user=UserOut.model_validate(user),
        level=level_out(user.total_xp),
        streak=global_streak(set(per_day), today),
        total_checkins=total,
        today=TodayOut(done=sum(1 for h in scheduled if h.id in done_today), scheduled=len(scheduled)),
        heatmap=heatmap,
        badges=badges.all_badges(session, user),
        recent_xp=[XPEventOut(amount=e.amount, reason=e.reason, created_at=e.created_at) for e in events],
    )
