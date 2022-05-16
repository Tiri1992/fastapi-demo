"""Creating JWT tokens."""
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import schema
from . import database
from . import models
from .config import settings
from jose import JWSError, jwt
from datetime import datetime, timedelta

# Endpoint for login user. Requires data to be in form type. So username, password
# as key attributes.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# WE NEED 3 things to sign the token
# SECRET, HEADER, PAYLOAD
# STORE SECRET_KEY AS ENV VARIABLE
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    # data is the values we decide to put in the payload.
    # There are 3 types of claims: registered, public & private claims.
    to_encode = data.copy()

    # We want to add the expiration date inside the payload of the token.
    # So that the user isn't logged in forever
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({
        "exp": expire,
    })
    # Good ref: https://jwt.io/introduction
    # claims -> what goes in the payload
    encoded_jwt = jwt.encode(
        claims=to_encode,
        key=SECRET_KEY,
        algorithm=ALGORITHM,
    )

    return encoded_jwt


def verify_access_token(token: str, credentials_exception) -> schema.TokenData | None:
    try:
        payload = jwt.decode(
            token=token,
            key=SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        # This will be relative to the data we stored in our payload
        # in our case we used 'user_id' but this might be different,
        # depending on how we design out JWT token.
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = schema.TokenData(id=id)
    except JWSError:
        raise credentials_exception
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    token: schema.TokenData = verify_access_token(
        token=token, credentials_exception=credentials_exception)
    # To avoid having the client use the token to authenticate on every path operation
    # We can return the user_id from this function.

    user = db.query(models.User).filter(models.User.id == token.id).first()
    # header is just what we need to define as bearer when we authenticate a user.
    return user
