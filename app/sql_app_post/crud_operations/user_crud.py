from fastapi import HTTPException
from starlette import status

from app.sql_app_post import models
from app.sql_app_post.crud_operations import utils


def get_user_by_email_or_ID(db, email, id):
	try:
		user = None
		if id:
			user = db.query(models.User).filter(models.User.user_id == id).first()
		if email:
			user = db.query(models.User).filter(models.User.email == email).first()
		if user:
			return user
		else:
			return None
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
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internet server error")
