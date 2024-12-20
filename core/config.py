from pathlib import Path
from typing import Literal

from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent
LOG_DEFAULT_FORMAT = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)


class RunConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000


class GunicornConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8001
    workers: int = 1
    timeout: int = 900


class LoggingConfig(BaseModel):
    log_level: Literal[
        "debug",
        "info",
        "warning",
        "error",
        "critical",
    ] = "info"
    log_format: str = LOG_DEFAULT_FORMAT


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    tasks: str = "/tasks"
    categories: str = "/categories"
    auth: str = "/auth"
    users: str = "/users"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class Project(BaseModel):
    name: str = "Pomodoro-time Service"
    version: str = "0.1.0"
    description: str = "Test service for fastapi practice"


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class AuthJWTConfig(BaseModel):
    private_key_path: Path = BASE_DIR / "cert" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "cert" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 5
    refresh_token_expire_days: int = 10


class CeleryConfig(BaseModel):
    broker_url: str = "redis://localhost:6379/0"
    result_backend: str = "redis://localhost:6379/0"


class BrokerConfig(BaseModel):
    url: str = "redis://localhost:6379/0"
    mail_queue: str
    callback_mail_queue: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.dev",),
        # env_file=(".env",),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    mode: str = "DEV"
    run: RunConfig = RunConfig()
    gunicorn: GunicornConfig = GunicornConfig()
    logging: LoggingConfig = LoggingConfig()
    api: ApiPrefix = ApiPrefix()
    project: Project = Project()
    db: DatabaseConfig
    auth_jwt: AuthJWTConfig
    celery: CeleryConfig
    broker: BrokerConfig


settings = Settings()
