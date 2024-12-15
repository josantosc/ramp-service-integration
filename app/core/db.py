from sqlmodel import Session, create_engine, select, QueuePool

from app.crud.user_crud import create_user
from app.core.config import settings
from app.models.users import Users, UserCreate

engine = create_engine(f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}",
                       poolclass=QueuePool,
                       pool_size=10,
                       max_overflow=20,
                       pool_timeout=30,
                       pool_recycle=1800)


def init_db(session: Session) -> None:

    # from app.core.engine import engine
    # This works because the models are already imported and registered from app.models
    # SQLModel.metadata.create_all(engine)

    user = session.exec(
        select(Users).where(Users.email == settings.FIRST_SUPERUSER)
    ).first()
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            full_name=settings.FIRST_FULL_NAME,
            is_superuser=True,
        )
        user = create_user(session=session, user_create=user_in)
