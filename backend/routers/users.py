from fastapi import APIRouter, Depends
from typing import Literal
from sqlmodel import Session
from backend import database as db
from backend.models.user import (
	User,
	UserCollection,
	UserResponse,
	UserCreate,
	UserUpdate
)
from backend.models.chat import(
	ChatCollection
)
from backend.models.entities import UserInDB
from backend.auth import get_current_user

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.get("",
				  response_model=UserCollection,
				  description="Retrieve a collection of users from the database.")
def get_users(
	sort: Literal["id", "created_at"] = "id",
	session: Session = Depends(db.get_session)
):
	"""
	Retrieve a collection of users from the database.

	Args:
		sort (Literal["id", "created_at"], optional): The field to sort the users by. Defaults to "id".

	Returns:
		UserCollection: The collection of users, sorted by the specified field.
	"""
	sort_key = lambda user: getattr(user, sort)
	users = db.get_all_users(session)

	return UserCollection(
		meta={"count": len(users)},
		users=sorted(users, key=sort_key)
	)

@users_router.get("/me",
				  response_model=UserResponse,
				  description="Retrieves the current user.")
def get_curr_user(user: UserInDB = Depends(get_current_user)):
	return UserResponse(user=user)

@users_router.put("/me",
				  response_model=UserResponse,
				  description="Retrieves the current user.")
def update_curr_user(user_update: UserUpdate,
					user: UserInDB = Depends(get_current_user), 
				  session: Session = Depends(db.get_session)):
	user = db.get_user_by_id(session, user.id)
	for attr, value in user_update.model_dump(exclude_unset=True).items():
		setattr(user, attr, value)
	session.add(user)
	session.commit()
	session.refresh(user)
	return user

@users_router.get("/{user_id}",
				  response_model=UserResponse,
				  description="Retrieve a user by their ID.")
def get_user_by_id(user_id: int, session: Session = Depends(db.get_session)):
	"""
	Retrieve a user by their ID.

	Args:
		user_id (str): The ID of the user to retrieve.

	Returns:
		UserResponse: The response containing the user information.
	"""
	return UserResponse(user=db.get_user_by_id(session, user_id))


def create_user(user_create: UserCreate, session: Session = Depends(db.get_session)):
	"""
	Create a new user.

	Args:
		user_create (UserCreate): The user data to create.

	Returns:
		UserResponse: The response containing the created user.
	"""
	return UserResponse(user=db.create_user(session, user_create))


@users_router.get("/{user_id}/chats",
				  response_model=ChatCollection,
				  description="Retrieve the chats for a specific user.")
def get_user_chats(user_id: int, 
				   sort: Literal["name", "id", "created_at"] = "name",
				   session: Session = Depends(db.get_session)):
	"""
	Retrieve the chats for a specific user.

	Args:
		user_id (str): The ID of the user.
		sort (Literal["name", "id", "created_at"], optional): The field to sort the chats by. Defaults to "name".

	Returns:
		ChatCollection: The collection of chats for the user, sorted based on the specified field.
	"""
	sort_key = lambda chat: getattr(chat, sort)
	chats = db.get_user_chats(session, user_id)
	return ChatCollection(
		meta={"count": len(chats)},
		chats=sorted(chats, key=sort_key)
	)