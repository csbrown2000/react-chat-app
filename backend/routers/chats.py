from fastapi import APIRouter
from typing import Literal
from backend import database as db

from backend.models.chat import (
	Chat,
	ChatCollection,
	ChatResponse,
	ChatUpdate,
	Message,
	MessageCollection
)

from backend.models.user import UserCollection

chats_router = APIRouter(prefix="/chats", tags=["Chats"])

@chats_router.get("",
				  response_model=ChatCollection,
				  description="Retrieve all chats and sort them based on the specified attribute.")
def get_all_chats(sort: Literal["id", "created_at", "name"] = "name"):
	"""
	Retrieve all chats and sort them based on the specified attribute.

	Args:
		sort (Literal["id", "created_at", "name"], optional): The attribute to sort the chats by. Defaults to "name".

	Returns:
		ChatCollection: A collection of chats, sorted based on the specified attribute.
	"""
	sort_key = lambda chat: getattr(chat, sort)
	chats = db.get_all_chats()

	return ChatCollection(
		meta={"count": len(chats)},
		chats=sorted(chats, key=sort_key)
	)


@chats_router.get("/{chat_id}",
				  response_model=ChatResponse,
				  description="Retrieve a chat by its ID.")
def get_chat_by_id(chat_id: str):
	"""
	Retrieve a chat by its ID.

	Parameters:
	- chat_id (str): The ID of the chat to retrieve.

	Returns:
	- ChatResponse: The response containing the chat information.
	"""
	return ChatResponse(chat=db.get_chat_by_id(chat_id))

@chats_router.put("/{chat_id}",
				  response_model=ChatResponse,
				  description="Update a chat with the given chat_id.")
def update_chat(chat_id: str, chat_update: ChatUpdate):
	"""
	Update a chat with the given chat_id.

	Args:
		chat_id (str): The ID of the chat to be updated.
		chat_update (ChatUpdate): The updated chat information.

	Returns:
		ChatResponse: The response containing the updated chat information.
	"""
	return ChatResponse(chat=db.update_chat(chat_id, chat_update))

@chats_router.delete("/{chat_id}",
					 status_code=204,
					 response_model=None,
					 description="Deletes a chat with the given chat_id from the database.")
def delete_chat(chat_id: str):
	"""
	Deletes a chat with the given chat_id from the database.

	Parameters:
	- chat_id (str): The ID of the chat to be deleted.

	Returns:
	- None

	"""
	db.delete_chat(chat_id)


@chats_router.get("/{chat_id}/messages",
				  response_model=MessageCollection,
				  description="Get messages by chat ID and sort them based on the specified attribute.")
def get_messages_by_chat_id(
		chat_id: str,
		sort: Literal["id", "created_at", "text", "user_id"] = "created_at"
		):
	"""
	Get messages by chat ID and sort them based on the specified attribute.

	Parameters:
	- chat_id (str): The ID of the chat.
	- sort (Literal["id", "created_at", "text", "user_id"], optional): The attribute to sort the messages by. Defaults to "created_at".

	Returns:
	- MessageCollection: A collection of messages with metadata.

	"""
	sort_key = lambda message: getattr(message, sort)
	messages = db.get_messages_by_id(chat_id)
	return MessageCollection(
		meta={"count": len(messages)},
		messages=sorted(messages, key=sort_key)
	)
	
@chats_router.get("/{chat_id}/users",
				  response_model=UserCollection,
				  description="Get the users in a chat.")
def get_users_in_chat(chat_id: str,
					  sort: Literal["id", "created_at"] = "id"):
	"""
	Get the users in a chat.

	Parameters:
	- chat_id (str): The ID of the chat.
	- sort (Literal["id", "created_at"], optional): The field to sort the users by. Defaults to "id".

	Returns:
	- UserCollection: A collection of users in the chat, sorted based on the specified field.
	"""
	sort_key = lambda user: getattr(user, sort)
	users = db.get_users_in_chat(chat_id)
	return UserCollection(
		meta={"count": len(users)},
		users=sorted(users, key=sort_key)
	)

