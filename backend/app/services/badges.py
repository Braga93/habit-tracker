from datetime import date

from sqlmodel import Session, func, select

from app.domain.badges import BADGES, BADGES_BY_CODE, Badge, BadgeStats, newly_unlocked
from app.domain.levels import level_from_xp
from app.domain.schedule import global_streak
from app.models import CheckIn, Habit, User, UserBadge
from app.schemas import BadgeOut
from app.services import xp


def _active_days(session: Session, user: User) -> set[date]:
    return set(session.exec(select(CheckIn.day).where(CheckIn.user_id == user.id).distinct()).all())


def gather_stats(session: Session, user: User, today: date) -> BadgeStats:
    habits = session.exec(select(func.count()).select_from(Habit).where(Habit.user_id == user.id)).one()
    checkins = session.exec(select(func.count()).select_from(CheckIn).where(CheckIn.user_id == user.id)).one()
    return BadgeStats(
        habits_created=habits,
        checkins=checkins,
        streak=global_streak(_active_days(session, user), today),
        level=level_from_xp(user.total_xp),
    )


def earned_badges(session: Session, user: User) -> dict[str, UserBadge]:
    rows = session.exec(select(UserBadge).where(UserBadge.user_id == user.id)).all()
    return {row.code: row for row in rows}


def evaluate(session: Session, user: User, today: date) -> list[Badge]:
    session.flush()
    earned = set(earned_badges(session, user))
    unlocked: list[Badge] = []
    while True:
        new = newly_unlocked(gather_stats(session, user, today), earned)
        if not new:
            return unlocked
        for badge in new:
            session.add(UserBadge(user_id=user.id, code=badge.code))
            xp.award(session, user, badge.xp_bonus, f"Medalha: {badge.name}")
            earned.add(badge.code)
            unlocked.append(badge)
        session.flush()


def to_out(badge: Badge, earned: UserBadge | None = None) -> BadgeOut:
    return BadgeOut(
        code=badge.code,
        name=badge.name,
        description=badge.description,
        icon=badge.icon,
        xp_bonus=badge.xp_bonus,
        earned=earned is not None,
        earned_at=earned.earned_at if earned else None,
    )


def all_badges(session: Session, user: User) -> list[BadgeOut]:
    earned = earned_badges(session, user)
    return [to_out(badge, earned.get(badge.code)) for badge in BADGES]


def describe(codes: list[Badge]) -> list[BadgeOut]:
    return [to_out(BADGES_BY_CODE[badge.code]) for badge in codes]
