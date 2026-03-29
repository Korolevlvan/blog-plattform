# src/models/database.py
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# SQLAlchemy базовый класс для моделей
Base = declarative_base()

# Пример подключения к PostgreSQL
DATABASE_URL = "postgresql://postgres:postgres@db:5432/postgres"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)