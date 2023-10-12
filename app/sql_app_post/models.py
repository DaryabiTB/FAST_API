from datetime import datetime

from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text

from app.sql_app_post.database import Base


class Post(Base):
	__tablename__ = "posts"
	
	id = Column(Integer, primary_key=True, index=True, autoincrement=True)
	title = Column(String, index=True)
	content = Column(String, nullable=False)
	published = Column(Boolean, server_default='TRUE', default=False)
	created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
	update_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
	
	def as_dict(self):
		return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class User(Base):
	__tablename__ = "users"
	
	id = Column(Integer, primary_key=True, index=True, autoincrement=True)
	email = Column(String, unique=True)
	password = Column(String, nullable=False)
	create_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
	is_active = Column(Boolean, server_default='TRUE', default=True)
