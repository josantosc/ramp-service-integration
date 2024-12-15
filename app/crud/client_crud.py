from typing import Any

from sqlmodel import Session, select
from fastapi_pagination import Params
from fastapi_pagination.ext.sqlmodel import paginate
from fastapi import status
from sqlalchemy.exc import SQLAlchemyError


from app.core.security import get_password_hash, verify_password
from app.models.clients import Clients
from app.models.users import Users
from app.schemas.client_schema import ClientSchemaCreate


def create_client(*, session: Session, client_create: ClientSchemaCreate) -> Clients:
    db_obj = Clients(**client_create.dict())
    print(db_obj)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)

    return Clients(**dict(db_obj))


def update_user(*, session: Session, db_user: Clients, user_in: "ClientsUpdate") -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_email(*, session: Session, email: str) -> Clients | None:
    statement = select(Clients).where(Clients.email == email)
    session_user = session.exec(statement).first()
    return session_user


def authenticate(*, session: Session, email: str, password: str) -> Clients | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user


def get_all_clients_use_case(session: Session, size: int = 50, page: int = 1):
    query = select(Clients).where(Clients.status == "A")
    params = Params(page=page, size=size)
    return paginate(session, query=query, params=params)


def create_client_use_case(session: Session, client_data: ClientSchemaCreate, user_id: int):
    try:
        new_client = Clients(**client_data.dict(), user_id=user_id)
        session.add(new_client)
        session.commit()
        session.refresh(new_client)
        return new_client
    except SQLAlchemyError as e:
        raise Exception(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed create client. Please try again later.",
            more_info=str(e)
        )
