from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str):
	return pwd_context.hash(password)


def verify_password(plain_password, hashed_password1):
	return pwd_context.verify(plain_password, hashed_password1)


def create_access_token(data):
	return None
