from typing import Optional
from sqlmodel import SQLModel
from pydantic import Field


class ClientSchemaBase(SQLModel):
    name: str
    phone: Optional[str]
    status: str = Field(default="A", description="Status of the client (default: A)")


class ClientSchema(ClientSchemaBase):
    id: Optional[int]


class ClientSchemaCreate(ClientSchemaBase):
    whatsapp_phone_number_id: Optional[str] = None
