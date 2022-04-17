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

# Curr video time: 2:02:01


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
