from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from fastapi import HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schema
from .. import models
from .. import utils
from .. import oauth2

router = APIRouter(
    tags=['Authentication'],
)


@router.post('/login', response_model=schema.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # {username = ..., password: ""}
    # Note: the user_credentials obj has username which we've built under as email in our User DB obj. Not to be confused
    # OAuth2PasswordRequestForm requests you sent the body under form-data.
    # Get user email from DB based on the credentials the client provided
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid credentials")

    # Verify the correct pw by using the hashed pw stored in the db
    # Look up notes on how to loggin in as a user.
    # Note that the `user` variable in the object stored in db
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    # Create token

    access_token = oauth2.create_access_token(
        data={
            "user_id": user.id,
        }
    )

    # return token
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
