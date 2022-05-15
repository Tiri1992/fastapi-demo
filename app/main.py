from gettext import find
from lib2to3.pgen2.token import OP
from turtle import pos
from fastapi import FastAPI
# Models
from . import models
from .database import SessionLocal, engine, get_db

from .routers import post, user, auth
# Passlib -> to use bcrypt hashing algo
models.Base.metadata.create_all(bind=engine)

# Create an instance
app = FastAPI()


# NOTE: If you have to routes that are the same i.e. '/' it will resolve the first function as the route.

# Curr video time: 8:11:09

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
