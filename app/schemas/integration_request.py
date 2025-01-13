from datetime import date
from typing import Optional, List
from sqlmodel import SQLModel
from pydantic import Field


class DisponibilidadeRequest(SQLModel):
    cod_astab: int
    dt_agenda: str
    periodo: str
    servicos: str
    tp_agd: str


class PacienteRequest(SQLModel):
    cod_astab: int
    cpf: str
    email: str
    id: int
    celular: str


class CreatePacienteRequest(SQLModel):
    cod_astab: int
    cpf: str
    nome: str
    celular: Optional[str]
    email: Optional[str]
    observacao: Optional[str]
    tp_origem: Optional[str]
    cod_origem: Optional[str]


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


class BasePaciente(SQLModel):
    codigo: int = Field(description="Código único do cliente")
    nome: str = Field(description="Nome do cliente")
    cpf: str = Field(description="CPF do cliente sem pontuação")
    dtNascimento: Optional[date] = Field(default=None, description="Data de nascimento do cliente")
    celular: Optional[str] = Field(default=None, description="Número de celular principal do cliente")
    celular2: Optional[str] = Field(default=None, description="Número de celular secundário do cliente")
    email: Optional[str] = Field(default=None, description="E-mail do cliente")
    telefone: Optional[str] = Field(default=None, description="Telefone fixo do cliente")
    dtCadastro: Optional[date] = Field(default=None, description="Data de cadastro do cliente")
    sexo: Optional[str] = Field(default=None, description="Sexo do cliente")
    profissao: Optional[str] = Field(default=None, description="Profissão do cliente")
    UF: Optional[str] = Field(default=None, description="Estado do cliente")
    cidade: Optional[str] = Field(default=None, description="Cidade do cliente")
    bairro: Optional[str] = Field(default=None, description="Bairro do cliente")
    cep: Optional[str] = Field(default=None, description="CEP do cliente")
    endereco: Optional[str] = Field(default=None, description="Endereço do cliente")
    numEndereco: Optional[str] = Field(default=None, description="Número do endereço")
    tipoOrigem: Optional[str] = Field(default=None, description="Tipo de origem do cliente")
    origem: Optional[str] = Field(default=None, description="Origem do cliente")
    pontos: Optional[int] = Field(default=None, description="Pontuação do cliente")


class BaseCreatePaciente(SQLModel):
    codigo: str


class Prof(SQLModel):
    cod_usuario: Optional[str]
    nom_usuario: Optional[str]


class Servico(SQLModel):
    codServico: int
    nome: str
    tempo: int
    label: str
    cod_saldo: str
    usa_dia: Optional[str]
    dia_retorno: int


class RequestCreateAgendamento(SQLModel):
    cod_cli: int
    cod_estab: int
    prof: Prof
    dt_agd: str
    hri: str
    serv: List[Servico]
    cod_plano: str
    ag_sala: bool
    cod_sala: int
    cod_vendedor: str
    cod_equipamento: int
