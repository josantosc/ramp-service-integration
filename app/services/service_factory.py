from sqlmodel import Session
from app.services.integration_service_balle import IntegrationServiceBalle
from app.services.integration_get_paciente_service_balle import IntegrationGetPacienteServiceBalle
from app.services.integration_create_paciente_service_balle import IntegrationCreatePacienteServiceBalle
from app.services.integration_create_agendamento_service_balle import IntegrationAgendamentoServiceBalle
from app.services.base_service import BaseDisponibilidadeService, BaseGetPacienteService, BaseCreatePacienteService, BaseAgendamentoService
from app.services.credential_service import CredentialService


class DisponibilidadeServiceFactory:
    @staticmethod
    def get_service(client_id: int, cod_estab: str, session: Session) -> BaseDisponibilidadeService:

        credential_service = CredentialService(db_session=session)
        credentials = credential_service.get_credentials(client_id, cod_estab)
        api_provider = credentials["api_provider"]

        if api_provider == "balle":
            return IntegrationServiceBalle(auth_token=credentials["auth_token"])

        else:
            raise ValueError(f"Provedor de API desconhecido: {api_provider}")

    @staticmethod
    def get_paciente(client_id: int, cod_estab: str, session: Session) -> BaseGetPacienteService:

        credential_service = CredentialService(db_session=session)
        credentials = credential_service.get_credentials(client_id, cod_estab)
        api_provider = credentials["api_provider"]

        if api_provider == "balle":
            return IntegrationGetPacienteServiceBalle(auth_token=credentials["auth_token"])

        else:
            raise ValueError(f"Provedor de API desconhecido: {api_provider}")


    @staticmethod
    def create_paciente(client_id: int, cod_estab: str, session: Session) -> BaseCreatePacienteService:

        credential_service = CredentialService(db_session=session)
        credentials = credential_service.get_credentials(client_id, cod_estab)
        api_provider = credentials["api_provider"]

        if api_provider == "balle":
            return IntegrationCreatePacienteServiceBalle(auth_token=credentials["auth_token"])

        else:
            raise ValueError(f"Provedor de API desconhecido: {api_provider}")

    @staticmethod
    def create_agendamento(client_id: int, cod_estab: str, session: Session) -> BaseAgendamentoService:

        credential_service = CredentialService(db_session=session)
        credentials = credential_service.get_credentials(client_id, cod_estab)
        api_provider = credentials["api_provider"]

        if api_provider == "balle":
            return IntegrationAgendamentoServiceBalle(auth_token=credentials["auth_token"])

        else:
            raise ValueError(f"Provedor de API desconhecido: {api_provider}")
