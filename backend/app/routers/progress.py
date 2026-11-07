from fastapi import APIRouter

from app.deps import CurrentUser, SessionDep, Today
from app.schemas import ProgressOut
from app.services import progress

router = APIRouter(prefix="/progress", tags=["progresso"])


@router.get("", response_model=ProgressOut)
def get_progress(user: CurrentUser, session: SessionDep, today: Today) -> ProgressOut:
    return progress.summary(session, user, today)
