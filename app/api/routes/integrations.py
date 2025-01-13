from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import col, delete, func, select

from app.crud.user_crud import get_user_by_email, update_user, create_user
from app.deps.users_deps import (
    CurrentUser,
    SessionDep,
    get_current_active_superuser
)
from app.core.config import settings
from app.core.security import get_password_hash, verify_password
from app.models.users import (
    UpdatePassword,
    Users,
    UserCreate,
    UserPublic,
    UserRegister,
    UsersPublic,
    UserUpdate,
    UserUpdateMe,
)
from app.models.item_model import Item
from app.models.token_model import (
    Message
)
from app.utils.login import generate_new_account_email, send_email
from app.services.service_factory import DisponibilidadeServiceFactory
from app.schemas.integration_request import DisponibilidadeRequest, DisponibilidadeDiaModel, PacienteRequest, \
    BasePaciente, BaseCreatePaciente, CreatePacienteRequest, RequestCreateAgendamento

router = APIRouter()


@router.get(
    "/horario/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=List[DisponibilidadeDiaModel]
)
async def get_disponibilidade(session: SessionDep, skip: int = 0, limit: int = 100,
                              params: DisponibilidadeRequest = Depends(),
                              client_id: int = Query(..., description="ID do cliente")
                              ):
    service = DisponibilidadeServiceFactory.get_service(client_id, params.cod_estab, session)
    return await service.get_disponibilidade(
        cod_estab=params.cod_estab,
        dt_agenda=params.dt_agenda,
        periodo=params.periodo,
        servicos=params.servicos,
        tp_agd=params.tp_agd,
    )


@router.get(
    "/paciente/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=List[BasePaciente]
)
async def get_paciente(session: SessionDep, skip: int = 0, limit: int = 100,
                       params: PacienteRequest = Depends(),
                       client_id: int = Query(..., description="ID do cliente")
                       ):
    service = DisponibilidadeServiceFactory.get_paciente(client_id, params.cod_estab, session)
    return await service.get_paciente(
        cod_estab=params.cod_estab,
        cpf=params.cpf,
        email=params.email,
        id=params.servicos,
        celular=params.tpAgd,
    )


@router.post(
    "/paciente/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=List[BaseCreatePaciente]
)
async def create_paciente(session: SessionDep,
                          params: CreatePacienteRequest = Depends(),
                          client_id: int = Query(..., description="ID do cliente")
                          ):
    service = DisponibilidadeServiceFactory.create_paciente(client_id, params.cod_estab, session)
    return await service.create_paciente(
        cod_estab=params.cod_estab,
        cpf=params.cpf,
        nome=params.nome,
        celular=params.celular,
        email=params.email,
        observacao=params.observacao,
        tp_origem=params.tp_origem,
        cod_origem=params.cod_origem
    )


@router.post(
    "/agendamento/",
    dependencies=[Depends(get_current_active_superuser)],
    #response_model=List[BaseCreatePaciente]
)
async def create_agendamento(session: SessionDep,
                             body: RequestCreateAgendamento = Depends(),
                             ):
    service = DisponibilidadeServiceFactory.create_agendamento(body.cod_cli, str(body.cod_estab), session)
    return await service.create_agendamento(
        cod_cli=body.cod_cli,
        cod_estab=body.cod_estab,
        prof=body.prof,
        dt_agd=body.dt_agd,
        hri=body.hri,
        serv=body.servicos,
        cod_plano=body.cod_plano,
        ag_sala=body.ag_sala,
        cod_sala=body.cod_sala,
        cod_vendedor=body.cod_vendedor,
        cod_equipamento=body.cod_equipamento
    )
