from abc import ABC, abstractmethod


class BaseDisponibilidadeService(ABC):
    @abstractmethod
    async def get_disponibilidade(self, codEstab: int, dtAgenda: str, periodo: str, servicos: str, tpAgd: str):
        pass
