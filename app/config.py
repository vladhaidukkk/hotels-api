from pydantic import Extra, Field, PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_host: str
    db_port: int = Field(ge=1, le=65535)
    db_user: str
    db_pass: str
    db_name: str

    @computed_field
    def db_url(self) -> str:
        dsn = PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.db_user,
            password=self.db_pass,
            host=str(self.db_host),
            port=self.db_port,
            path=self.db_name,
        )
        return dsn.unicode_string()

    model_config = SettingsConfigDict(env_file=".env", extra=Extra.ignore)


settings = Settings()  # type: ignore
