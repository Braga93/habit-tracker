from typing import Annotated

from fastapi import APIRouter, Depends

from app.config import Settings, get_settings
from app.deps import CurrentUser, SessionDep, Today
from app.schemas import ChatIn, ChatOut, InsightsOut
from app.services import coach

router = APIRouter(prefix="/coach", tags=["coach"])

SettingsDep = Annotated[Settings, Depends(get_settings)]


@router.get("/insights", response_model=InsightsOut)
def get_insights(user: CurrentUser, session: SessionDep, today: Today, settings: SettingsDep) -> InsightsOut:
    return coach.insights(session, user, today, settings)


@router.post("/chat", response_model=ChatOut)
async def chat(data: ChatIn, user: CurrentUser, session: SessionDep, today: Today, settings: SettingsDep) -> ChatOut:
    return await coach.chat(session, user, data, today, settings)
