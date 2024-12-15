from sqlmodel import Session
from app.services.integration_service_balle import IntegrationServiceBalle
from app.services.base_service import BaseDisponibilidadeService
from app.services.credential_service import CredentialService


class DisponibilidadeServiceFactory:
    @staticmethod
    def get_service(client_id: int, codEstab: str, session: Session) -> BaseDisponibilidadeService:

        credential_service = CredentialService(db_session=session)
        credentials = credential_service.get_credentials(client_id, codEstab)
        api_provider = credentials["api_provider"]

        if api_provider == "balle":
            return IntegrationServiceBalle(auth_token=credentials["auth_token"])

        else:
            raise ValueError(f"Provedor de API desconhecido: {api_provider}")
