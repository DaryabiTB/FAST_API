import random
from typing import Optional

import psycopg2
from fastapi import FastAPI, Response, status, HTTPException
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

from app.database import close_connection, get_connection

app = FastAPI()

my_post = [{"id": 1, "title": "hello", "content": "world", "published": True},
           {"id": 2, "title": "world", "content": "hello", "published": False}]


# post model validates the data
class Post_Model(BaseModel):
    title: str
    content: str
    published: bool = True  # default, it is an optional field and it only accepts boolean
    author: Optional[str] = None  # default, it is an optional field and it only accepts string
    rating: Optional[int] = None  # default, it is an optional field and it only accepts integer
    # tags: list


@app.get("/posts")
def get_posts():
    connection = get_connection()
    if not connection:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={"message": "failed to connect to database"})
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products")
    posts = cursor.fetchall()
    cursor.close()
    close_connection(connection)
    return {"my post": posts.__dict__}  # fast api automatically convert list to jsonify dict


@app.get("/")
async def root():
    return {"message": "Hello end"}


@app.get("/hello/{name}")
async def hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/posts")
def create_post(post: Post_Model, status_code: int = status.HTTP_201_CREATED):
    # print(post.dict())  # convert pydantic model to dict
    id = random.randint(1, 1000000)
    connection = get_connection()
    if not connection:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={"message": "failed to connect to database"})

    cursor = connection.cursor()
    cursor.execute("INSERT INTO products (id, title, content, published) VALUES (%s, %s, %s, %s)",
                   (id, post.title, post.content, post.published))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": f"post with {id} was not found"})
    connection.commit()
    cursor.close()
    close_connection(connection)
    return {"message": f"created post: {post.dict()}"}


@app.post("/posts/{id}")
def get_post_by_id(id: int):
    connection = get_connection()
    if not connection:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={"message": "failed to connect to database"})
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": f"post with {id} was not found"})
    cursor.close()
    connection.close()
    return {"post": post}


@app.delete("/posts/{id}")
def delete_post_by_id(id: int, status_code: int = status.HTTP_204_NO_CONTENT):
    connection = get_connection()
    if not connection:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={"message": "failed to connect to database"})
    cursor = connection.cursor()
    cursor.execute("DELETE FROM posts WHERE id = %s", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": f"post with {id} was not found"})
    connection.commit()
    cursor.close()
    connection.close()

    return {"message": f"deleted post: {post[0]}"}


@app.put("/posts/{id}")
def update_post(id: int, post: Post_Model, status_code: int = status.HTTP_202_ACCEPTED):
    connection = get_connection()
    if not connection:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={"message": "failed to connect to database"})
    cursor = connection.cursor()
    cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s",
                   (post.title, post.content, post.published, str(id)))
    post = cursor.fetchone()
    # Check if the `post` is empty. If it is, then return a 404 error.
    if not my_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": f"post with {id} was not found"})
    post_dict = post.dict()
    post_dict['id'] = id

    connection.commit()
    cursor.close()
    connection.close()

    return {"message": f"updated post: {post_dict}"}
