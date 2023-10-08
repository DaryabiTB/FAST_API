from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello end"}


@app.get("/hello/{name}")
async def hello(name: str):
    return {"message": f"Hello {name}"}


class Post:
    title: str


@app.post("/create_post")
def create_post(post: dict = Body(...)):
    return {"message": f"created post: {post['title']}"}
