import json
from datetime import date
from uuid import uuid4

from backend.models.user import (
    User,
    UserResponse,
    UserCreate
)

from backend.models.chat import(
	Chat,
    ChatCollection,
    ChatResponse
)


# Open 'db' and begin reading the json file
with open("backend/fake_db.json", "r") as f:
    DB = json.load(f)
    
def get_all_users() -> list[User]:
    return [User(**user_data) for user_data in DB["users"].values()]

def get_user_by_id(user_id: str) -> User:
    if user_id in DB["users"]:
        return User(**DB["users"][user_id])
    
	# TODO: raise exception


def create_user(user_create: UserCreate) -> User:
    user = User(
		created_at=date.today(),
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
			
	return chats
