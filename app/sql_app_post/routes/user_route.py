from fastapi import Depends, HTTPException, APIRouter, Query
from sqlalchemy.orm import Session
from starlette import status

from app.sql_app_post import schema
from app.sql_app_post.database import get_db
from app.sql_app_post.crud_operations import user_crud as crud
from app.sql_app_post.routes import oauth2

router = APIRouter(
	prefix="/users",
	tags=["users"]
)


# tested and works fine
@router.post("/", response_model=schema.return_user, status_code=status.HTTP_201_CREATED)
def create_user(user: schema.create_user, db: Session = Depends(get_db)):
	result = crud.get_user_by_email_or_ID(db, email=user.email, id=None)
	if isinstance(result, HTTPException):
		raise result
	result = crud.create_user(db=db, user=user)
	if isinstance(result, HTTPException):
		raise result
	return result


# tested and works fine.
@router.get("/me", response_model=schema.return_user, status_code=status.HTTP_200_OK)
def get_current_loggedIN_user_data(db: Session = Depends(get_db),
                                   current_user: schema.return_user = Depends(oauth2.get_current_user)):
	return current_user

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
