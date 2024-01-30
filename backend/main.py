from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

# Router imports
from backend.routers.chats import chats_router
from backend.routers.users import users_router
from backend.models.exception import EntityNotFoundException

app = FastAPI(
	title="Pony Express API",
	description="API for chat application",
)

# Router list
app.include_router(chats_router)
app.include_router(users_router)

# Setup exception stuff
@app.exception_handler(EntityNotFoundException)
def handle_entity_not_found(
    _request: Request,
    exception: EntityNotFoundException,
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={
            "detail": {
                "type": "entity_not_found",
                "entity_name": exception.entity_name,
                "entity_id": exception.entity_id,
            },
        },
    )