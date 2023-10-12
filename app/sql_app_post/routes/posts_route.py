from typing import List

from fastapi import Depends, HTTPException, APIRouter, Request
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse

from app.sql_app_post.crud_operations import post_crud as crud
from app.sql_app_post import schema
from app.sql_app_post.database import get_db
from app.sql_app_post.routes import oauth2
from app.sql_app_post.routes.oauth2 import get_current_user

router = APIRouter(
	prefix="/posts",
	tags=["posts"]
)


@router.get("/", response_model=list[schema.ReturnPost] | None, status_code=status.HTTP_200_OK, )
def read_posts(db: Session = Depends(get_db), current_user: schema.ReturnPost = Depends(oauth2.get_current_user)):
	posts = crud.read_posts(db, current_user_id=current_user.user_id)
	
	if len(posts) > 0:
		return posts
	else:
		raise HTTPException(status_code=404, detail={"message": f"not found any post for user {current_user.email}"})


@router.get("/{id}", response_model=schema.ReturnPost, status_code=status.HTTP_200_OK)
def read_post_by_id(id: int, db: Session = Depends(get_db),
                    current_user: schema.ReturnPost = Depends(oauth2.get_current_user)):
	post = crud.read_post_by_id(db, id, current_user_id=current_user.user_id)
	if post:
		return post
	else:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
		                    detail="You are not authorized to access this post")


# tested and works
@router.post("/", response_model=schema.ReturnPost, status_code=status.HTTP_201_CREATED)
def create_post(post: schema.create_post, db: Session = Depends(get_db),
                current_user: schema.ReturnPost = Depends(oauth2.get_current_user)):
	current_user_id = current_user.user_id
	
	created_post = crud.create_post(db, post=post, current_user_id=current_user_id)
	if created_post is None:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
	return created_post


@router.put("/{id}", response_model=schema.ReturnPost, status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, post: schema.create_post, db: Session = Depends(get_db),
                current_user: schema.ReturnPost = Depends(oauth2.get_current_user)):
	current_user_id = current_user.user_id
	if current_user_id != post.owner_id:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
		                    detail="You are not authorized to update this post")
	updated_post = crud.update_post(db, id, post)
	if updated_post is None:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
		                    detail={"message": f"post with ID {id} was not found"})
	return updated_post


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_post_by_id(id: int, db: Session = Depends(get_db),
                      current_user: schema.ReturnPost = Depends(oauth2.get_current_user)):
	post = crud.delete_post_by_id(db, id, current_user_id=current_user.user_id)
	if post == -2:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
		                    detail="You are not authorized to delete this post")
	if post is not None:
		return {"message": f"post with ID {id} was deleted"}
	else:
		raise HTTPException(status_code=404, detail={"message": f"post with ID {id} was not found"})

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
