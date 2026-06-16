from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from src.config.domain.interface import IConfig


class Settings(BaseSettings):
    env: str = "dev"
    app_name: str = "waslini"
    api_version: str = "1"
    port: int = 8000

    db_host: str = "localhost"
    db_port: int = 5432
    db_user: str = "postgres"
    db_password: str = "postgres"
    db_name: str = "waslini"

    logs_dirname: str = "logs"
    retention_days: int = Field(30, alias="RENTENTION_DAYS")

    jwt_access_token_secret: str = "your_access_token_secret"
    jwt_refresh_token_secret: str = "your_refresh_token_secret"
    jwt_access_token_expiry: int = 3600
    jwt_refresh_token_expiry: int = 604800
    jwt_algo: str = "HS256"

    cookies_secure: bool = False
    cookies_same_site: str = "lax"
    cors_origins: list[str] = ["*"]
    cors_credentials: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )


class ConfigAdapter(IConfig):
    def __init__(self, env_file: str | None = None):
        kwargs = {}
        if env_file:
            kwargs["_env_file"] = env_file
        self._settings = Settings(**kwargs)

    @property
    def env(self) -> str:
        return self._settings.env

    @property
    def app_name(self) -> str:
        return self._settings.app_name

    @property
    def api_version(self) -> str:
        return self._settings.api_version

    @property
    def port(self) -> int:
        return self._settings.port

    @property
    def db_host(self) -> str:
        return self._settings.db_host

    @property
    def db_port(self) -> int:
        return self._settings.db_port

    @property
    def db_user(self) -> str:
        return self._settings.db_user

    @property
    def db_password(self) -> str:
        return self._settings.db_password

    @property
    def db_name(self) -> str:
        return self._settings.db_name

    @property
    def logs_dirname(self) -> str:
        return self._settings.logs_dirname

    @property
    def retention_days(self) -> int:
        return self._settings.retention_days

    @property
    def jwt_access_token_secret(self) -> str:
        return self._settings.jwt_access_token_secret

    @property
    def jwt_refresh_token_secret(self) -> str:
        return self._settings.jwt_refresh_token_secret

    @property
    def jwt_access_token_expiry(self) -> int:
        return self._settings.jwt_access_token_expiry

    @property
    def jwt_refresh_token_expiry(self) -> int:
        return self._settings.jwt_refresh_token_expiry

    @property
    def jwt_algo(self) -> str:
        return self._settings.jwt_algo

    @property
    def cookies_secure(self) -> bool:
        return self._settings.cookies_secure

    @property
    def cookies_same_site(self) -> str:
        return self._settings.cookies_same_site

    @property
    def cors_origins(self) -> list[str]:
        return self._settings.cors_origins

    @property
    def cors_credentials(self) -> bool:
        return self._settings.cors_credentials

    @property
    def database_url(self) -> str:
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    @property
    def async_database_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    @property
    def jwt_secret(self) -> str:
        return self.jwt_access_token_secret

    @property
    def debug(self) -> bool:
        return self.env == "dev"
