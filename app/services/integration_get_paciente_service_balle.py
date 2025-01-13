from typing import Any
from httpx import AsyncClient

from app.services.base_service import BaseGetPacienteService


class IntegrationGetPacienteServiceBalle(BaseGetPacienteService):
    def __init__(self, auth_token: str):
        self.auth_token = auth_token
        self.base_url = "https://app.bellesoftware.com.br/api/release/controller/IntegracaoExterna/v1.0"

    async def get_paciente(self, cpf: str, id: int, cod_estab: int, email: str, celular: str) -> Any:
        url = f"{self.base_url}/cliente/listar"
        headers = {
            "Authorization": f"{self.auth_token}"
        }
        params = {
            "codEstab": cod_estab,
            "cpf": cpf,
            "email": email,
            "id": id,
            "celular": celular
        }

        async with AsyncClient() as client:
            response = await client.get(url, headers=headers, params=params)

            response.raise_for_status()

            return response.json()
