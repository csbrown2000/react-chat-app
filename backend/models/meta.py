from pydantic import BaseModel
from datetime import datetime

class MetaData(BaseModel):
	"""
	Represents metadata for a specific data object.
	
	Attributes:
		count (int): The count of the data object.
	"""
	count: int

class ChatMetaData(BaseModel):
	message_count: int
	user_count: int
