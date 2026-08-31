from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    llm_provider: str = "mock"
    groq_api_key: str | None = None
    groq_model: str = "llama-3.1-8b-instant"
    gemini_api_key: str | None = None
    gemini_model: str = "gemini-2.5-flash"
    supabase_db_url: str | None = None
    embedding_dimension: int = 384
    top_k: int = 5


@lru_cache
def get_settings() -> Settings:
    return Settings()
