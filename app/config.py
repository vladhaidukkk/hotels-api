from typing import Literal

from pydantic import BaseModel, Field, PostgresDsn, RedisDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvSettings(BaseSettings):
    mode: Literal["prod", "dev", "test"]
    debug: bool = False
    # For Celery & Pytest, it must be set to `True`.
    null_pool: bool = False

    model_config = SettingsConfigDict(env_ignore_empty=True, extra="ignore")


class DatabaseSettings(BaseModel):
    host: str
    port: int = Field(ge=1, le=65535)
    user: str
    password: str | None = None
    name: str

    @computed_field
    def url(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            path=self.name,
        ).unicode_string()


class RedisSettings(BaseModel):
    host: str
    port: int = Field(ge=1, le=65535)

    @computed_field
    def url(self) -> RedisDsn:
        return RedisDsn.build(
            scheme="redis",
            host=self.host,
            port=self.port,
        ).unicode_string()


class SmtpSettings(BaseModel):
    host: str
    port: int
    user: str
    # Specify if you want to send emails from a real user.
    password: str | None = None
    # Specify if you want to hardcode the receiver (useful for development & testing).
    receiver: str | None = None


class SentrySettings(BaseModel):
    dsn: str | None = None
    enabled: bool = False


class JwtSettings(BaseModel):
    secret_key: str
    algorithm: str
    access_token_exp_mins: int


class AppSettings(BaseSettings):
    db: DatabaseSettings
    redis: RedisSettings
    smtp: SmtpSettings
    sentry: SentrySettings
    jwt: JwtSettings

    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_ignore_empty=True,
        extra="ignore",
    )


class Settings:
    def __init__(self) -> None:
        self._env_file = ".env"
        self.env = EnvSettings(_env_file=self._env_file)
        self._app_env_prefix = "test__app__" if self.env.mode == "test" else "app__"
        self.app = AppSettings(
            _env_file=self._env_file, _env_prefix=self._app_env_prefix
        )


settings = Settings()
print(settings.env, settings.app)
