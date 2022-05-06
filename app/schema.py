"""Schema model for validating request body data."""
from pydantic import BaseModel, EmailStr
from datetime import datetime


class PostBase(BaseModel):
    """Base class Post, and each request schema will extend
    depending on the client endpoint."""
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    """Response model. Extends PostBase."""
    id: int
    created_at: datetime

    class Config:
        # Will need to specfiy this to tell pydantic model to read
        # the data even if it is not a dict, but an ORM model
        orm_mode = True


class UserCreate(BaseModel):

    # EmailStr is a pydantic email validator
    email: EmailStr
    password: str


class User(BaseModel):

    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True
