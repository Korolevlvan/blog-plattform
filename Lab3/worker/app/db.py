from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings


class MainBase(DeclarativeBase):
    pass


class UsersBase(DeclarativeBase):
    pass


main_engine = create_engine(settings.main_database_url, pool_pre_ping=True)
users_engine = create_engine(settings.users_database_url, pool_pre_ping=True)

MainSessionLocal = sessionmaker(bind=main_engine, autoflush=False, autocommit=False)
UsersSessionLocal = sessionmaker(bind=users_engine, autoflush=False, autocommit=False)
