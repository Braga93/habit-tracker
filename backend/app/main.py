from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import create_tables
from app.routers import auth, coach, habits, progress


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    create_tables()
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="Habit Tracker API",
        description="Hábitos no ciclo gatilho, rotina e recompensa, com XP, medalhas e um coach.",
        version="2.0.0",
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    for router in (auth.router, habits.router, progress.router, coach.router):
        app.include_router(router, prefix="/api")

    @app.get("/api/health", tags=["sistema"])
    def health() -> dict[str, object]:
        return {"status": "ok", "ai_enabled": settings.ai_enabled}

    return app


app = create_app()
