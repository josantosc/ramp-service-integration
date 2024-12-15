from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field
from app.core.config import settings

TZ = settings.TZ


def current_time():
    return datetime.now().isoformat()


class CredentialsIntegrations(SQLModel):
    id: Optional[int] = Field(primary_key=True, index=True)
    client_id: int = Field(default=None, foreign_key="clients.id")
    estabelecimento: Optional[str] = Field(default=None)
    provider: Optional[str] = Field(default=None)
    token: Optional[str] = Field(default=None)
    create_at: Optional[datetime] = Field(default=datetime.now())
    updated_at: Optional[datetime] = Field(default=datetime.now())
    status: str = Field(default=None)


class IntegrationsCredential(CredentialsIntegrations, table=True):
    __tablename__ = "integrations_credentials"
