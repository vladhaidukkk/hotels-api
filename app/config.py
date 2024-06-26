from pydantic import Extra, Field, PostgresDsn, RedisDsn, computed_field
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

    # For Celery set it to True, but only for Celery.
    null_pool: bool = False

    jwt_secret_key: str
    jwt_algorithm: str
    jwt_access_token_expire_minutes: int

    redis_host: str
    redis_port: int

    @computed_field
    def redis_url(self) -> str:
        dsn = RedisDsn.build(
            scheme="redis",
            host=self.redis_host,
            port=self.redis_port,
        )
        return dsn.unicode_string()

    smtp_host: str
    smtp_port: int
    smtp_user: str
    # Specify password for production. For local development, I'd recommend to proceed without it.
    smtp_pass: str | None = None
    # Specify it if you want to hardcode receiver for testing.
    smtp_receiver: str | None = None

    model_config = SettingsConfigDict(env_file=".env", extra=Extra.ignore)


settings = Settings()  # type: ignore
