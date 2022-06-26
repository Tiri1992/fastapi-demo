# from .conftest import session, client
import pytest
from app import schema
from jose import jwt
from app.config import settings


def test_create_user(client):
    # need to add trailing "/users/", this is because with our api endpoint /user
    # does a redirect to /users/ and this gives a status code of 307, hence would fail the 200 status code
    res = client.post("/users/", json={
        "email": "john.doe@gmail.com",
        "password": "pass123",
    })
    assert res.status_code == 201


def test_login_user(client, test_user):
    # This works slightly different to /users/ because the path operation for users
    # has '/' as an endpoint where as if you look under auth.py we have the path operation
    # as '/login'
    # FORM-DATA -> use the data param in client.post()
    res = client.post("/login", data={
        "username": test_user['email'],
        "password": "pass123",
    })
    # to debug print out the response json and use the -s flag
    login_res = schema.Token(**res.json())
    payload = jwt.decode(
        token=login_res.access_token,
        key=settings.secret_key,
        algorithms=[settings.algorithm],
    )

    id: str = payload.get("user_id")
    assert res.status_code == 200
    # Check user.ids match
    assert id == test_user['id']
    # Token type
    assert login_res.token_type == 'bearer'


@pytest.mark.parametrize(
    "email,password,status_code,", [
        ('wrongemail@gmail.com', 'wrongPass', 403),
        ('john.doe@gmail.com', 'pass123133', 403),
        (None, "pass123", 422),
        ('john.doe@gmail.com', None, 422)
    ]
)
def test_incorrect_login(test_user, client, email, password, status_code):
    # Param test, tests for incorrect arg in: email, password, None for email, None for password all separately
    # Test that given a valid username and an incorrect password
    # the server response is 403 and details 'Invalid credentials'
    res = client.post(
        "/login", data={"username": email, "password": password})

    assert res.status_code == status_code
    # assert res.json().get("detail") == 'Invalid credentials'
