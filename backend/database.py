import json
from datetime import date
from uuid import uuid4

from backend.models.user import (
    User,
    UserResponse
)

# Open 'db' and begin reading the json file
with open("backend/fake_db.json", "r") as f:
    DB = json.load(f)
    
def get_all_users() -> list[User]:
    return [User(**user_data) for user_data in DB["users"].values()]