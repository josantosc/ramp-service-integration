from typing import Any, Optional
from httpx import AsyncClient

from app.services.base_service import BaseCreatePacienteService


class IntegrationCreatePacienteServiceBalle(BaseCreatePacienteService):
    def __init__(self, auth_token: str):
        self.auth_token = auth_token
        self.base_url = "https://app.bellesoftware.com.br/api/release/controller/IntegracaoExterna/v1.0"

    async def create_paciente(self, cod_estab: int, nome: str, celular: str, email: str, cpf: str, observacao: str, tp_origem: str, cod_origem: str) -> Any:
        url = f"{self.base_url}/cliente/gravar"
        headers = {
            "Authorization": f"{self.auth_token}"
        }
        params = {
            "nome": nome,
            "celular": celular,
            "email": email,
            "cpf": cpf,
            "observacao": observacao,
            "tpOrigem": tp_origem,
            "codOrigem": cod_origem,
            "codEstab": cod_estab,
        }

        async with AsyncClient() as client:
            response = await client.post(url, headers=headers, data=params)

            response.raise_for_status()

            return response.json()
