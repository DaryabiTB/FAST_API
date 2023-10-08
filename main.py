from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# post model validates the data
class post_model(BaseModel):
    title: str
    content: str
    # author: str
    # tags: list


@app.get("/")
async def root():
    return {"message": "Hello end"}


@app.get("/hello/{name}")
async def hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/create_post")
def create_post(post: post_model):
    return {"message": f"created post: {post.title}"}
