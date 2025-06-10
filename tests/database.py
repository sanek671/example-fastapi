from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app.config import settings
from app.database import get_db, Base
from alembic import command


# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password@localhost:5432/fastapi_test'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'
engin = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessinLocal = sessionmaker(bind=engin, autoflush=False, expire_on_commit=False)
# Base.metadata.drop_all(bind=engin)

# def override_get_db():
#     db = TestingSessinLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# app.dependency_overrides[get_db] = override_get_db

# client = TestClient(app)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engin)
    Base.metadata.create_all(bind=engin)
    db = TestingSessinLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
