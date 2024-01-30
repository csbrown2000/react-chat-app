from fastapi import APIRouter
from typing import Literal

from backend import database as db

from backend.models.user import (
	User,
	UserCollection,
	UserResponse,
	UserCreate
)

from backend.models.chat import(
	ChatCollection
)

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.get("",
				  response_model=UserCollection,
				  description="Retrieve a collection of users from the database.")
def get_users(
	sort: Literal["id", "created_at"] = "id"
):
	"""
	Retrieve a collection of users from the database.

	Args:
		sort (Literal["id", "created_at"], optional): The field to sort the users by. Defaults to "id".

	Returns:
		UserCollection: The collection of users, sorted by the specified field.
	"""
	sort_key = lambda user: getattr(user, sort)
	users = db.get_all_users()

	return UserCollection(
		meta={"count": len(users)},
		users=sorted(users, key=sort_key)
	)


@users_router.get("/{user_id}",
				  response_model=UserResponse,
				  description="Retrieve a user by their ID.")
def get_user_by_id(user_id: str):
	"""
	Retrieve a user by their ID.

	Args:
		user_id (str): The ID of the user to retrieve.

	Returns:
		UserResponse: The response containing the user information.
	"""
	return UserResponse(user=db.get_user_by_id(user_id))


@users_router.post("",
				   response_model=UserResponse,
				   description="Create a new user.")
def create_user(user_create: UserCreate):
	"""
	Create a new user.

	Args:
		user_create (UserCreate): The user data to create.

	Returns:
		UserResponse: The response containing the created user.
	"""
	return UserResponse(user=db.create_user(user_create))


@users_router.get("/{user_id}/chats",
				  response_model=ChatCollection,
				  description="Retrieve the chats for a specific user.")
def get_user_chats(user_id: str, 
				   sort: Literal["name", "id", "created_at"] = "name"):
	"""
	Retrieve the chats for a specific user.

	Args:
		user_id (str): The ID of the user.
		sort (Literal["name", "id", "created_at"], optional): The field to sort the chats by. Defaults to "name".

	Returns:
		ChatCollection: The collection of chats for the user, sorted based on the specified field.
	"""
	sort_key = lambda chat: getattr(chat, sort)
	chats = db.get_user_chats(user_id)
	return ChatCollection(
		meta={"count": len(chats)},
		chats=sorted(chats, key=sort_key)
	)