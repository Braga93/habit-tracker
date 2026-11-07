from fastapi import APIRouter, HTTPException, status
from sqlmodel import or_, select

from app.deps import CurrentUser, SessionDep
from app.models import User
from app.schemas import LoginIn, RegisterIn, TokenOut, UserOut
from app.security import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["autenticação"])


def token_for(user: User) -> TokenOut:
    return TokenOut(access_token=create_access_token(user.id), user=UserOut.model_validate(user))


@router.post("/register", response_model=TokenOut, status_code=status.HTTP_201_CREATED)
def register(data: RegisterIn, session: SessionDep) -> TokenOut:
    username_taken = session.exec(select(User).where(User.username == data.username)).first()
    if username_taken:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Este nome de usuário já está em uso.")
    email_taken = session.exec(select(User).where(User.email == data.email)).first()
    if email_taken:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Já existe uma conta com este e-mail.")

    user = User(username=data.username, email=data.email, password_hash=hash_password(data.password))
    session.add(user)
    session.commit()
    session.refresh(user)
    return token_for(user)


@router.post("/login", response_model=TokenOut)
def login(data: LoginIn, session: SessionDep) -> TokenOut:
    identifier = data.username.strip()
    user = session.exec(select(User).where(or_(User.username == identifier, User.email == identifier.lower()))).first()
    if user is None or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário ou senha incorretos.")
    return token_for(user)


@router.get("/me", response_model=UserOut)
def me(user: CurrentUser) -> User:
    return user
