from fastapi import HTTPException
from starlette import status

from app.sql_app_post import models
from app.sql_app_post.crud_operations import utils


def get_user_by_email_or_ID(db, email, id):
	try:
		if id:
			user = db.query(models.User).filter(models.User.user_id == id).first()
			if user is not None:
				return user
			else:
				return HTTPException(status_code=400, detail=f"user with id{id} already registered")
		if email:
			user = db.query(models.User).filter(models.User.email == email).first()
			if user is not None:
				return user
			else:
				return HTTPException(status_code=400, detail=f" user with email {email} already registered")
	except Exception as e:
		return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internet server error")


def get_user_by_id(db, id):
	try:
		user = db.query(models.User).filter(models.User.user_id == id).first()
		return user
	except Exception as e:
		return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internet server error")


def get_user_by_email(db, email):
	try:
		user = db.query(models.User).filter(models.User.email == email).first()
		return user
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internet server error")


def create_user(db, user):
	try:
		user.password = utils.get_password_hash(user.password)
		db_user = models.User(**user.dict())
		db.add(db_user)
		db.commit()
		db.refresh(db_user)
		return db_user
	except Exception as e:
		return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internet server error")
