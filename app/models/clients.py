from datetime import datetime
from typing import List, Optional

from sqlmodel import SQLModel, Field, Relationship, Column, String

from app.core.config import settings

TZ = settings.TZ


class Clients(SQLModel, table=True):
    __tablename__ = "clients"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column(String, unique=True, index=True, nullable=False))
    phone: Optional[str] = None
    status: Optional[str] = None
    created_at: datetime = Field(default=datetime.now().isoformat())
    whatsapp_phone_number_id: str = Field(nullable=False)
    owner_id: Optional[int] = Field(default=None, foreign_key="users.id")


class Threads(SQLModel, table=True):
    __tablename__ = "threads"

    id: int = Field(default=None, primary_key=True, index=True)
    sender_id: str = Field(index=True)
    thread_id: str = Field()
    expiration_time: datetime = Field()
    client_id: int = Field(default=None, foreign_key="clients.id")
    #owner: 'User' = Relationship(back_populates="notification_flow")
    #client_id: int = Field(default=None, foreign_key="clients.id")

