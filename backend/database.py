import json
import os
from datetime import datetime
from uuid import uuid4
from sqlmodel import Session, SQLModel, create_engine, select
from fastapi import HTTPException

from backend.models.entities import (
	UserInDB,
	UserChatLinkInDB,
	ChatInDB,
	MessageInDB
)
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
	MessageCollection,
	MessageCreate,
	MessageResponse
)

if os.environ.get("DB_LOCATION") == "RDS":
    username = os.environ.get("PG_USERNAME")
    password = os.environ.get("PG_PASSWORD")
    endpoint = os.environ.get("PG_ENDPOINT")
    port = os.environ.get("PG_PORT")
    db_url = f"postgresql://{username}:{password}@{endpoint}:{port}/{username}"
    echo = False
    connect_args = {}
else:
    db_url = "sqlite:///backend/pony_express.db"
    echo = True
    connect_args = {"check_same_thread": False}

engine = create_engine(
    db_url,
    echo=echo,
    connect_args=connect_args,
)

engine = create_engine(
	"sqlite:///backend/pony_express.db",
	echo=True,
	connect_args={"check_same_thread": False},
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

# Open 'db' and begin reading the json file
with open("backend/fake_db.json", "r") as f:
    DB = json.load(f)
    
def get_all_users(session: Session) -> list[UserInDB]:
	"""
	Retrieve all users from the database.

	Returns:
		list[User]: A list of User objects representing all the users in the database.
	"""
	return session.exec(select(UserInDB)).all()

def get_user_by_id(session: Session, user_id: int) -> UserInDB:
	"""
	Retrieve a user from the database based on their ID.

	Args:
		user_id (str): The ID of the user to retrieve.

	Returns:
		User: The user object corresponding to the given ID.

	Raises:
		EntityNotFoundException: If the user with the given ID does not exist in the database.
	"""
	user = session.get(UserInDB, user_id)
	if user:
		return user
	raise EntityNotFoundException(entity_name="User", entity_id=user_id)


def create_user(session: Session, user_create: UserCreate) -> UserInDB:
	"""
	Creates a new user in the database.

	Args:
		user_create (UserCreate): The user creation data.

	Returns:
		User: The created user object.

	Raises:
		DuplicateEntityException: If a user with the same ID already exists in the database.
	"""
	try:
		user = UserInDB(**user_create.model_dump())
		session.add(user)
		session.commit()
		session.refresh(user)
		return user
	except:
		raise DuplicateEntityException(entity_name="User", entity_id=user_create.id)
	

def get_user_chats(session: Session, user_id: int) -> list[ChatInDB]:
	"""
	Retrieves the chats associated with a given user ID.

	Args:
		user_id (str): The ID of the user.

	Returns:
		list[Chat]: A list of Chat objects associated with the user.

	Raises:
		EntityNotFoundException: If no chats are found for the given user ID.
	"""
	user = session.get(UserInDB, user_id)
	if user:
		return user.chats
	raise EntityNotFoundException(entity_name="User", entity_id=user_id)



def get_all_chats(session: Session) -> list[ChatInDB]:
	"""
	Retrieve all chats from the database.

	Returns:
		list[Chat]: A list of Chat objects representing all the chats in the database.
	"""
	return session.exec(select(ChatInDB)).all()

def get_chat_by_id(session: Session, chat_id: int) -> ChatInDB:
	"""
	Retrieve a chat object by its ID.

	Args:
		chat_id (str): The ID of the chat.

	Returns:
		Chat: The chat object corresponding to the given ID.

	Raises:
		EntityNotFoundException: If the chat with the given ID does not exist.
	"""

	chat = session.get(ChatInDB, chat_id)
	if chat:
		return chat
	raise EntityNotFoundException(entity_name="Chat", entity_id=chat_id)

def update_chat(session: Session, chat_id: int, chat_update: ChatUpdate) -> ChatInDB:
	"""
	Update the chat with the given chat_id using the provided chat_update.

	Args:
		chat_id (str): The ID of the chat to be updated.
		chat_update (ChatUpdate): The updated chat information.

	Returns:
		Chat: The updated chat object.
	"""
	chat = get_chat_by_id(session, chat_id)
	for attr, value in chat_update.model_dump(exclude_unset=True).items():
		setattr(chat, attr, value)

	session.add(chat)
	session.commit()
	session.refresh(chat)
	return chat

def delete_chat(session: Session, chat_id: int):
	"""
	Deletes a chat from the database.

	Args:
		chat_id (str): The ID of the chat to be deleted.

	Returns:
		None
	"""

	chat = get_chat_by_id(session, chat_id)
	session.delete(chat)
	session.commit()

def get_messages_by_id(session: Session, chat_id: int) -> list[MessageInDB]:
	"""
	Retrieves a list of messages by chat ID.

	Args:
		chat_id (str): The ID of the chat.

	Returns:
		list[Message]: A list of Message objects.

	Raises:
		EntityNotFoundException: If the chat ID is not found in the database.
	"""

	return session.exec(select(MessageInDB).where(MessageInDB.chat_id == chat_id)).all()
	raise EntityNotFoundException(entity_name="Chat", entity_id=chat_id)

def get_users_in_chat(session: Session, chat_id: int) -> list[UserInDB]:
	"""
	Retrieves a list of users in a chat based on the chat ID.

	Args:
		chat_id (str): The ID of the chat.

	Returns:
		list[User]: A list of User objects representing the users in the chat.

	Raises:
		EntityNotFoundException: If the chat with the specified ID does not exist.
	"""
	chat = session.get(ChatInDB, chat_id)
	if chat:
		return chat.users
	raise EntityNotFoundException(entity_name="Chat", entity_id=chat_id)

def create_new_message(session: Session, message_create: MessageCreate, user: UserInDB, chat_id: int) -> MessageResponse:
	try:
		message = MessageInDB(text=message_create.text,
						user_id=user.id,
						chat_id=chat_id)
		session.add(message)
		session.commit()
		session.refresh(message)
		return MessageResponse(message=message)
	except:
		pass

class AuthException(HTTPException):
    def __init__(self, error: str, entity_name: str, entity_field: str, entity_value: str):
        super().__init__(
            status_code=422,
            detail={
                "type": error,
                "entity_name": entity_name,
                "entity_field": entity_field,
                "entity_value": entity_value
            },
        )

class DuplicateUsernameException(AuthException):
    def __init__(self, value:str):
        super().__init__(
            error="duplicate_value",
            entity_name="User",
			entity_field="username",
			entity_value=value
        )

class DuplicateEmailException(AuthException):
    def __init__(self, value:str):
        super().__init__(
            error="duplicate_value",
            entity_name="User",
			entity_field="email",
			entity_value=value
        )


def check_credentials_exist(session: Session, user_name: str, user_email: str):
	username = session.exec(select(UserInDB).where(UserInDB.username == user_name)).first()
	print("username", username)
	if username:
		raise DuplicateUsernameException(value=user_name)
	else:
		email = session.exec(select(UserInDB).where(UserInDB.email == user_email)).first()
		print("email", email)
		if email:
			raise DuplicateEmailException(value=user_email)
		return False