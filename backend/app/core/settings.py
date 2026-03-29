from functools import lru_cache
from typing import Annotated

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class Settings(BaseSettings):
    api_host: str = Field(default="0.0.0.0", alias="API_HOST")
    api_port: int = Field(default=8000, alias="API_PORT")
    cors_allow_origins: Annotated[list[str], NoDecode] = Field(
        default_factory=lambda: ["http://localhost:3000"],
        alias="CORS_ALLOW_ORIGINS",
    )
    environment: str = Field(default="local", alias="ENVIRONMENT")
    supabase_url: str | None = Field(default=None, alias="SUPABASE_URL")
    supabase_anon_key: str | None = Field(default=None, alias="SUPABASE_ANON_KEY")
    supabase_service_role_key: str | None = Field(
        default=None,
        alias="SUPABASE_SERVICE_ROLE_KEY",
    )
    supabase_db_url: str | None = Field(default=None, alias="SUPABASE_DB_URL")
    storage_bucket_raw_inputs: str = Field(
        default="accounting-mvp-raw-inputs",
        alias="STORAGE_BUCKET_RAW_INPUTS",
    )
    storage_bucket_run_exports: str = Field(
        default="accounting-mvp-run-exports",
        alias="STORAGE_BUCKET_RUN_EXPORTS",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    @field_validator("cors_allow_origins", mode="before")
    @classmethod
    def split_origins(cls, value: object) -> object:
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]

        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()
