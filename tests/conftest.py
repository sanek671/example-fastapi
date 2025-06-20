from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.main import app
from app.config import settings
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models
from alembic import command


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'
engin = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessinLocal = sessionmaker(bind=engin, autoflush=False, expire_on_commit=False)


@pytest.fixture()
def session():
    print("My session fixture run")
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


@pytest.fixture
def test_user(client):
    user_data = json={"email": "sanek123@gmail.com", 
                      "password": "password123"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    # print(response.json())
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def test_user2(client):
    user_data = json={"email": "sanek@gmail.com", 
                      "password": "password123"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture
def test_posts(test_user, session, test_user2):
    post_data = ({
        "title": "first title",
        "content": "first content",
        "owner_id": test_user["id"]
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user["id"]
    }, {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user["id"]
    }, {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user2["id"]
    })

    def create_post_model(post):
        return models.Post(**post)
    
    post_map = map(create_post_model, post_data)
    posts = list(post_map)
    session.add_all(posts)

    # session.add_all([models.Post(title="first title", content="first content", owner_id=test_user["id"])],
    #                  models.Post(title="2nd title", content="2nd content", owner_id=test_user["id"]),
    #                  models.Post(title="3rd title", content="3rd content", owner_id=test_user["id"]))

    session.commit()
    posts = session.query(models.Post).all()
    return posts