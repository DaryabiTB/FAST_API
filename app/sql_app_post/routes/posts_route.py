from typing import List

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from starlette import status
from app.sql_app_post.crud_operations import post_crud as crud
from app.sql_app_post import schema
from app.sql_app_post.database import get_db

router = APIRouter(
	prefix="/posts",
	tags=["posts"]
)


@router.get("/", response_model=list[schema.Post], status_code=status.HTTP_200_OK)
def read_posts(db: Session = Depends(get_db)):
	print("read_posts")
	posts = crud.read_posts(db)
	if posts is not None:
		return posts
	else:
		raise HTTPException(status_code=404, detail={"message": "No data found"})


@router.get("/{id}", response_model=schema.return_post, status_code=status.HTTP_200_OK)
def read_post_by_id(id: int, db: Session = Depends(get_db), skip: int = 0, limit: int | None = None):
	post = crud.read_post_by_id(db, id)
	if post:
		return post
	else:
		raise HTTPException(status_code=404, detail={"message": f"post with ID {id} was not found"})


# tested and works
@router.post("/", response_model=schema.return_post, status_code=status.HTTP_201_CREATED)
def create_post(post: schema.create_post, db: Session = Depends(get_db)):
	created_post = crud.create_post(db, post=post)
	if created_post is None:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
	return created_post


@router.put("/{id}", response_model=schema.return_post, status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, post: schema.create_post, db: Session = Depends(get_db)):
	updated_post = crud.update_post(db, id, post)
	if updated_post is None:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
		                    detail={"message": f"post with ID {id} was not found"})
	return updated_post


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def read_post_by_id(id: int, db: Session = Depends(get_db)):
	post = crud.delete_post_by_id(db, id)
	if post:
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
