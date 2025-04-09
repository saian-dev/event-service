from pathlib import Path

from pydantic import Field, PostgresDsn

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_dsn: PostgresDsn = Field(..., validation_alias="database_url")
    echo_sql: bool = Field(False)

    model_config = SettingsConfigDict(env_file=Path(__file__).parent.parent.parent / ".env")

    @property
    def database_url(self) -> str:
        return self.database_dsn.unicode_string()


settings = Settings()
