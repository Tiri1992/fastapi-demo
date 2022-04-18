from gettext import find
from lib2to3.pgen2.token import OP
from turtle import pos
from fastapi import FastAPI
from fastapi import Response
from fastapi import status
from fastapi import HTTPException
from fastapi.params import Body
# Schema validation with pydantic
from pydantic import BaseModel
from typing import Optional
from random import randrange
# Create an instance
app = FastAPI()

# NOTE: If you have to routes that are the same i.e. '/' it will resolve the first function as the route.

# Curr video time: 3:47:17


class Post(BaseModel):
    """Representation of Post to be sent in the body of /createposts"""
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


# tmp db
my_post = [
    {
        "title": "title of post 1",
        "content": "content of post 1",
        "id": 1,
    },
    {
        "title": "favourite foods",
        "content": "I like pizza.",
        "id": 2,
    }
]


def find_post(id: int) -> Optional[dict]:
    for post in my_post:
        if post["id"] == id:
            return post


def find_idx(id: int) -> Optional[int]:
    for idx, post in enumerate(my_post):
        if post["id"] == id:
            return idx


@app.get("/")
def read_root():
    # Path operation (or route)
    # Keep the name of the route as descriptive as possible
    return {"Hello": "Tiri"}


@app.get("/posts")
def get_posts():
    # FastApi will automatically serialize a list as an array for json format
    return {
        "data": my_post,
    }


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    # Name of the function never matters, but its bad practice to have
    # the http method inside the endpoint i.e. 'createposts'
    # NOTE: POST requests sends data to the api server and then the server does something with that data
    # Body is a fastApi obj which extracts the body of the data being sent over by the client and the variable body
    # will be referencing this data.
    # If you ever need to serialise the model back into a json format we can use the .dict() method
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 10000000)
    my_post.append(post_dict)
    # ALWAYS SEND BACK THE DATA CREATED TO THE CLIENT!
    return {
        "data": post_dict,
    }

# NOTE: ORDER MATTERS, if I define an endpoint /posts/latest it will work top down to find matching path
# So this will need to be before /posts/{id} or it will this your id = "latest" and throw an error.


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    # posts -> plural
    # path parameter is the {id} field: we type annotated it here as an int
    # NOTE: make sure you put the type annotation as int to convert it from str -> int (for id)
    res = find_post(id)
    if not res:
        # Check http status codes. 404 = server can not find the requested resource
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found.",
        )
    return {
        "post_detail": find_post(id)
    }


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # For delete requests, we can provide a 204 - NO content response which is typical for delete requests
    # HTTP 204 No Content: The server successfully processed the request, but is not returning any content
    # Find the index in the array that has required id
    idx = find_idx(id)
    print(idx)
    if idx is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found.",
        )
    del my_post[idx]
    # We dont want to send any data back for a 204 response
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update


@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post):
    # Either 200 or 204 should be okay as a response for a PUT request
    # Remember for PUT requests we need to send the body alongside the request which contains
    # the entire payload for updating (even if its just a subset being updates).
    # This is different from PATCH were we define the subset of data to update the resource with.
    idx = find_idx(id)
    if idx is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found.",
        )
    # Update the entire post with new record
    data = post.dict()
    data["id"] = id
    my_post[idx] = data
    return {
        "message": "data was successfully updated."
    }
