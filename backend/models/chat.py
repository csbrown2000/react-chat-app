from pydantic import BaseModel
from datetime import datetime

from backend.models.meta import MetaData

class Chat(BaseModel):
	"""
	Represents a chat room.

	Attributes:
		id (str): The unique identifier of the chat.
		name (str): The name of the chat.
		user_ids (list[str]): The list of user IDs participating in the chat.
		owner_id (str): The ID of the chat owner.
		created_at (datetime): The timestamp when the chat was created.
	"""
	id: str
	name: str
	user_ids: list[str]
	owner_id: str
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