from typing import List

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session
from starlette import status
from .routes import login, posts_route, user_route
from . import models
from .database import SessionLocal, engine, get_db

models.Base.metadata.create_all(bind=engine)

# Dependency

app = FastAPI()
app.include_router(posts_route.router)
app.include_router(user_route.router)
app.include_router(login.auth_router)


@app.get("/")
def root():
	return {"message": "Hello World"}
