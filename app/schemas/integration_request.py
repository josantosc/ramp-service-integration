from typing import Optional
from sqlmodel import SQLModel
from pydantic import Field


class DisponibilidadeRequest(SQLModel):
    codEstab: int
    dtAgenda: str
    periodo: str
    servicos: str
    tpAgd: str
