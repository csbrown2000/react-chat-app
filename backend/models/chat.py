from pydantic import BaseModel
from datetime import datetime


# id: the id of the chat (string)
# name: the name of the chat (string)
# user_ids: the ids of the users in the chat (list of strings)
# owner_id: the id of the user that owns the chat (string)
# created_at: the datetime the chat was created in ISO format (string of the form yyyy-mm-ddThh:mm:ss)
class Chat(BaseModel):
	id: str
	name: str
	user_ids: list[str]
	owner_id: str
	created_at: datetime