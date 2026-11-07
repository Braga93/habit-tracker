import os
from collections.abc import Iterator
from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

os.environ["DATABASE_URL"] = "sqlite://"

from app.config import Settings, get_settings
from app.database import get_session
from app.deps import get_today
from app.main import create_app


class Clock:
    def __init__(self, today: date) -> None:
        self.today = today


@pytest.fixture
def clock() -> Clock:
    return Clock(date(2026, 3, 2))


@pytest.fixture
def engine():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)
    yield engine
    engine.dispose()


@pytest.fixture
def settings() -> Settings:
    return Settings(openai_api_key="", secret_key="chave-de-teste")


@pytest.fixture
def client(engine, clock: Clock, settings: Settings) -> Iterator[TestClient]:
    app = create_app()

    def session_override() -> Iterator[Session]:
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = session_override
    app.dependency_overrides[get_today] = lambda: clock.today
    app.dependency_overrides[get_settings] = lambda: settings
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def auth(client: TestClient) -> dict[str, str]:
    response = client.post(
        "/api/auth/register",
        json={"username": "braga", "email": "braga@exemplo.com", "password": "senha-segura"},
    )
    assert response.status_code == 201
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


@pytest.fixture
def habit_payload() -> dict:
    return {
        "name": "Ler",
        "cue": "Depois do café",
        "routine": "Ler 10 páginas",
        "reward": "Um chá",
        "icon": "📚",
        "difficulty": "medium",
        "weekdays": [0, 1, 2, 3, 4, 5, 6],
    }
