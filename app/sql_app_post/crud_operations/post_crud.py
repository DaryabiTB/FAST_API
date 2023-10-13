from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.sql_app_post import models, schema
from starlette import status


def create_post(db: Session, post: schema.create_post, current_user_id: int):
	try:
		db_post = models.Post(owner_id=current_user_id, **post.dict())
		db.add(db_post)
		db.commit()
		db.refresh(db_post)
		return db_post
	except Exception as e:
		return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internet server error")


def read_posts(db: Session, current_user_id: int):
	posts = db.query(models.Post).filter(models.Post.owner_id == current_user_id).all()
	return posts


def read_post_by_id(db: Session, id: int, current_user_id: int):
	try:
		post = db.query(models.Post).filter(models.Post.id == id and models.Post.owner_id == current_user_id).first()
		if not post:
			return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
			                     detail="You are not authorized to access this post")
		return post
	except Exception as e:
		return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internet server error")


def delete_post_by_id(db: Session, id: int, current_user_id: int):
	try:
		post = db.query(models.Post).filter(models.Post.id == id).first()
		if post is None:
			return HTTPException(status_code=404, detail={"message": f"post with ID {id} was not found"})
		if post.owner_id != current_user_id:
			return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
			                     detail="You are not authorized to delete this post")
		db.query(models.Post).filter(models.Post.id == id).delete(synchronize_session=False)
		db.commit()
		return post
	
	except HTTPException as e:
		print("exception", e)
		return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internet server error")


#


def update_post(db, id, post, current_user_id):
	try:
		if current_user_id != post.owner_id:
			return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
			                     detail="You are not authorized to update this post")
		
		post_query = db.query(models.Post).filter(models.Post.id == id)
		existing_post = post_query.first()
		
		if not existing_post:
			return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
			                     detail={"message": f"Post with ID {id} was not found"})
		
		# Update the existing post with the new data
		post_query.update(post.dict(), synchronize_session=False)
		db.commit()
		db.refresh(existing_post)
		
		return existing_post
	except Exception as e:
		print("exception", e)
		return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

# def update_post(db, id, updated_post):
#     try:
# 	    # post = models.Post(**post.dict())
# 	    # post.update_at = datetime.now()
# 	    post_query = db.query(models.Post).filter(models.Post.id == id)
# 	    post = post_query.first()
# 	    if post:
# 		    post_query.update(updated_post.dict(), synchronize_session=False)
# 		    db.commit()
# 		    db.refresh(post)
# 		    return post
# 	    else:
# 		    return None
#     except Exception as e:
# 	    print("exception", e)
# 	    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internet server error")
