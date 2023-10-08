import random
from typing import Optional

from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel

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
    return {"my post": my_post}  # fast api automatically convert list to jsonify dict


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
    post_dict = post.dict()
    post_dict['id'] = id
    my_post.append(post_dict)
    return {"message": f"created post: {post.dict()}"}


@app.post("/posts/{id}")
def get_post_by_id(id: int, response: Response):
    # it automatically converts string to int. this also does the validation, hence if we pass
    # a string, it will throw an error
    global my_post
    post = [post for post in my_post if post['id'] == id]

    # Check if the `my_post` list is empty. If it is, then return a 404 error.
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": f"post with {id} was not found"})
    # Otherwise, return the first element of the `my_post` list.
    return Post_Model(**post[0])


@app.delete("/posts/{id}")
def delete_post_by_id(id: int, status_code: int = status.HTTP_204_NO_CONTENT):
    global my_post
    post = [post for post in my_post if post['id'] == id]

    # Check if the `my_post` list is empty. If it is, then return a 404 error.
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": f"post with {id} was not found"})
    # Otherwise, remove the first element of the `my_post` list.
    my_post.remove(post[0])
    return {"message": f"deleted post: {post[0]}"}


@app.put("/posts/{id}")
def update_post(id: int, post: Post_Model, status_code: int = status.HTTP_202_ACCEPTED):
    global my_post
    my_post = [post for post in my_post if post['id'] == id]

    # Check if the `my_post` list is empty. If it is, then return a 404 error.
    if not my_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": f"post with {id} was not found"})
    # Otherwise, update the first element of the `my_post` list.
    post_dict = post.dict()
    post_dict['id'] = id
    my_post[0] = post_dict
    return {"message": f"updated post: {post[0]}"}
