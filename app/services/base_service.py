from abc import ABC, abstractmethod
from typing import Optional


class BaseDisponibilidadeService(ABC):
    @abstractmethod
    async def get_disponibilidade(self, cod_estab: int, dt_agenda: str, periodo: str, servicos: str, tp_agd: str):
        pass


class BaseGetPacienteService(ABC):
    @abstractmethod
    async def get_paciente(self, cpf: str, id: int, cod_estab: int, email: str, celular: str):
        pass


class BaseCreatePacienteService(ABC):
    @abstractmethod
    async def create_paciente(self, cod_estab: int, nome: str, celular: str, email: str, cpf: str, observacao: str,
                              tp_origem: str, cod_origem: str):
        pass


class BaseAgendamentoService(ABC):
    @abstractmethod
    async def create_agendamento(
            self,
            cod_cli: int,
            cod_estab: int,
            prof: dict,
            dt_agd: str,
            hri: str,
            serv: list,
            cod_plano: str,
            ag_sala: bool,
            cod_sala: int,
            cod_vendedor: str,
            cod_equipamento: int):
        pass
