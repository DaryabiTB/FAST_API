from typing import List

from fastapi import Depends, HTTPException, APIRouter, Request
from sqlalchemy import func
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse

from app.sql_app_post.crud_operations import post_crud as crud
from app.sql_app_post import models, schema
from app.sql_app_post.database import get_db
from app.sql_app_post.routes import oauth2
from app.sql_app_post.routes.oauth2 import get_current_user

router = APIRouter(
	prefix="/posts",
	tags=["posts"]
)


# @router.get("/", response_model=list[schema.return_post] | None, status_code=status.HTTP_200_OK, )
@router.get("/", response_model=list[schema.post_with_vote_count], status_code=status.HTTP_200_OK, )
def get_posts(db: Session = Depends(get_db),
              limit=5, skip=0, search: str = None,
              current_user: schema.return_post = Depends(oauth2.get_current_user)):
	# posts = crud.read_posts(db, current_user_id=current_user.user_id)
	#
	# if len(posts) > 0:
	# 	return posts
	# else:
	# 	raise HTTPException(status_code=404, detail={"message": f"not found any post for user {current_user.email}"})
	#
	# posts = db.query(models.Post).filter(
	# 	models.Post.owner_id == current_user.user_id and models.Post.title.contains(search)).offset(skip).limit(
	# 	limit).all()
	
	# if we run this query , we need to remove the response model from the function definition, otherwise it will throw an error
	result = db.query(models.Post, func.count(models.Vote.post_id).label("votes_count")).join(models.Vote,
	                                                                                          models.Vote.post_id == models.Post.post_id,
	                                                                                          isouter=True).group_by(
		models.Post.post_id).filter(
		models.Post.owner_id == current_user.user_id and models.Post.title.contains(search)).offset(skip).limit(
		limit).all()
	
	return result


@router.get("/{id}", response_model=schema.return_post | None, status_code=status.HTTP_200_OK)
def read_post_by_id(id: int, db: Session = Depends(get_db),
                    current_user: schema.return_post = Depends(oauth2.get_current_user)):
	result = crud.read_post_by_id(db, id, current_user_id=current_user.user_id)
	if isinstance(result, HTTPException):
		raise result
	return result


# tested and works
@router.post("/", response_model=schema.return_post, status_code=status.HTTP_201_CREATED)
def create_post(post: schema.create_post, db: Session = Depends(get_db),
                current_user: schema.return_post = Depends(oauth2.get_current_user)):
	current_user_id = current_user.user_id
	
	created_post = crud.create_post(db, post=post, current_user_id=current_user_id)
	if isinstance(created_post, HTTPException):
		raise created_post
	return created_post


# create_post_schema = {"title" : "", "content":""}
@router.put("/{id}", response_model=schema.return_post, status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, post: schema.create_post, db: Session = Depends(get_db),
                current_user: schema.return_post = Depends(oauth2.get_current_user)):
	current_user_id = current_user.user_id
	result = crud.update_post(db, id, post, current_user_id)
	if isinstance(result, HTTPException):
		raise result
	return result


#
# @router.put("/{id}", response_model=schema.ReturnPost, status_code=status.HTTP_202_ACCEPTED)
# def update_post(id: int, post: schema.create_post, db: Session = Depends(get_db),
#                 current_user: schema.ReturnPost = Depends(oauth2.get_current_user)):
# 	current_user_id = current_user.user_id
# 	if current_user_id != post.owner_id:
# 		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
# 		                    detail="You are not authorized to update this post")
# 	updated_post = crud.update_post(db, id, post)
# 	if updated_post is None:
# 		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
# 		                    detail={"message": f"post with ID {id} was not found"})
# 	return updated_post


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_post_by_id(id: int, db: Session = Depends(get_db),
                      current_user: schema.return_post = Depends(oauth2.get_current_user)):
	result = crud.delete_post_by_id(db, id, current_user_id=current_user.user_id)
	if isinstance(result, HTTPException):
		raise result
	return result

# @router.post("/posts_lists/", response_model=List[schema.return_post], status_code=status.HTTP_201_CREATED)
# def create_post(post: list[schema.create_post], db: Session = Depends(get_db)):
# 	post_created = []
# 	for post in post:
# 		created_post = crud.create_post(db, post=post)
# 		if created_post is None:
# 			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
# 		post_created.append(created_post)
#
# 	return post_created
