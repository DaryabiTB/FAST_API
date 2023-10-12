from datetime import datetime

from pydantic import BaseModel, EmailStr


class create_post(BaseModel):
	title: str
	content: str


class Post(create_post):
	published: bool = False  # float | None = None
	created_at: datetime
	update_at: datetime


class return_post(Post):
	id: int
	
	class Config:
		orm_mode = True
		extra = "allow"


class base_user(BaseModel):
	email: EmailStr


class create_user(base_user):
	password: str


class return_user(base_user):
	id: int
	is_active: bool
	create_at: datetime
	
	class Config:
		orm_mode = True
		extra = "allow"


class UserLogin(BaseModel):
	email: EmailStr
	password: str


class Token(BaseModel):
	access_token: str
	token_type: str


# what we embed in the token
class TokenData(BaseModel):
	email: str = None
