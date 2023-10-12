from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from starlette import status

from app.sql_app_post import models, schema
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.sql_app_post.database import get_db
from config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# login is the path of the token url
oauth2_schema = Depends(OAuth2PasswordBearer(tokenUrl="login"))


def create_access_token(data: dict):
	to_encode = data.copy()
	expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
	to_encode.update({"exp": expire})
	encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
	return encoded_jwt


def verify_token(token: str, credentials_exception):
	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		email: str = payload.get("email")
		if email is None:
			raise credentials_exception
		token_data = schema.TokenData(email=email)
		return token_data
	except JWTError:
		raise credentials_exception


# oauth2_schema is the dependency defined above
def get_current_user(token: str = oauth2_schema, db: Session = Depends(get_db)):
	credentials_exception = HTTPException(
		status_code=status.HTTP_401_UNAUTHORIZED,
		detail="Could not validate credentials",
		headers={"WWW-Authenticate": "Bearer"},
	)
	token = verify_token(token, credentials_exception)
	user = db.query(models.User).filter(models.User.email == token.email).first()
	
	return user
