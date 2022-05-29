"""Path operations associated to posts."""
# Models
from fastapi import Response
from fastapi import status
from fastapi import HTTPException
from fastapi import Depends
# Do not import app from app. Make use of the APIRouter
from fastapi import APIRouter
from fastapi.params import Body
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, schema
from .. import oauth2
from ..database import get_db

router = APIRouter(
    prefix='/posts',
    tags=['Posts'],
)


@router.get("/", response_model=list[schema.PostOut])
def get_posts(
        db: Session = Depends(get_db),
        current_user=Depends(oauth2.get_current_user),
        limit: int = 10,
        skip: int = 0,
        search: str | None = ""):
    """Gets all rows from post table."""
    # Made a functionality change to only get posts from current user
    # Query parameters are the remaining parameters given in our path operation function.

    # By default SQLAlchemy performs a left inner join. To get an left outer join you must specify.
    # To alias a column use .label()
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.owner_id == current_user.id, models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts

# In the response_model, we can reference a pydantic schema to define the response data


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def create_post(post: schema.PostCreate, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    # NOTE: by adding Depends(oauth2.get_current_user) it will require the user to be logged in via token
    # before accessing any of the endpoints such as create_post.

    # Have sqlalchemy handle the model inputs instead of raw sql query
    # NOTE: Get the owner_id from the current user thats logged on through the JWT TOKEN!
    new_post = models.Post(**post.dict(), owner_id=current_user.id)
    db.add(new_post)
    db.commit()
    # equivalent to adding RETURNING *; It retrieves that obj and stores it back as new_post
    db.refresh(new_post)
    # new_post is a sqlAlchemy model, and pydantic only knows how to handle dicts. So we needed to specify
    # in the schema.Post model -> orm_mode = True
    return new_post

# # NOTE: ORDER MATTERS, if I define an endpoint /posts/latest it will work top down to find matching path
# # So this will need to be before /posts/{id} or it will this your id = "latest" and throw an error.


@router.get("/{id}", response_model=schema.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    # posts -> plural
    # path parameter is the {id} field: we type annotated it here as an int
    # NOTE: make sure you put the type annotation as int to convert it from str -> int (for id)
    # For %s placeholders requires values of type str.
    # always use .first() when calling an ID as this grabs the first result -> More efficient
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).first()
    if post.Post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User not authorized to perform requested action.",
        )
    if not post:
        # Check http status codes. 404 = server can not find the requested resource
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found.",
        )
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    # For delete requests, we can provide a 204 - NO content response which is typical for delete requests
    # HTTP 204 No Content: The server successfully processed the request, but is not returning any content
    # Find the index in the array that has required id
    post = db.query(models.Post).filter(models.Post.id == id)
    # Persist the change to the DB.
    post_val = post.first()
    if post_val is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found.",
        )
    if post_val.owner_id != current_user.id:
        # User is trying to delete a post that does not belong to them
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action.")
    post.delete(synchronize_session=False)
    db.commit()
    # We dont want to send any data back for a 204 response
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# # Update


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schema.Post)
def update_post(id: int, post: schema.PostCreate, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
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

    if post_val.owner_id != current_user.id:
        # User is trying to delete a post that does not belong to them
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action.")
    # If it does exist, update with pydantic model passed in by client request
    post_updated = post_query.update(post.dict(), synchronize_session=False)
    # Update the entire post with new record
    db.commit()
    return post_val
