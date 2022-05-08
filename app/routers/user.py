# Models
from fastapi import FastAPI
from fastapi import Response
from fastapi import status
from fastapi import HTTPException
from fastapi import Depends
# Do not import app from app. Make use of the APIRouter
from fastapi import APIRouter
from fastapi.params import Body
from sqlalchemy.orm import Session
from .. import models, schema, utils
from ..database import get_db

# Similar to FastAPI class, but allows us to keep our submodules grouped per path operations
router = APIRouter(
    prefix='/users',
    tags=["Users"],
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.User)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    # Hash the pw - user.password
    pw_hash = utils.hash(user.password)
    # Update the pydantic model with hash
    user.password = pw_hash
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    # Refresh returns the data back to us
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schema.User)
def get_user(id: int, db: Session = Depends(get_db)):
    # Get specific user by id
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id={id} does not exist.")
    return user
