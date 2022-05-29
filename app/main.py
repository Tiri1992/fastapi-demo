from lib2to3.pgen2.token import OP
from fastapi import FastAPI
# Models
from . import models
from .database import engine

from .routers import post, user, auth, vote

# Passlib -> to use bcrypt hashing algo
models.Base.metadata.create_all(bind=engine)

# Create an instance
app = FastAPI()


# NOTE: If you have to routes that are the same i.e. '/' it will resolve the first function as the route.

# Curr video time: 9:21:25

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
