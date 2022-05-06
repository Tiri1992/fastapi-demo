from gettext import find
from lib2to3.pgen2.token import OP
from turtle import pos
from fastapi import FastAPI
from fastapi import Response
from fastapi import status
from fastapi import HTTPException
from fastapi import Depends
from fastapi.params import Body
from sqlalchemy.orm import Session
from . import schema
from . import utils
# Schema validation with pydantic
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
# Models
from . import models
from .database import SessionLocal, engine, get_db

# Passlib -> to use bcrypt hashing algo
models.Base.metadata.create_all(bind=engine)

# Create an instance
app = FastAPI()


# NOTE: If you have to routes that are the same i.e. '/' it will resolve the first function as the route.

# Curr video time: 6:11:39

# In order to map(schema.Post) we parse list[schema.Post] to tell fastapi the type we expect to return
@app.get("/posts", response_model=list[schema.Post])
def get_posts(db: Session = Depends(get_db)):
    """Gets all rows from post table."""
    posts = db.query(models.Post).all()
    return posts

# In the response_model, we can reference a pydantic schema to define the response data


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def create_post(post: schema.PostCreate, db: Session = Depends(get_db)):
    # Have sqlalchemy handle the model inputs instead of raw sql query
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    # equivalent to adding RETURNING *; It retrieves that obj and stores it back as new_post
    db.refresh(new_post)
    # new_post is a sqlAlchemy model, and pydantic only knows how to handle dicts. So we needed to specify
    # in the schema.Post model -> orm_mode = True
    return new_post

# # NOTE: ORDER MATTERS, if I define an endpoint /posts/latest it will work top down to find matching path
# # So this will need to be before /posts/{id} or it will this your id = "latest" and throw an error.


@app.get("/posts/{id}", response_model=schema.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # posts -> plural
    # path parameter is the {id} field: we type annotated it here as an int
    # NOTE: make sure you put the type annotation as int to convert it from str -> int (for id)
    # For %s placeholders requires values of type str.
    # always use .first() when calling an ID as this grabs the first result -> More efficient
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        # Check http status codes. 404 = server can not find the requested resource
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found.",
        )
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # For delete requests, we can provide a 204 - NO content response which is typical for delete requests
    # HTTP 204 No Content: The server successfully processed the request, but is not returning any content
    # Find the index in the array that has required id
    post = db.query(models.Post).filter(models.Post.id == id)
    # Persist the change to the DB.
    if post.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found.",
        )
    post.delete(synchronize_session=False)
    db.commit()
    # We dont want to send any data back for a 204 response
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# # Update


@app.put("/posts/{id}", status_code=status.HTTP_200_OK, response_model=schema.Post)
def update_post(id: int, post: schema.PostCreate, db: Session = Depends(get_db)):
    # Either 200 or 204 should be okay as a response for a PUT request
    # Remember for PUT requests we need to send the body alongside the request which contains
    # the entire payload for updating (even if its just a subset being updates).
    # This is different from PATCH were we define the subset of data to update the resource with.
    # Easier to see with the UPDATE statement, we require all data (even that which has not changed). I.e. PUT request.

    # Saving the query as a variables
    post_query = db.query(models.Post).filter(models.Post.id == id)

    # Check post exists, if not raise 404
    post_val = post_query.first()
    if post_val is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found.",
        )
    # If it does exist, update with pydantic model passed in by client request
    post_updated = post_query.update(post.dict(), synchronize_session=False)
    # Update the entire post with new record
    db.commit()
    return post_val


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schema.User)
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
