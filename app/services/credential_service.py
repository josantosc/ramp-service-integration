from sqlmodel import Session, select
from app.models.integrations_base import IntegrationsCredential
from typing import Optional


class CredentialService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_credentials(self, client_id: int, estabelecimento: str) -> Optional[dict]:
        query = (
            select(IntegrationsCredential)
            .where(
                IntegrationsCredential.client_id == client_id,
                IntegrationsCredential.estabelecimento == estabelecimento,
                IntegrationsCredential.status == "Ativo"  # Verifica status ativo
            )
        )
        result = self.db_session.exec(query).first()

        if result:
            return {
                "api_provider": result.provider,
                "auth_token": result.token,
                "client_id": result.client_id,
                "estabelecimento": result.estabelecimento,
            }

        raise ValueError(f"Credenciais não encontradas para cliente {client_id} e estabelecimento {estabelecimento}")
