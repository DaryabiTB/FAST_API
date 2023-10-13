from fastapi import APIRouter, Depends, HTTPException, status

from app.sql_app_post.crud_operations import vote_crud
from app.sql_app_post import models, schema
from sqlalchemy.orm import Session
from app.sql_app_post.database import get_db
from app.sql_app_post.routes.oauth2 import get_current_user

vote_router = APIRouter(
	prefix="/votes",
	tags=["vote"]
)


@vote_router.post("/", status_code=status.HTTP_201_CREATED)
def create_vote(vote: schema.VoteCreate, db: Session = Depends(get_db),
                current_user: models.User = Depends(get_current_user)):
	return vote_crud.create_vote(db, vote, current_user.user_id)
