from typing import List

from fastapi import Depends, FastAPI, HTTPException, Query,
from sqlalchemy.orm import Session
from starlette import status
from starlette.middleware.cors import CORSMiddleware

from .routes import login, posts_route, user_route, votes_route
from . import models
from .database import SessionLocal, engine, get_db

# m
# Dependency


app = FastAPI(debug=True)

# origin = ['http://localhost:3000', 'http://localhost:8000', 'http://localhost:8080', 'http://localhost:4200','https://google.com']
origin = ['*']
# origin=['my_domain']
app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],
                   )

app.include_router(posts_route.router)
app.include_router(user_route.router)
app.include_router(login.auth_router)
app.include_router(votes_route.vote_router)


@app.get("/")
def root():
	return {"message": "Hello World"}
