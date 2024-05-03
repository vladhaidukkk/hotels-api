from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Extra


class Settings(BaseSettings):
    db_host: str
    db_port: int
    db_user: str
    db_pass: str
    db_name: str

    @property
    def db_url(self):
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.db_pass}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    model_config = SettingsConfigDict(env_file=".env", extra=Extra.ignore)


settings = Settings()  # type: ignore
