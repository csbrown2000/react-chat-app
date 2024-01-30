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

@chats_router.get("", response_model=ChatCollection)
def get_all_chats(sort: Literal["id", "created_at", "name"] = "name"):
	sort_key = lambda chat: getattr(chat, sort)
	chats = db.get_all_chats()

	return ChatCollection(
		meta={"count": len(chats)},
		chats=sorted(chats, key=sort_key)
	)


@chats_router.get("/{chat_id}", response_model=ChatResponse)
def get_chat_by_id(chat_id: str):
	return ChatResponse(chat=db.get_chat_by_id(chat_id))

@chats_router.put("/{chat_id}", response_model=ChatResponse)
def update_chat(chat_id: str, chat_update: ChatUpdate):
	return ChatResponse(chat=db.update_chat(chat_id, chat_update))

@chats_router.delete("/{chat_id}", status_code=204, response_model=None)
def delete_chat(chat_id: str):
	db.delete_chat(chat_id)


@chats_router.get("/{chat_id}/messages", response_model=MessageCollection)
def get_messages_by_chat_id(
		chat_id: str,
		sort: Literal["id", "created_at", "text", "user_id"] = "created_at"
		):
	sort_key = lambda message: getattr(message, sort)
	messages = db.get_messages_by_id(chat_id)
	return MessageCollection(
		meta={"count": len(messages)},
		messages=sorted(messages, key=sort_key)
	)
	
# TODO: Get users from specified chat id
@chats_router.get("/{chat_id}/users", response_model=UserCollection)
def get_users_in_chat(chat_id: str,
					  sort: Literal["id", "created_at"] = "id"):
	sort_key = lambda user: getattr(user, sort)
	users = db.get_users_in_chat(chat_id)
	return UserCollection(
		meta={"count": len(users)},
		users=sorted(users, key=sort_key)
	)

