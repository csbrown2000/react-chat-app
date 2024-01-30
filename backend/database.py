import json
from datetime import datetime
from uuid import uuid4

from backend.models.exception import EntityNotFoundException, DuplicateEntityException
from backend.models.user import (
    User,
    UserResponse,
    UserCreate
)
from backend.models.chat import(
	Chat,
    ChatCollection,
    ChatResponse,
    ChatUpdate,
	Message,
	MessageCollection
)



# Open 'db' and begin reading the json file
with open("backend/fake_db.json", "r") as f:
    DB = json.load(f)
    
def get_all_users() -> list[User]:
    return [User(**user_data) for user_data in DB["users"].values()]

def get_user_by_id(user_id: str) -> User:
    if user_id in DB["users"]:
        return User(**DB["users"][user_id])
    raise EntityNotFoundException(entity_name="User", entity_id=user_id)


def create_user(user_create: UserCreate) -> User:
	if user_create.id in DB["users"]:
		raise DuplicateEntityException(entity_name="User", entity_id=user_create.id)
	else:
		user = User(
			created_at=datetime.now(),
			**user_create.model_dump()
		)
		DB["users"][user.id] = user.model_dump()
		return user
		
	

def get_user_chats(user_id: str) -> list[Chat]:
	chats = list()
	for chat_data in DB["chats"].values():
		if user_id in chat_data["user_ids"]:
			list.append(chats, Chat(
                        id=chat_data["id"],
                        name=chat_data["name"],
                        user_ids=chat_data["user_ids"],
                        owner_id=chat_data["owner_id"],
                        created_at=chat_data["created_at"]
			))
	if (len(chats) == 0):
		raise EntityNotFoundException(entity_name="User", entity_id=user_id)
	else:
		return chats


def get_all_chats() -> list[Chat]:
    return [Chat(**chat_data) for chat_data in DB["chats"].values()]

def get_chat_by_id(chat_id: str) -> Chat:
	if chat_id in DB["chats"]:
		chat_data = DB["chats"][chat_id]
		return Chat(
			id=chat_data["id"],
			name=chat_data["name"],
			user_ids=chat_data["user_ids"],
			owner_id=chat_data["owner_id"],
			created_at=chat_data["created_at"]
		)
	
	raise EntityNotFoundException(entity_name="Chat", entity_id=chat_id)

def update_chat(chat_id: str, chat_update: ChatUpdate) -> Chat:
	chat = get_chat_by_id(chat_id)
	setattr(chat, "name", chat_update)
	return chat

def delete_chat(chat_id: str):
      chat = get_chat_by_id(chat_id)
      del DB["chats"][chat_id]

def get_messages_by_id(chat_id: str) -> list[Message]:
	messages = list()
	if chat_id in DB["chats"]:
		for message_data in DB["chats"][chat_id]["messages"]:
			list.append(messages, Message(
				id=message_data["id"],
				user_id=message_data["user_id"],
				text=message_data["text"],
				created_at=message_data["created_at"]
			))
		return messages
	raise EntityNotFoundException(entity_name="Chat", entity_id=chat_id)

def get_users_in_chat(chat_id: str) -> list[User]:
	users = list()
	if chat_id in DB["chats"]:
		for user_data in DB["chats"][chat_id]["user_ids"]:
			list.append(users, get_user_by_id(user_data))
		return users