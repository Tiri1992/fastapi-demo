from lib2to3.pgen2.token import OP
from turtle import pos
from fastapi import FastAPI
from fastapi.params import Body
# Schema validation with pydantic
from pydantic import BaseModel
from typing import Optional
from random import randrange
# Create an instance
app = FastAPI()

# NOTE: If you have to routes that are the same i.e. '/' it will resolve the first function as the route.


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


@app.post("/posts")
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
