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
import psycopg2
from psycopg2.extras import RealDictCursor
# Create an instance
app = FastAPI()

# NOTE: If you have to routes that are the same i.e. '/' it will resolve the first function as the route.

# Curr video time: 4:34:30


class Post(BaseModel):
    """Representation of Post to be sent in the body of /createposts"""
    title: str
    content: str
    published: bool = True


try:
    # RealDictCursor modifies the returned result from the cursor so that its more user friendly for the developer. This case, it will return a dict.
    # This allows you to get() values from the response i.e. res["id"] or res["name"], where "id" and "name" are fields on the table.
    conn = psycopg2.connect(host='localhost', database='fastapi',
                            user='postgres', password='', cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Database connected successfully.")
except Exception as err:
    print(f"Connecting to db failed: {err}")


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
    cursor.execute("""SELECT * FROM posts;""")
    # Response from db
    res = cursor.fetchall()
    print(res)
    return {
        "data": res,
    }


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    # Placeholders %s with a tuple holding the values allows the library to check for sql injections
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
                   (post.title, post.content, post.published))
    # Get result from RETURNING statement
    new_post = cursor.fetchone()
    # We need to commit the changes to persist the result
    conn.commit()
    return {
        "data": new_post,
    }

# NOTE: ORDER MATTERS, if I define an endpoint /posts/latest it will work top down to find matching path
# So this will need to be before /posts/{id} or it will this your id = "latest" and throw an error.


@app.get("/posts/{id}")
def get_post(id: int):
    # posts -> plural
    # path parameter is the {id} field: we type annotated it here as an int
    # NOTE: make sure you put the type annotation as int to convert it from str -> int (for id)
    # For %s placeholders requires values of type str.
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    res = cursor.fetchone()
    if not res:
        # Check http status codes. 404 = server can not find the requested resource
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found.",
        )
    return {
        "post_detail": res
    }


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # For delete requests, we can provide a 204 - NO content response which is typical for delete requests
    # HTTP 204 No Content: The server successfully processed the request, but is not returning any content
    # Find the index in the array that has required id
    cursor.execute(
        """DELETE FROM posts WHERE id = %s RETURNING *;""", (str(id), ))
    res = cursor.fetchone()
    # Persist the change to the DB.
    conn.commit()
    if res is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found.",
        )
    # We dont want to send any data back for a 204 response
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update


@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
def update_post(id: int, post: Post):
    # Either 200 or 204 should be okay as a response for a PUT request
    # Remember for PUT requests we need to send the body alongside the request which contains
    # the entire payload for updating (even if its just a subset being updates).
    # This is different from PATCH were we define the subset of data to update the resource with.
    # Easier to see with the UPDATE statement, we require all data (even that which has not changed). I.e. PUT request.
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                   (post.title, post.content, post.published, str(id)))
    res = cursor.fetchone()
    # Persist change to db
    conn.commit()
    if res is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found.",
        )
    # Update the entire post with new record
    return {
        "updated": res
    }
