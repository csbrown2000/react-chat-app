from fastapi import APIRouter
from typing import Literal

from backend import database as db

from backend.models.user import (
	UserCollection
)


users_router = APIRouter(prefix="/users", tags=["Users"])

@users_router.get("", response_model=UserCollection)
def get_users(
	sort: Literal["id", "created_at"] = "id"
):
	sort_key = lambda animal: getattr(animal, sort)
	users = db.get_all_users()

	return UserCollection(
		meta={"count": len(users)},
		users=sorted(users, key=sort_key)
	)