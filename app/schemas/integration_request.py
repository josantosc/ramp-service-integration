from typing import Optional, List
from sqlmodel import SQLModel
from pydantic import Field


class DisponibilidadeRequest(SQLModel):
    codEstab: int
    dtAgenda: str
    periodo: str
    servicos: str
    tpAgd: str


class HorarioModel(SQLModel):
    horario: str
    cod: str
    bloq: str


class ProfissionalModel(SQLModel):
    codProf: str
    nome: str
    horarios: List[HorarioModel]


class DisponibilidadeDiaModel(SQLModel):
    nome: str
    data: str
    disp: str
    horarios: List[ProfissionalModel]
