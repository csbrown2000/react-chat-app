from pydantic import BaseModel, Field
from datetime import datetime
from sqlmodel import SQLModel
from typing import Optional

from backend.models.meta import MetaData

class User(SQLModel):
	"""
	Represents a user in the system.

	Attributes:
		id (str): The unique identifier for the user.
		created_at (datetime): The timestamp when the user was created.
	"""
	id: int
	username: str
	email: str
	created_at: datetime

class UserCollection(BaseModel):
	"""
	Represents a collection of users.

	Attributes:
		count (MetaData): The metadata about the count of users.
		user (list[User]): The list of User objects.
	"""
	meta: MetaData
	users: list[User]

class UserList(BaseModel):
	users: list[User]

class UserCreate(BaseModel):
	"""
	Represents a user creation model.

	Attributes:
		id (str): The ID of the user.
	"""
	id: int


class UserResponse(BaseModel):
	"""
	Represents a response containing a user object.
	
	Attributes:
		user (User): The user object.
	"""
	user: User

class UserUpdate(BaseModel):
	username: Optional[str] = Field(default=None)
	email: Optional[str] = Field(default=None)