from datetime import datetime
from pydantic import BaseModel, EmailStr, conint


# items listed inside the schema should Match the database Model.
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


class return_post(Post):
	post_id: int
	owner_id: int
	
	class Config:
		orm_mode = True
		extra = "allow"


class return_user(base_user):
	user_id: int
	is_active: bool
	create_at: datetime
	posts: list[return_post] = []
	
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


class vote_post_id(BaseModel):
	post_id: int


class VoteCreate(BaseModel):
	post_id: int
	vote_dir: conint(ge=0, le=1)


class return_vote(vote_post_id):
	vote_at: datetime
	user_id: int
	
	class Config:
		orm_mode = True
		extra = "allow"


class post_with_vote_count(BaseModel):
	Post: Post
	votes_count: int
