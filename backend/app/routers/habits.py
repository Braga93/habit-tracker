from fastapi import APIRouter, status

from app.deps import CurrentUser, SessionDep, Today
from app.schemas import CheckInIn, CheckInResult, HabitCreated, HabitIn, HabitOut, HabitUpdate
from app.services import habits

router = APIRouter(prefix="/habits", tags=["hábitos"])


@router.get("", response_model=list[HabitOut])
def list_habits(user: CurrentUser, session: SessionDep, today: Today) -> list[HabitOut]:
    return habits.list_habits(session, user, today)


@router.post("", response_model=HabitCreated, status_code=status.HTTP_201_CREATED)
def create_habit(data: HabitIn, user: CurrentUser, session: SessionDep, today: Today) -> HabitCreated:
    return habits.create(session, user, data, today)


@router.patch("/{habit_id}", response_model=HabitOut)
def update_habit(habit_id: int, data: HabitUpdate, user: CurrentUser, session: SessionDep, today: Today) -> HabitOut:
    return habits.update(session, user, habit_id, data, today)


@router.delete("/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
def archive_habit(habit_id: int, user: CurrentUser, session: SessionDep) -> None:
    habits.archive(session, user, habit_id)


@router.post("/{habit_id}/checkins", response_model=CheckInResult, status_code=status.HTTP_201_CREATED)
def check_in(
    habit_id: int, user: CurrentUser, session: SessionDep, today: Today, data: CheckInIn | None = None
) -> CheckInResult:
    return habits.check_in(session, user, habit_id, data or CheckInIn(), today)


@router.delete("/{habit_id}/checkins/today", response_model=HabitOut)
def undo_check_in(habit_id: int, user: CurrentUser, session: SessionDep, today: Today) -> HabitOut:
    return habits.undo_check_in(session, user, habit_id, today)
