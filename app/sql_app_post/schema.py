from datetime import datetime
from typing import List

from pydantic import BaseModel, EmailStr


class create_post(BaseModel):
	title: str
	content: str


class base_user(BaseModel):
	email: EmailStr


class create_user(base_user):
	password: str


class Post(create_post):
	published: bool = False  # float | None = None
	created_at: datetime
	update_at: datetime


class ReturnPost(Post):
	post_id: int
	
	class Config:
		orm_mode = True
		extra = "allow"


class ReturnUser(BaseModel):
	user_id: int
	is_active: bool
	create_at: datetime
	posts: List[ReturnPost] = []
	
	class Config:
		orm_mode = True
		extra = "allow"


# class return_post(Post):
# 	id: int
# 	owner_id: int
# 	owner: return_user
#
# 	class Config:
# 		orm_mode = True
# 		extra = "allow"
#
#
# class return_user(base_user):
# 	id: int
# 	is_active: bool
# 	create_at: datetime
# 	posts: list[return_post] = []
#
# 	class Config:
# 		orm_mode = True
# 		extra = "allow"
#

class UserLogin(BaseModel):
	email: EmailStr
	password: str


class Token(BaseModel):
	access_token: str
	token_type: str


# what we embed in the token
class TokenData(BaseModel):
	email: str = None
