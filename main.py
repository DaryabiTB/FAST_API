from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# post model validates the data
class Post_Model(BaseModel):
    title: str
    content: str
    published: bool = True  # default, it is an optional field and it only accepts boolean
    author: Optional[str] = None  # default, it is an optional field and it only accepts string
    rating: Optional[int] = None  # default, it is an optional field and it only accepts integer
    # tags: list


@app.get("/")
async def root():
    return {"message": "Hello end"}


@app.get("/hello/{name}")
async def hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/create_post")
def create_post(post: Post_Model):
    print(post.dict())  # convert pydantic model to dict
    return {"message": f"created post: {post.dict()}"}
