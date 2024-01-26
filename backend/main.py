from fastapi import FastAPI

# Router imports
from backend.routers.chats import chats_router
from backend.routers.users import users_router

app = FastAPI(
	title="Pony Express API",
	description="API for chat application",
)

# Router list
app.include_router(chats_router)
app.include_router(users_router)