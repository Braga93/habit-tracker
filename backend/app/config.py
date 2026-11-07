from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    database_url: str = "sqlite:///./habit_tracker.db"
    secret_key: str = "troque-esta-chave-em-producao"
    token_expire_minutes: int = 60 * 24 * 7
    cors_origins: str = "http://localhost:5173"

    openai_api_key: str = ""
    openai_base_url: str = "https://api.openai.com/v1"
    llm_model: str = "gpt-4o-mini"
    llm_timeout_seconds: float = 20.0

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def ai_enabled(self) -> bool:
        return bool(self.openai_api_key.strip())


@lru_cache
def get_settings() -> Settings:
    return Settings()
