"""Handles our db connection with SqlAlchemy."""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
import os

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db():
    """Gets session to our db and then cleans up resources."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# All models we will be defining are going to be extending this Base class.
Base = declarative_base()
