from typing import Any

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
from app.schemas.integration_request import DisponibilidadeRequest

router = APIRouter()


@router.get(
    "/balle/",
    dependencies=[Depends(get_current_active_superuser)]
)
async def get_disponibilidade(session: SessionDep, skip: int = 0, limit: int = 100,
                              params: DisponibilidadeRequest = Depends(),
                              client_id: int = Query(..., description="ID do cliente"),
                              codEstab: str = Query(..., description="Código do estabelecimento")
                              ):
    service = DisponibilidadeServiceFactory.get_service(client_id, codEstab, session)
    return await service.get_disponibilidade(
        codEstab=params.codEstab,
        dtAgenda=params.dtAgenda,
        periodo=params.periodo,
        servicos=params.servicos,
        tpAgd=params.tpAgd,
    )

@router.post(
    "/balle/", dependencies=[Depends(get_current_active_superuser)], response_model=UserPublic
)
def create_agendamento(*, session: SessionDep, user_in: UserCreate) -> Any:
    """
    Create new user.
    """
    user = get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )

    user = create_user(session=session, user_create=user_in)
    if settings.emails_enabled and user_in.email:
        email_data = generate_new_account_email(
            email_to=user_in.email, username=user_in.email, password=user_in.password
        )
        send_email(
            email_to=user_in.email,
            subject=email_data.subject,
            html_content=email_data.html_content,
        )
    return user
