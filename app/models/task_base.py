from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field
import pytz


def current_time():
    return datetime.now(pytz.timezone('America/Sao_Paulo')).isoformat()


class RegisteredTask(SQLModel, table=True):
    __tablename__ = "registered_tasks"

    id: Optional[int] = Field(primary_key=True, index=True)
    task_id: str = Field(index=True)
    created_at: datetime = Field(default=current_time())
    campaign_id: Optional[int] = None


class Task(SQLModel, table=True):
    __tablename__ = "tasks"
    id: Optional[int] = Field(primary_key=True, index=True)
    client_id: Optional[int] = Field(index=True)
    created_at: Optional[datetime] = Field(default=current_time())
    name: str = None
    queue_id: Optional[int] = None
