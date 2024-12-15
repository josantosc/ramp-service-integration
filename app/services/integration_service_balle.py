from typing import Any
from httpx import AsyncClient

from app.services.base_service import BaseDisponibilidadeService


class IntegrationServiceBalle(BaseDisponibilidadeService):
    def __init__(self, auth_token: str):
        self.auth_token = auth_token
        self.base_url = "https://app.bellesoftware.com.br/api/release/controller/IntegracaoExterna/v1.0"

    async def get_disponibilidade(self, codEstab: int, dtAgenda: str, periodo: str, servicos: str, tpAgd: str) -> Any:
        url = f"{self.base_url}/agenda/disponibilidade"
        headers = {
            "Authorization": f"{self.auth_token}"
        }
        params = {
            "codEstab": codEstab,
            "dtAgenda": dtAgenda,
            "periodo": periodo,
            "servicos": servicos,
            "tpAgd": tpAgd,
        }

        async with AsyncClient() as client:
            response = await client.get(url, headers=headers, params=params)

            # Verifica se a requisição foi bem-sucedida
            response.raise_for_status()

            # Retorna a resposta como JSON
            return response.json()
