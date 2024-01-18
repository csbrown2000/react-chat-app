from pydantic import BaseModel
from datetime import datetime

# id: the id of the user (string)
# created_at: the datetime the user was created in ISO format (string of the form yyyy-mm-ddThh:mm:ss)
class User(BaseModel):
	id: str
	created_at: datetime

