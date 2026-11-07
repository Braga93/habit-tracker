from datetime import date
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import Session

from app.database import get_session
from app.models import User
from app.security import decode_access_token

bearer = HTTPBearer(auto_error=False)


def get_today() -> date:
    return date.today()


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)],
    session: Annotated[Session, Depends(get_session)],
) -> User:
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Sessão inválida ou expirada. Entre novamente.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if credentials is None:
        raise unauthorized
    user_id = decode_access_token(credentials.credentials)
    user = session.get(User, user_id) if user_id else None
    if user is None:
        raise unauthorized
    return user


SessionDep = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
Today = Annotated[date, Depends(get_today)]
