from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.sql_app_post import models, schema
from starlette import status


def create_post(db: Session, post: schema.create_post):
	db_post = models.Post(**post.dict())
	db.add(db_post)
	db.commit()
	db.refresh(db_post)
	return db_post


def read_posts(db: Session):
	try:
		posts = db.query(models.Post).all()
		if posts:
			return posts
		else:
			return {"message": "No data found"}
	except Exception as e:
		return None


def read_post_by_id(db: Session, id: int):
	try:
		post = db.query(models.Post).filter(models.Post.id == id).first()
		if post:
			return post
		else:
			print("read_post_by_id", None)
			return None
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internet server error")


def delete_post_by_id(db: Session, id: int):
	try:
		post = db.query(models.Post).filter(models.Post.id == id).first()
		if post:
			db.query(models.Post).filter(models.Post.id == id).delete(synchronize_session=False)
			db.commit()
			return post
		else:
			return None
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internet server error")


#
def update_post(db, id, updated_post):
	try:
		# post = models.Post(**post.dict())
		# post.update_at = datetime.now()
		post_query = db.query(models.Post).filter(models.Post.id == id)
		post = post_query.first()
		if post:
			post_query.update(updated_post.dict(), synchronize_session=False)
			db.commit()
			db.refresh(post)
			return post
		else:
			return None
	except Exception as e:
		print("exception", e)
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internet server error")
