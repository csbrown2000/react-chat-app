from pydantic import BaseModel
from datetime import datetime
from sqlmodel import SQLModel

from backend.models.meta import MetaData
from backend.models.user import User

class Chat(SQLModel):
	"""
	Represents a chat room.

	Attributes:
		id (str): The unique identifier of the chat.
		name (str): The name of the chat.
		user_ids (list[str]): The list of user IDs participating in the chat.
		owner_id (str): The ID of the chat owner.
		created_at (datetime): The timestamp when the chat was created.
	"""
	id: int
	name: str
	owner: User
	created_at: datetime

class ChatCollection(BaseModel):
	"""
	Represents a collection of chat objects.
	
	Attributes:
		meta (MetaData): The metadata associated with the chat collection.
		chats (list[Chat]): The list of chat objects in the collection.
	"""
	meta: MetaData
	chats: list[Chat]

class ChatResponse(BaseModel):
	"""
	Represents a chat response object.

	Attributes:
		chat (Chat): The chat object associated with the response.
	"""
	chat: Chat

class ChatUpdate(BaseModel):
	"""
	Represents an update for a chat.

	Attributes:
		name (str): The updated name of the chat.
	"""
	name: str

class Message(SQLModel):
	id: int
	text: str
	chat_id: int
	user: User
	created_at: datetime

class MessageCollection(BaseModel):
	meta: MetaData
	messages: list[Message]