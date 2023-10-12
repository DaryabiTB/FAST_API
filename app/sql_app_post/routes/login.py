from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.sql_app_post import models
from app.sql_app_post.database import get_db
from app.sql_app_post.crud_operations import utils
from app.sql_app_post.crud_operations import user_crud
from app.sql_app_post import schema
from . import oauth2  # a module in the same directory

auth_router = APIRouter(
	tags=['Authentication'])


@auth_router.post('/login', status_code=status.HTTP_200_OK, response_model=schema.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
	# OAuth2PasswordRequestForm is a class that has username and password as attributes
	user = user_crud.get_user_by_email_or_ID(db, user_credentials.username, id=None)
	if not user:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
	if not utils.verify_password(user_credentials.password, user.password):
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
	# email will be used as the payload for the access token
	access_token = oauth2.create_access_token(data={"email": user.email})
	return {"access_token": access_token, "token_type": "bearer"}
