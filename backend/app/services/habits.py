from collections import defaultdict
from datetime import date

from fastapi import HTTPException, status
from sqlmodel import Session, col, select

from app.domain.levels import level_from_xp, level_progress
from app.domain.rewards import streak_bonus, xp_for_difficulty
from app.domain.schedule import (
    completion_rate,
    format_weekdays,
    global_streak,
    habit_streak,
    is_scheduled,
    parse_weekdays,
)
from app.models import CheckIn, Habit, User
from app.schemas import CheckInIn, CheckInResult, HabitCreated, HabitIn, HabitOut, HabitUpdate, LevelOut
from app.services import badges, xp


def level_out(total_xp: int) -> LevelOut:
    progress = level_progress(total_xp)
    return LevelOut(
        level=progress.level,
        total_xp=progress.total_xp,
        current=progress.current,
        needed=progress.needed,
        percent=progress.percent,
    )


def to_out(habit: Habit, done: set[date], today: date) -> HabitOut:
    weekdays = parse_weekdays(habit.weekdays)
    return HabitOut(
        id=habit.id,
        name=habit.name,
        cue=habit.cue,
        routine=habit.routine,
        reward=habit.reward,
        icon=habit.icon,
        difficulty=habit.difficulty,
        xp=xp_for_difficulty(habit.difficulty),
        weekdays=list(weekdays),
        created_on=habit.created_on,
        streak=habit_streak(done, weekdays, today, habit.created_on),
        completion_rate=completion_rate(done, weekdays, today, habit.created_on),
        total_checkins=len(done),
        scheduled_today=is_scheduled(weekdays, today),
        done_today=today in done,
    )


def checkin_days_by_habit(session: Session, user: User) -> dict[int, set[date]]:
    rows = session.exec(select(CheckIn.habit_id, CheckIn.day).where(CheckIn.user_id == user.id)).all()
    days: dict[int, set[date]] = defaultdict(set)
    for habit_id, day in rows:
        days[habit_id].add(day)
    return days


def active_habits(session: Session, user: User) -> list[Habit]:
    statement = select(Habit).where(Habit.user_id == user.id, col(Habit.archived).is_(False)).order_by(Habit.id)
    return list(session.exec(statement).all())


def list_habits(session: Session, user: User, today: date) -> list[HabitOut]:
    days = checkin_days_by_habit(session, user)
    return [to_out(habit, days.get(habit.id, set()), today) for habit in active_habits(session, user)]


def get_owned(session: Session, user: User, habit_id: int) -> Habit:
    habit = session.get(Habit, habit_id)
    if habit is None or habit.user_id != user.id or habit.archived:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hábito não encontrado.")
    return habit


def habit_days(session: Session, habit: Habit) -> set[date]:
    return set(session.exec(select(CheckIn.day).where(CheckIn.habit_id == habit.id)).all())


def create(session: Session, user: User, data: HabitIn, today: date) -> HabitCreated:
    habit = Habit(
        user_id=user.id,
        name=data.name.strip(),
        cue=data.cue.strip(),
        routine=data.routine.strip(),
        reward=data.reward.strip(),
        icon=data.icon,
        difficulty=data.difficulty,
        weekdays=format_weekdays(data.weekdays),
        created_on=today,
    )
    session.add(habit)
    unlocked = badges.evaluate(session, user, today)
    session.commit()
    session.refresh(habit)
    return HabitCreated(habit=to_out(habit, set(), today), new_badges=badges.describe(unlocked))


def update(session: Session, user: User, habit_id: int, data: HabitUpdate, today: date) -> HabitOut:
    habit = get_owned(session, user, habit_id)
    changes = data.model_dump(exclude_unset=True, exclude_none=True)
    if "weekdays" in changes:
        changes["weekdays"] = format_weekdays(changes["weekdays"])
    for field, value in changes.items():
        setattr(habit, field, value.strip() if isinstance(value, str) and field != "icon" else value)
    session.add(habit)
    session.commit()
    session.refresh(habit)
    return to_out(habit, habit_days(session, habit), today)


def archive(session: Session, user: User, habit_id: int) -> None:
    habit = get_owned(session, user, habit_id)
    habit.archived = True
    session.add(habit)
    session.commit()


def _user_active_days(session: Session, user: User) -> set[date]:
    return set(session.exec(select(CheckIn.day).where(CheckIn.user_id == user.id).distinct()).all())


def check_in(session: Session, user: User, habit_id: int, data: CheckInIn, today: date) -> CheckInResult:
    habit = get_owned(session, user, habit_id)
    if today in habit_days(session, habit):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Este hábito já foi registrado hoje.")

    level_before = level_from_xp(user.total_xp)
    first_of_day = today not in _user_active_days(session, user)

    gained = xp_for_difficulty(habit.difficulty)
    checkin = CheckIn(
        user_id=user.id,
        habit_id=habit.id,
        day=today,
        mood=data.mood,
        note=data.note.strip() if data.note else None,
        xp_earned=gained,
    )
    session.add(checkin)
    xp.award(session, user, gained, f"Check-in: {habit.name}")
    session.flush()

    streak = global_streak(_user_active_days(session, user), today)
    bonus = streak_bonus(streak) if first_of_day else 0
    if bonus:
        xp.award(session, user, bonus, f"Bônus de {streak} dias seguidos")
        checkin.xp_earned += bonus
        session.add(checkin)

    unlocked = badges.evaluate(session, user, today)
    session.commit()
    session.refresh(user)

    return CheckInResult(
        habit=to_out(habit, habit_days(session, habit), today),
        xp_gained=gained,
        streak_bonus=bonus,
        streak=streak,
        new_badges=badges.describe(unlocked),
        level=level_out(user.total_xp),
        leveled_up=level_from_xp(user.total_xp) > level_before,
    )


def undo_check_in(session: Session, user: User, habit_id: int, today: date) -> HabitOut:
    habit = get_owned(session, user, habit_id)
    checkin = session.exec(select(CheckIn).where(CheckIn.habit_id == habit.id, CheckIn.day == today)).first()
    if checkin is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Não há registro de hoje para desfazer.")
    xp.revoke(session, user, checkin.xp_earned, f"Check-in desfeito: {habit.name}")
    session.delete(checkin)
    session.commit()
    return to_out(habit, habit_days(session, habit), today)
