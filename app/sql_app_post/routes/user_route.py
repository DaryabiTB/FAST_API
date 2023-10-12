from fastapi import Depends, HTTPException, APIRouter, Query
from sqlalchemy.orm import Session
from starlette import status

from app.sql_app_post import schema
from app.sql_app_post.database import get_db
from app.sql_app_post.crud_operations import user_crud as crud

router = APIRouter(
	prefix="/users",
	tags=["users"]
)


@router.post("/", response_model=schema.return_user, status_code=status.HTTP_201_CREATED)
def create_user(user: schema.create_user, db: Session = Depends(get_db)):
	db_user = crud.get_user_by_email_or_ID(db, email=user.email, id=None)
	if db_user:
		raise HTTPException(status_code=400, detail="Email already registered")
	return crud.create_user(db=db, user=user)


@router.get("/", response_model=schema.return_user, status_code=status.HTTP_200_OK)
def read_user(user_identifier: str = Query(..., title="User Identifier (Email or ID)"), db: Session = Depends(get_db)):
	if user_identifier.isdigit():
		# If the user_identifier is a number (assumed to be an ID), query by ID
		db_user = crud.get_user_by_email_or_ID(db, email=None, id=int(user_identifier))
	else:
		# Otherwise, assume it's an email and query by email
		db_user = crud.get_user_by_email_or_ID(db, email=user_identifier, id=None)
	
	if db_user is None:
		raise HTTPException(status_code=404, detail="User not found")
	return db_user

# @app.get("/users/{user_email}", response_model=schema.return_user, status_code=status.HTTP_200_OK)
# def read_user(user_email: str, db: Session = Depends(get_db)):
# 	db_user = crud.get_user_by_email(db, email=user_email, id=None)
# 	if db_user is None:
# 		raise HTTPException(status_code=404, detail="User not found")
# 	return db_user


# @app.get("/users/{id}", response_model=schema.return_user, status_code=status.HTTP_200_OK)
# def read_user(id: int, db: Session = Depends(get_db)):
# 	db_user = crud.get_user_by_email(db, email=None, id=id)
# 	if db_user is None:
# 		raise HTTPException(status_code=404, detail="User not found")
# 	return db_user
