import secrets
import warnings
from typing import Annotated, Any, Literal, List

from pydantic import (
    AnyUrl,
    BeforeValidator,
    HttpUrl,
    PostgresDsn,
    computed_field,
    model_validator,
    Field
)
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Self


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    DOMAIN: str = Field("local", env="DOMAIN")
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    ENV_SERVER: str = Field("NEREUS-SERVER", env="ENV_SERVER")

    @computed_field  # type: ignore[misc]
    @property
    def server_host(self) -> str:
        # Use HTTPS for anything other than local development
        if self.ENVIRONMENT == "local":
            return f"http://{self.DOMAIN}"
        return f"https://{self.DOMAIN}"

    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    PROJECT_NAME: str
    SENTRY_DSN: HttpUrl | None = None
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str = ""
    CELERY_RESULT_BACKEND: str = Field("teste123", env="CELERY_RESULT_BACKEND")
    CELERY_BROKER_URL: str = Field("teste123", env="CELERY_BROKER_URL")
    ENV_WORKER: str = Field("ATLA_TASK", env="ENV_WORKER")
    MEGA_SERVER_URL: str = Field("MEGA_SERVER_URL", env="MEGA_SERVER_URL")
    MEGA_DEFAULT_CREDENTIALS: str = Field("MEGA_DEFAULT_CREDENTIALS", env="MEGA_DEFAULT_CREDENTIALS")
    MEGA_INTANCE_DEFAULT: str = Field("MEGA_INTANCE_DEFAULT", env="MEGA_INTANCE_DEFAULT")
    EVOL_SERVER_VALIDATE_WHATS: str = Field("EVOL_SERVER_VALIDATE_WHATS", env="EVOL_SERVER_VALIDATE_WHATS")
    LOGFIRE_TOKEN: str = Field("123", env="LOGFIRE_TOKEN")


    @computed_field  # type: ignore[misc]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    SMTP_TLS: bool = True
    SMTP_SSL: bool = False
    SMTP_PORT: int = 587
    SMTP_HOST: str | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    # TODO: update type to EmailStr when sqlmodel supports it
    EMAILS_FROM_EMAIL: str | None = None
    EMAILS_FROM_NAME: str | None = None

    BASE_URL_WHATSAPP: str | None = None
    BASE_URL_V15_WHATSAPP: str | None = None
    GCP_CREDENTIALS: str | None = None


    REDIS_HOST: str | None = None
    REDIS_PORT: str | None = None
    REDIS_PASSWORD: str | None = None
    REDIS_SSL: str | None = None
    VERYFY_TOKEN: str | None = None

    EXPIRATION_TIME: int | None = None

    TZ: str = Field('America/Sao_Paulo', env='TZ')

    SERVER_URLS_EVO: str | None = None



    @model_validator(mode="after")
    def _set_default_emails_from(self) -> Self:
        if not self.EMAILS_FROM_NAME:
            self.EMAILS_FROM_NAME = self.PROJECT_NAME
        return self

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48

    @computed_field  # type: ignore[misc]
    @property
    def emails_enabled(self) -> bool:
        return bool(self.SMTP_HOST and self.EMAILS_FROM_EMAIL)

    # TODO: update type to EmailStr when sqlmodel supports it
    EMAIL_TEST_USER: str = "test@example.com"
    # TODO: update type to EmailStr when sqlmodel supports it
    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_PASSWORD: str
    FIRST_FULL_NAME: str
    USERS_OPEN_REGISTRATION: bool = False

    def _check_default_secret(self, var_name: str, value: str | None) -> None:
        if value == "changethis":
            message = (
                f'The value of {var_name} is "changethis", '
                "for security, please change it, at least for deployments."
            )
            if self.ENVIRONMENT == "local":
                warnings.warn(message, stacklevel=1)
            else:
                raise ValueError(message)

    def get_server_urls_evolution(self) -> List[str]:
        return [url.strip() for url in self.SERVER_URLS_EVO.split(',')]

    def get_server_urls_mega_api(self) -> List[str]:
        return [url.strip() for url in self.MEGA_SERVER_URL.split(',')]

    @model_validator(mode="after")
    def _enforce_non_default_secrets(self) -> Self:
        self._check_default_secret("SECRET_KEY", self.SECRET_KEY)
        self._check_default_secret("POSTGRES_PASSWORD", self.POSTGRES_PASSWORD)
        self._check_default_secret(
            "FIRST_SUPERUSER_PASSWORD", self.FIRST_SUPERUSER_PASSWORD
        )

        return self


settings = Settings()  # type: ignore
