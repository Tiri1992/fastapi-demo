import pytest
from app.oauth2 import create_access_token
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app.database import get_db, Base
from app import schema
from app.config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    bind=engine, autocommit=False, autoflush=False)


@pytest.fixture(scope="function")
def session():
    # This way we have access to the DB obj as well as the client by keeping them separate
    # Run cleanup of resources. Easier to debug any issues to keep the db visible after build.
    Base.metadata.drop_all(bind=engine)
    # Run code before yielding testClient
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(session):
    # Read up on scopes: https://docs.pytest.org/en/6.2.x/fixture.html#scope-sharing-fixtures-across-classes-modules-packages-or-session
    # Issues occur when teardown is per test function. Scope default is set to 'function'
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


# User

@pytest.fixture(scope="function")
def test_user(client):
    user_data = {
        "email": "john.doe@gmail.com",
        "password": "pass123",
    }

    res = client.post("/users/", json=user_data)

    # Verify
    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture(scope="function")
def token(test_user):
    # Returns access token to be created specifically for test purposes
    return create_access_token({"user_id": test_user['id']})


@pytest.fixture(scope="function")
def test_authorised_client(client, token):
    # Anytime we need to perform a request whilst being authorised use this
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client
