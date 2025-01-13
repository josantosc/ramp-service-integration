from typing import Any, Optional
from httpx import AsyncClient

from app.services.base_service import BaseAgendamentoService


class IntegrationAgendamentoServiceBalle(BaseAgendamentoService):
    def __init__(self, auth_token: str):
        self.auth_token = auth_token
        self.base_url = "https://app.bellesoftware.com.br/api/release/controller/IntegracaoExterna/v1.0"

    async def create_agendamento(self, cod_cli: int,
                                 cod_estab: int,
                                 prof: dict,
                                 dt_agd: str,
                                 hri: str,
                                 serv: list,
                                 cod_plano: str,
                                 ag_sala: bool,
                                 cod_sala: int,
                                 cod_vendedor: str,
                                 cod_equipamento: int) -> Any:
        url = f"{self.base_url}/cliente/gravar"
        headers = {
            "Authorization": f"{self.auth_token}"
        }
        params = {"codCli": cod_cli,
                  "codEstab": cod_estab,
                  "prof": prof,
                  "dtAgd": dt_agd,
                  "hri": hri,
                  "serv": serv,
                  "codPlano": cod_plano,
                  "agSala": ag_sala,
                  "codSala": cod_sala,
                  "codVendedor": cod_vendedor,
                  "codEquipamento": cod_equipamento}

        async with AsyncClient() as client:
            response = await client.post(url, headers=headers, data=params)

            response.raise_for_status()

            return response.json()
