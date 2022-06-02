from lib2to3.pgen2.token import OP
from fastapi import FastAPI
# CORS
from fastapi.middleware.cors import CORSMiddleware
# Models
from . import models
from .database import engine

from .routers import post, user, auth, vote

# Passlib -> to use bcrypt hashing algo
# Manage the creation/migration of DB in alembic
# models.Base.metadata.create_all(bind=engine)

# Create an instance
app = FastAPI()

# Best security practice to narrow down the origins that should
# have access to our application
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# NOTE: If you have to routes that are the same i.e. '/' it will resolve the first function as the route.

# Curr video time: 11:15:21

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get('/')
def root():
    return {
        "message": "Hello World!"
    }
